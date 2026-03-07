DIABETES_FEATURES = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age"
]

HEART_FEATURES = [
    "age","sex","cp","trestbps","chol","fbs",
    "restecg","thalach","exang","oldpeak",
    "slope","ca","thal"
]

PCOS_FEATURES = [
    "Age",
    "BMI",
    "Menstrual_Irregularity",
    "Testosterone_Level(ng/dL)",
    "Antral_Follicle_Count"
]


def validate_input(disease, data):
    if disease == "diabetes":
        required = DIABETES_FEATURES
    elif disease == "heart":
        required = HEART_FEATURES
    elif disease == "pcos":
        required = PCOS_FEATURES
    else:
        return False, "Invalid disease type"

    for feature in required:
        if feature not in data:
            return False, f"Missing feature: {feature}"

    return True, None