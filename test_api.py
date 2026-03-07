import requests
import json

URL = "http://127.0.0.1:5000/predict"

# ===============================
# 1️⃣ DIABETES TEST JSON
# ===============================
diabetes_data = {
    "disease": "diabetes",
    "data": {
        "Pregnancies": 2,
        "Glucose": 150,
        "BloodPressure": 80,
        "SkinThickness": 25,
        "Insulin": 100,
        "BMI": 32.5,
        "DiabetesPedigreeFunction": 0.5,
        "Age": 45
    }
}

# ===============================
# 2️⃣ HEART DISEASE TEST JSON
# ===============================
heart_data = {
    "disease": "heart",
    "data": {
        "age": 52,
        "sex": 1,
        "cp": 2,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.5,
        "slope": 2,
        "ca": 0,
        "thal": 2
    }
}

# ===============================
# 3️⃣ PCOS TEST JSON
# ===============================
pcos_data = {
    "disease": "pcos",
    "data": {
        "Age": 26,
        "BMI": 29,
        "Menstrual_Irregularity": 1,
        "Testosterone_Level(ng/dL)": 18,
        "Antral_Follicle_Count": 2

    }
}

# ===============================
# FUNCTION TO TEST
# ===============================
def test_api(payload):
    response = requests.post(URL, json=payload)
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=4))
    print("\n" + "="*50 + "\n")


# ===============================
# RUN TESTS
# ===============================
if __name__ == "__main__":
    print("Testing Diabetes Model")
    test_api(diabetes_data)

    print("Testing Heart Model")
    test_api(heart_data)

    print("Testing PCOS Model")
    test_api(pcos_data)