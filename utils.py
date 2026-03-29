def classify_risk(prob):
    if prob < 0.4:
        return "Low"
    elif prob < 0.7:
        return "Medium"
    return "High"


def generate_suggestion(disease, risk):
    if risk == "Low":
        return "Maintain a healthy lifestyle."

    suggestions = {
        "diabetes": "Monitor sugar levels and exercise regularly.",
        "heart": "Check BP and cholesterol regularly.",
        "pcos": "Consult a gynecologist and maintain weight."
    }

    return suggestions.get(disease, "Consult a doctor.")


def format_response(pred, prob, risk, suggestion):
    return {
        "prediction": pred,
        "risk_probability": f"{prob*100:.2f}%",
        "risk_level": risk,
        "suggestion": suggestion
    }