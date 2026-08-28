import os
import psycopg2
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

load_dotenv()

KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")

def get_password():
    try:
        if KEY_VAULT_URL:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
            password = client.get_secret("psql-password").value
            print("Using password from Key Vault")
            return password
    except Exception as e:
        print(f"Could not reach Key Vault ({e}), falling back to .env")

    return os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=get_password(),
        port=os.getenv("DB_PORT")
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Connected!")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)