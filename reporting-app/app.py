from flask import Flask, request, jsonify
from report_builder import build_report_text, save_report_to_file
from upload import upload_report

app = Flask(__name__)

@app.route("/report", methods=["GET"])
def generate_report():
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    if not start_date or not end_date:
        return jsonify({"error": "start and end query params are required (YYYY-MM-DD)"}), 400

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