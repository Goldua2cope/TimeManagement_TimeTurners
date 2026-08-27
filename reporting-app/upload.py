import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

load_dotenv()

KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")

def get_storage_connection_string():
    try:
        if KEY_VAULT_URL:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
            conn_str = client.get_secret("storageac-constring").value
            print("Using storage connection string from Key Vault")
            return conn_str
    except Exception as e:
        print(f"Could not reach Key Vault ({e}), falling back to .env")
        return 

def upload_report(local_file_path, blob_name, container_name="time-management-container"):
    connection_string = get_storage_connection_string()
    client = BlobServiceClient.from_connection_string(connection_string)
    container_client = client.get_container_client(container_name)

    with open(local_file_path, "rb") as f:
        container_client.upload_blob(name=blob_name, data=f, overwrite=True)

    print(f"Uploaded {local_file_path} as {blob_name} to container '{container_name}'")

if __name__ == "__main__":
    upload_report(
        local_file_path="report_2026-08-01_to_2026-08-31.txt",
        blob_name="report_2026-08-01_to_2026-08-31.txt"
    )