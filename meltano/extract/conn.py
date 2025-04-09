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


def update_meltano_yml(tables):
    with open('meltano.yml', 'r') as file:
        meltano_config = yaml.safe_load(file)
    
    meltano_config["plugins"]["extractors"][1]["config"]["tables"] = tables

    with open('meltano.yml', 'w') as file:
        yaml.dump(meltano_config, file, default_flow_style=False)