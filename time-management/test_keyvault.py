from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_NAME = "time-management-v"
VAULT_URL = f"https://{VAULT_NAME}.vault.azure.net"

try:
    credential = DefaultAzureCredential()

    client = SecretClient(
        vault_url=VAULT_URL,
        credential=credential
    )

    password = client.get_secret("psql-password").value

    if password:
        print("Successfully retrieved PostgreSQL password from Key Vault!")

except Exception as error:
    print("Error:")
    print(error)