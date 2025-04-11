import json
import yaml

tap_properties_path = "/home/adriel/Documentos/professional/INDICIUM/de-indicium/meltano/.meltano/run/tap-postgres/tap.properties.json"
meltano_yaml_path = "/home/adriel/Documentos/professional/INDICIUM/de-indicium/meltano/meltano.yml"

def extract_relevant_tables_and_columns():
    """
    Extracts relevant tables and columns from tap.properties.json.
    Returns a dictionary with table names as keys and relevant columns as values.
    """
    with open(tap_properties_path, "r") as file:
        tap_data = json.load(file)

    relevant_tables = {}
    for stream in tap_data.get("streams", []):
        table_name = stream.get("table_name")
        schema = stream.get("schema", {}).get("properties", {})
        if table_name:
            # Filter columns based on keywords
            relevant_columns = {
                column: properties.get("type", [])
                for column, properties in schema.items()
                if any(keyword in column for keyword in ["length", "position", "numeric", "max", "minimun", "integer", "sizing_id","datetime", "supported_value"])
            }
            # Only add the table if it has relevant columns
            if relevant_columns:
                relevant_tables[table_name] = relevant_columns
    return relevant_tables

def update_meltano_yaml(relevant_tables):
    """
    Updates meltano.yml with the extracted table and column information.
    Handles datetime fields by setting their type to string with a format of date-time.
    """
    with open(meltano_yaml_path, "r") as file:
        meltano_config = yaml.safe_load(file)

    for extractor in meltano_config["plugins"]["extractors"]:
        if extractor["name"] == "tap-postgres":
            schema = extractor.get("schema", {})
            for table, columns in relevant_tables.items():
                # Ensure the table exists in the schema or create it
                table_key = f"information_schema-{table}"
                if table_key not in schema:
                    schema[table_key] = {}

                # Update only the relevant columns
                for column, column_type in columns.items():
                    # Handle datetime fields
                    if "datetime" in column:
                        schema[table_key][column] = {
                            "type": ["integer", "null"],
                            "format": "date-time"
                        }
                    else:
                        # Default to integer and null for other relevant columns
                        schema[table_key][column] = {"type": ["integer", "null"]}

            # Update the extractor schema
            extractor["schema"] = schema
            break
    else:
        raise ValueError("Extractor 'tap-postgres' not found in meltano.yml")

    with open(meltano_yaml_path, "w") as file:
        yaml.dump(meltano_config, file, default_flow_style=False, sort_keys=False)

    print("meltano.yml updated successfully!")

if __name__ == "__main__":
    # Step 1: Extract relevant tables and columns from tap.properties.json
    relevant_tables = extract_relevant_tables_and_columns()
    print("Relevant tables and columns extracted:", relevant_tables)

    # Step 2: Update meltano.yml with the extracted information
    
    update_meltano_yaml(relevant_tables)