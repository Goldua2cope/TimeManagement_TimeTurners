from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/time", methods=["POST"])
def add_time():
    data = request.get_json()

    start_time = data["startTime"]
    end_time = data["endTime"]
    lunch_break = data["lunchBreak"]
    consultant_name = data["consultantName"]
    customer_name = data["customerName"]

    # Convert the time text into Python time values
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    # Calculate total minutes between start and end
    total_minutes = int((end - start).total_seconds() / 60)

    # Remove the lunch break
    worked_minutes = total_minutes - lunch_break

    # Convert worked minutes to hours
    worked_hours = round(worked_minutes / 60, 2)

    return jsonify({
        "startTime": start_time,
        "endTime": end_time,
        "lunchBreak": lunch_break,
        "consultantName": consultant_name,
        "customerName": customer_name,
        "workedMinutes": worked_minutes,
        "workedHours": worked_hours,
        "message": "Time information received successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)