from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import joblib
import os

app = Flask(__name__)

# ===============================
# DATABASE CONFIGURATION
# ===============================
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "patients.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ===============================
# DATABASE MODEL
# ===============================
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    disease = db.Column(db.String(50))
    prediction = db.Column(db.Integer)
    risk_probability = db.Column(db.Float)
    risk_level = db.Column(db.String(20))
    suggestion = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# ===============================
# CREATE TABLES
# ===============================
with app.app_context():
    db.create_all()
    print("Database and tables are ready!")

# ===============================
# LOAD TRAINED MODELS + SCALERS
# ===============================
diabetes_model = joblib.load("models/diabetes_model.pkl")
diabetes_scaler = joblib.load("models/diabetes_scaler.pkl")

pcos_model = joblib.load("models/pcos_model.pkl")
pcos_scaler = joblib.load("models/pcos_scaler.pkl")

heart_model = joblib.load("models/heart_model.pkl")
heart_scaler = joblib.load("models/heart_scaler.pkl")

# ===============================
# HELPER FUNCTIONS
# ===============================
def classify_risk(prob):
    if prob < 0.4:
        return "Low"
    elif prob < 0.7:
        return "Medium"
    else:
        return "High"

def generate_suggestion(disease, risk_level):
    if risk_level == "Low":
        return "Maintain a healthy lifestyle with balanced diet and regular exercise."
    if disease == "diabetes":
        return "Monitor glucose levels regularly and consult a physician."
    if disease == "heart":
        return "Check cholesterol and blood pressure. Consult a cardiologist."
    if disease == "pcos":
        return "Consult a gynecologist and monitor hormone levels."
    return "Consult a healthcare professional."

# ===============================
# ROUTES
# ===============================
@app.route("/")
def home():
    return render_template("home_page.html")

@app.route("/prediction")
def prediction_page():
    return render_template("prediction_form.html")

@app.route("/predict", methods=["POST"])
def predict():
    req = request.get_json()
    if not req:
        return jsonify({"error": "No JSON received"}), 400

    disease = req.get("disease")
    data = req.get("data")
    name = req.get("name")
    gender = req.get("gender")

    if not disease or not data:
        return jsonify({"error": "Missing disease or data"}), 400

    try:
        # ==========================
        # Select features, scaler, and model
        # ==========================
        if disease == "diabetes":
            fields = ["Pregnancies","Glucose","BloodPressure","SkinThickness",
                      "Insulin","BMI","DiabetesPedigreeFunction","Age"]
            features = np.array([[float(data[field]) for field in fields]])
            features_scaled = diabetes_scaler.transform(features)
            model_to_use = diabetes_model

        elif disease == "pcos":
            fields = ["Age","BMI","Menstrual_Irregularity",
                      "Testosterone_Level","Antral_Follicle_Count"]
            features = np.array([[float(data[field]) for field in fields]])
            features_scaled = pcos_scaler.transform(features)
            model_to_use = pcos_model

        elif disease == "heart":
            fields = ["age","sex","cp","trestbps","chol","fbs","restecg",
                      "thalach","exang","oldpeak","slope","ca","thal"]
            features = np.array([[float(data[field]) for field in fields]])
            features_scaled = heart_scaler.transform(features)
            model_to_use = heart_model

        else:
            return jsonify({"error": "Invalid disease type"}), 400

        # ==========================
        # Make prediction
        # ==========================
        prediction = int(model_to_use.predict(features_scaled)[0])
        probability = float(model_to_use.predict_proba(features_scaled)[0][1])
        risk_level = classify_risk(probability)
        suggestion = generate_suggestion(disease, risk_level)

        # ==========================
        # Save to database
        # ==========================
        new_patient = Patient(
            name=name,
            age=int(data.get("Age", data.get("age", 0))),
            gender=gender,
            disease=disease,
            prediction=prediction,
            risk_probability=probability,
            risk_level=risk_level,
            suggestion=suggestion
        )
        db.session.add(new_patient)
        db.session.commit()

        return jsonify({
            "prediction": prediction,
            "risk_probability": probability,
            "risk_level": risk_level,
            "suggestion": suggestion
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/patients")
def view_patients():
    patients = Patient.query.order_by(Patient.date_created.desc()).all()
    output = []
    for p in patients:
        output.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "disease": p.disease,
            "prediction": p.prediction,
            "risk_level": p.risk_level,
            "risk_probability": p.risk_probability,
            "date_created": p.date_created
        })
    return jsonify(output)

# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(debug=True)