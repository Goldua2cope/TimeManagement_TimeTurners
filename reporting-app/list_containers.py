import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()
client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
for container in client.list_containers():
    print(container.name)