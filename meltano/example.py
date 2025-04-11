import psycopg2


conn_target = psycopg2.connect(
    host="localhost",
    port=5434,
    database="northwind",
    user="northwind",
    password="northwind"
)

if __name__ == "__main__":
   # Chame a função
    cursor = conn_target.cursor()
    cursor.execute("""SELECT * FROM order_details""")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn_target.close()