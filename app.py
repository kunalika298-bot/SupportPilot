
from flask import Flask, render_template, request, jsonify
from classifier import process_ticket
from database import create_table, save_ticket, get_tickets

app = Flask(__name__)

# Create the database table
create_table()


def handle_ticket(data):
    # Accept the PDF's standard JSON field "employee"
    # or the webpage field "employee_name"
    employee_name = data.get("employee_name") or data.get("employee")
    
    required_fields = {
        "employee_name": employee_name,
        "title": data.get("title"),
        "description": data.get("description"),
        "department": data.get("department")
    }

    for field, value in required_fields.items():
        if not value:
            raise ValueError(f"Please provide {field.replace('_', ' ')}")

    email = data.get("email", "Not provided")
    business_impact = data.get("business_impact", "Low")

    if business_impact not in ["High", "Low"]:
        raise ValueError("Business impact must be High or Low")

    # Combine title and description for classification
    ticket_text = data["title"] + " " + data["description"]

    # Predict category, severity, priority and confidence
    category, severity, priority, confidence = process_ticket(
        ticket_text,
        business_impact
    )

    # Prepare ticket for database storage
    ticket = {
        "employee_name": employee_name,
        "email": email,
        "title": data["title"],
        "description": data["description"],
        "department": data["department"],
        "business_impact": business_impact,
        "category": category,
        "severity": severity,
        "priority": priority,
        "confidence": confidence
    }

    # Save ticket and generate a readable ticket ID
    database_id = save_ticket(ticket)
    ticket_id = f"T{database_id:04d}"

    ticket["ticket_id"] = ticket_id
    return ticket


# Webpage route
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        try:
            result = handle_ticket(request.form.to_dict())
        except ValueError as e:
            error = str(e)

    tickets = get_tickets()

    return render_template(
        "index.html",
        result=result,
        error=error,
        tickets=tickets
    )


# REST API route
@app.route("/ticket", methods=["POST"])
def create_ticket():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "JSON data is required"}), 400

        result = handle_ticket(data)

        return jsonify({
            "message": "Ticket processed successfully",
            "ticket": result
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
