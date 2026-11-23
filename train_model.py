
import pandas as pd

data = {
    "ticket": [
        "WiFi is not working",
        "Internet connection is very slow",
        "VPN is not connecting",
        "Unable to access company VPN",
        "I forgot my password",
        "Please reset my password",
        "Install Microsoft Office",
        "Application installation required",
        "Laptop keyboard is not working",
        "Monitor display is not working"
    ],

    "category": [
        "Network",
        "Network",
        "VPN",
        "VPN",
        "Password",
        "Password",
        "Software",
        "Software",
        "Hardware",
        "Hardware"
    ]
}

df = pd.DataFrame(data)

print(df)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

# Create the classification model
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train the model using the PDF dataset
model.fit(df["ticket"], df["category"])

# Create the models folder
os.makedirs("models", exist_ok=True)

# Save the trained model
joblib.dump(model, "models/ticket_classifier.pkl")

print("\nModel training completed successfully!")
print("Model saved successfully!")
