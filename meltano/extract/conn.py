import psycopg2
import yaml

conn_source = psycopg2.connect(
    host="localhost",
    port=5433,
    database="northwind",
    user="northwind",
    password="northwind"
)

conn_target = psycopg2.connect(
    host="localhost",
    port=5434,
    database="northwind",
    user="northwind",
    password="northwind"
)



def fetch_tables():
    conn = conn_source
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return tables



def update_tables_meltano_yml(tables):
    with open('meltano.yml', 'r') as file:
        meltano_config = yaml.safe_load(file)
    
    for extractor in meltano_config["plugins"]["extractors"]:
        if extractor["name"] == "tap-postgres":
            extractor["config"]["tables"] = tables
            break
    else:
        raise ValueError("Extractor 'tap-postgres' not found in meltano.yml")

    with open('meltano.yml', 'w') as file:
        yaml.dump(meltano_config, file, default_flow_style=False, sort_keys=False)



