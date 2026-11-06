
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Temporary storage for equipment reports
reports = []


# Home page

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("downtime.html")

    equipment_name = request.form.get("equipment_name", "").strip()
    reason = request.form.get("reason", "").strip()

    try:
        downtime_minutes = int(request.form.get("downtime_minutes", ""))
    except ValueError:
        return render_template(
            "downtime.html",
            error="Enter downtime as a whole number of minutes.",
        ), 400

    if not equipment_name or not reason or downtime_minutes < 1:
        return render_template(
            "downtime.html",
            error="Enter an equipment name, at least 1 minute, and a reason.",
        ), 400

    entry = {
        "equipment_name": equipment_name,
        "downtime_minutes": downtime_minutes,
        "reason": reason,
    }
    return render_template("downtime.html", entry=entry)



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
