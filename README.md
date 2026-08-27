# Time Management Application

This is a simple time management application built with Python and Flask.

The consultant enters their working hours using Postman, including start time, end time, lunch break, consultant, and customer.

The application calculates the worked hours and saves the information in Azure PostgreSQL.

Azure Key Vault is used to securely store the PostgreSQL password.

## Application Flow

```text
Consultant
    ↓
Postman
    ↓
Flask REST API
    ↓
Azure Key Vault
    ↓
Gets PostgreSQL password
    ↓
Azure PostgreSQL Database
    ↓
Saves working-time information
