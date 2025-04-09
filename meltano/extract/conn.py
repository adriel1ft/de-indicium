import psycopg2

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


# Exemplo de consulta
cursor = conn_source.cursor()
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORder by table_name;

""")
tables = cursor.fetchall()

for table in tables:
    print(f" - {table[0]}")

cursor.close()
conn_source.close()
conn_target.close()