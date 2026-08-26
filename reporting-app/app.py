from flask import Flask, request, jsonify
from report_builder import build_report_text, save_report_to_file
from upload import upload_report

app = Flask(__name__)

@app.route("/report", methods=["POST"])
def generate_report():
    data = request.get_json()

    if not data or "start" not in data or "end" not in data:
        return jsonify({"error": "JSON body must include 'start' and 'end' (YYYY-MM-DD)"}), 400

    start_date = data["start"]
    end_date = data["end"]

    text = build_report_text(start_date, end_date)
    filename = f"report_{start_date}_to_{end_date}.txt"
    save_report_to_file(text, filename)
    upload_report(filename, filename)

    return jsonify({
        "status": "uploaded",
        "blobName": filename,
        "container": "time-management-container"
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)