#!/usr/bin/env bash

# --- Provision resources for Time Management App ---
set -euo pipefail

# Load configuration
source .env

# Ensure Azure CLI is authenticated
az account show > /dev/null

# Prompt for postgres admin password
read -s -p "Enter PostgreSQL admin password: " POSTGRES_PASSWORD
echo

# Create resource group
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"
 
# Create keyvault for secrets
az keyvault create \
    --name "$KEY_VAULT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --enable-rbac-authorization true \
    --enable-purge-protection true \
    --retention-days 7 \
    --output none

## Assign access to vault
#az role assignment create \
#    --role "Key Vault Secrets Officer" \
#    --assignee "<upn>" \
#    --scope "/subscriptions/<subscription-id>/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/<vault-name>"

# Add secret to vault
az keyvault secret set \
    --vault-name "$KEY_VAULT_NAME" \
    --name "postgres-admin-password" \
    --value "$POSTGRES_PASSWORD" \
    --output none

# Create Azure postgres flexible-server
az postgres flexible-server create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$POSTGRES_SERVER" \
    --location "$LOCATION" \
    --admin-user "$POSTGRES_ADMIN" \
    --admin-password "$POSTGRES_PASSWORD" \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --public-access 0.0.0.0 \
    --storage-size 32 \
    --zonal-resiliency disabled 

# Create firewall rules to limit access to server
az postgres flexible-server firewall-rule create \
  --resource-group "$RESOURCE_GROUP" \
  --server-name "$POSTGRES_SERVER" \
  --name "$FIREWALL_RULE_NAME" \
  --start-ip-address "$CLIENT_IP" \
  --end-ip-address "$CLIENT_IP"

# Create database
az postgres flexible-server db create \
    --resource-group "$RESOURCE_GROUP" \
    --server-name "$POSTGRES_SERVER" \
    --name "$DB_NAME" \
    --only-show-errors \
    --output none

psql "host=$POSTGRES_SERVER.postgres.database.azure.com dbname=$DB_NAME user=$POSTGRES_ADMIN sslmode=require" \
  -set ON_ERROR_STOP=1 \
  -f ./database.sql

unset POSTGRES_PASSWORD

# Create Storage Account
az storage account create \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --sku Standard_LRS \
  --kind StorageV2 \
  --enable-hierarchical-namespace true \
  --allow-blob-public-access true \
  --output none

# Add Storage Account connection string to key vault
STORAGE_CONNECTION_STRING=$(az storage account show-connection-string \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --query connectionString \
  --output tsv)

az keyvault secret set \
  --vault-name "$KEY_VAULT_NAME" \
  --name "storage-connection-string" \
  --value "$STORAGE_CONNECTION_STRING" \
  --output none

# Add lifecycle management for blockblob objects
az storage account management-policy create \
    --account-name "$STORAGE_ACCOUNT" \
    --policy @storage_policy.json \
    --resource-group "$RESOURCE_GROUP"

# Create container for blob storage
az storage container create \
    --name "$STORAGE_CONTAINER" \
    --account-name "$STORAGE_ACCOUNT" \
    --auth-mode login \
    --output none

## Create ssh key for VMs
#ssh-keygen -t rsa -b 4096 -f "~/.ssh/$REPORT_SSH_KEY_SSH"
#ssh-keygen -t rsa -b 4096 -f "~/.ssh/$APP_SSH_KEY"

## Create VM for reporting application
#az vm create \
#    --name "$REPORT_VM" \
#    --resource-group "$RESOURCE_GROUP" \
#    --location "$LOCATION" \
#    --size "Standard_B1s" \
#    --image "Canonical:ubuntu-24_04-lts:server:latest" \
#    --admin-username "$VM_ADMIN" \
#    --ssh-key-values "$HOME/.ssh/$REPORT_SSH.pub" \
#    --zone 1 \
#    --output none

## Create VM for time management application
#az vm create \
#    --name "$APP_VM" \
#    --resource-group "$RESOURCE_GROUP" \
#    --location "$LOCATION" \
#    --size "Standard_B1s" \
#    --image "Canonical:ubuntu-24_04-lts:server:latest" \
#    --admin-username "$VM_ADMIN" \
#    --ssh-key-values "$HOME/.ssh/$APP_SSH_KEY.pub" \
#    --zone 1 \
#    --output none

# --- Ensure all resources are provisioned correctly: ---
echo "Resources successfully created:"
echo
echo "Key vault URI:"
az keyvault show \
    --name "$KEY_VAULT_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "properties.vaultUri"

echo
echo "Postgresql Server meta data:"
az postgres flexible-server show \
    --name "$POSTGRES_SERVER" \
    --resource-group "$RESOURCE_GROUP" \
    --query "{name:name, state:state, version:version, sku:sku.name, tier:sku.tier, location:location, admin:administratorLogin}" \
    --output table

echo
echo "Postgresql Databases:"
az postgres flexible-server db list \
  --server-name "$POSTGRES_SERVER" \
  --resource-group "$RESOURCE_GROUP" \
  --query "[].name" \
  --output table

echo
echo "Storage account meta data:"
az storage account show \
    --name "$STORAGE_ACCOUNT" \
    --resource-group "$RESOURCE_GROUP" \
    --query "{name:name, location:location, kind:kind, sku:sku.name, tier:accessTier, httpsOnly:httpsTrafficOnlyEnabled, minTls:minTlsVersion}" \
    --output table

echo
echo "Storage Container name:"
az storage container show \
    --name "$STORAGE_CONTAINER" \
    --account-name "$STORAGE_ACCOUNT" \
    --auth-mode login \
    --query "name"

echo
echo ("Secrets added to key vault:")
az keyvault secret list \
    --vault-name "$KEY_VAULT_NAME" \
    --query "[].name" \
    --output table