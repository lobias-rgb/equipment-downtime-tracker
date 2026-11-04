
from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary storage for equipment reports
reports = []


# Home page
@app.route("/")
def home():
    return "Equipment Downtime Tracker is running!"


# Submit an equipment failure report
@app.route("/reports", methods=["POST"])
def create_report():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing report information"}), 400

    equipment_id = data.get("equipment_id")
    description = data.get("description")

    if not equipment_id or not description:
        return jsonify({
            "error": "Equipment ID and description are required"
        }), 400

    report = {
        "report_id": len(reports) + 1,
        "equipment_id": equipment_id,
        "description": description,
        "status": "Open"
    }

    reports.append(report)

    return jsonify(report), 201


# Retrieve equipment failure reports
@app.route("/reports", methods=["GET"])
def get_reports():
    return jsonify(reports)


# Start the application locally
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
