from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "app": "time-management"
    })


VAULT_NAME = "time-management-v"
VAULT_URL = f"https://{VAULT_NAME}.vault.azure.net"

credential = DefaultAzureCredential()

secret_client = SecretClient(
    vault_url=VAULT_URL,
    credential=credential
)


def get_db_connection():
    db_password = secret_client.get_secret("psql-password").value

    return psycopg2.connect(
        host="time-manager.postgres.database.azure.com",
        database="time_turner",
        user="admin_turner",
        password=db_password,
        port="5432",
        sslmode="require"
    )


@app.route("/time", methods=["POST"])
def add_time():
    data = request.get_json()

    consultant_id = data["consultant_id"]
    customer_id = data["customer_id"]
    work_date = data["work_date"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    lunch_break = data["lunch_break"]

    start = datetime.strptime(start_time, "%H:%M:%S")
    end = datetime.strptime(end_time, "%H:%M:%S")

    total_minutes = int((end - start).total_seconds() / 60)
    worked_minutes = total_minutes - lunch_break
    worked_hours = round(worked_minutes / 60, 2)

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
    """
    INSERT INTO timeentries (
        consultant_id,
        customer_id,
        work_date,
        start_time,
        end_time,
        lunch_break
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
    """,
    (
        consultant_id,
        customer_id,
        work_date,
        start_time,
        end_time,
        lunch_break
    )
)

    entry_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({
        "id": entry_id,
        "consultant_id": consultant_id,
        "customer_id": customer_id,
        "work_date": work_date,
        "start_time": start_time,
        "end_time": end_time,
        "lunch_break": lunch_break,
        "worked_minutes": worked_minutes,
        "worked_hours": worked_hours,
        "message": "Time information saved successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)