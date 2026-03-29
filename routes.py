from flask import Blueprint, request, jsonify

routes = Blueprint("routes", __name__)

@routes.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        disease = data.get("disease")
        patient_data = data.get("data")

        # Basic validation
        if not disease or not patient_data:
            return jsonify({"error": "Missing data"}), 400

        # Dummy prediction logic (replace with ML later)
        score = sum(patient_data.values()) / len(patient_data)

        if score > 100:
            prediction = "High Risk"
            risk_level = "High"
        elif score > 50:
            prediction = "Medium Risk"
            risk_level = "Medium"
        else:
            prediction = "Low Risk"
            risk_level = "Low"

        return jsonify({
            "prediction": prediction,
            "risk_probability": round(score, 2),
            "risk_level": risk_level,
            "suggestion": "Consult a doctor for proper diagnosis."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500