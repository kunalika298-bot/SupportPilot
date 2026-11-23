
import re
import joblib

# Load the trained AI model
model = joblib.load("models/ticket_classifier.pkl")


# Preprocess ticket text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Predict ticket category
def predict_category(ticket):
    cleaned_ticket = preprocess_text(ticket)

    prediction = model.predict([cleaned_ticket])
    confidence = model.predict_proba([cleaned_ticket]).max()

    return prediction[0], round(float(confidence) * 100, 2)


# Predict ticket severity
def predict_severity(ticket):
    text = ticket.lower()

    critical_words = [
        "server down",
        "entire company",
        "production down",
        "security breach"
    ]

    high_words = [
        "urgent",
        "cannot work",
        "business stopped",
        "client meeting",
        "vpn not working"
    ]

    medium_words = [
        "slow",
        "error",
        "problem",
        "issue"
    ]

    for word in critical_words:
        if word in text:
            return "Critical"

    for word in high_words:
        if word in text:
            return "High"

    for word in medium_words:
        if word in text:
            return "Medium"

    return "Low"


# Calculate ticket priority
def calculate_priority(severity, business_impact):
    if severity == "Critical" and business_impact == "High":
        return "P1"
    elif severity == "High" and business_impact == "High":
        return "P1"
    elif severity == "High":
        return "P2"
    elif severity == "Medium":
        return "P3"
    else:
        return "P4"


# Process the complete ticket
def process_ticket(ticket, business_impact):
    category, confidence = predict_category(ticket)
    severity = predict_severity(ticket)
    priority = calculate_priority(severity, business_impact)

    return category, severity, priority, confidence
