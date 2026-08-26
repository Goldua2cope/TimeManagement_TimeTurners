import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

def upload_report(local_file_path, blob_name, container_name="time-management-container"):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
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

