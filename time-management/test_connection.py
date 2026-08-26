import psycopg2

try:
    connection = psycopg2.connect(
        host="time-manager.postgres.database.azure.com",
        database="time_turner",
        user="admin_turner",
        password="pass",
        port="5432",
        sslmode="require"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)

    tables = cursor.fetchall()

    print("Tables in database:")

    for table in tables:
        print(table[0])

    cursor.close()
    connection.close()

except Exception as error:
    print("Error:")
    print(error)