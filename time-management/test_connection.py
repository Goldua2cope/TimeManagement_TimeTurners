import psycopg2

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


VAULT_NAME = "time-management-v"
VAULT_URL = f"https://{VAULT_NAME}.vault.azure.net"

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url=VAULT_URL,
    credential=credential
)


try:
    # Get PostgreSQL password from Key Vault
    db_password = client.get_secret("psql-password").value

    # Connect to Azure PostgreSQL
    connection = psycopg2.connect(
        host="time-manager.postgres.database.azure.com",
        database="time_turner",
        user="admin_turner",
        password=db_password,
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

    print("Database connection successful!")
    print("Tables in database:")

    for table in tables:
        print(table[0])

    cursor.close()
    connection.close()

except Exception as error:
    print("Database connection failed:")
    print(error)