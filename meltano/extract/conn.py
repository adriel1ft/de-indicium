import psycopg2
import yaml

# Conectar ao banco de dados fonte
conn_source = psycopg2.connect(
    host="localhost",
    port=5433,
    database="northwind",
    user="northwind",
    password="northwind"
)

# Conectar ao banco de dados alvo
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

def ordinal_position():
    cursor = conn_source.cursor()
    cursor.execute("""
        SELECT table_name, column_name, ordinal_position
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_ordinal_positions():
    """
    Retorna as posições ordinais das colunas das tabelas no schema 'public',
    com ordinal_position convertido para texto.
    """

    cursor = conn_source.cursor()
    query = """
        SELECT table_name, column_name, ordinal_position::text AS ordinal_position
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    result = [
        {
            "table_name": row[0],
            "column_name": row[1],
            "ordinal_position": row[2],
        }
        for row in rows
        ]
    
    return result

if __name__ == "__main__":
   # Chame a função
    cursor = conn_target.cursor()
    cursor.execute("""SELECT * FROM order_details""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn_target.close()