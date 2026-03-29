import requests

URL = "http://127.0.0.1:5000/predict"

data = {
    "name": "Kavya",
    "gender": "Female",
    "disease": "diabetes",
    "data": {
        "Pregnancies": 2,
        "Glucose": 150,
        "BloodPressure": 80,
        "SkinThickness": 25,
        "Insulin": 100,
        "BMI": 32,
        "DiabetesPedigreeFunction": 0.5,
        "Age": 45
    }
}

response = requests.post(URL, json=data)
print(response.json())