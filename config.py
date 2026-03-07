import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MODEL_PATHS = {
    "diabetes": os.path.join(BASE_DIR, "models/diabetes_model.pkl"),
    "heart": os.path.join(BASE_DIR, "models/heart_model.pkl"),
    "pcos": os.path.join(BASE_DIR, "models/pcos_model.pkl"),
}