import joblib

def load_models():
    models = {}

    try:
        models["diabetes"] = {
            "model": joblib.load("models/diabetes_model.pkl"),
            "scaler": joblib.load("models/diabetes_scaler.pkl")
        }
    except:
        print("Diabetes model not found")

    try:
        models["heart"] = {
            "model": joblib.load("models/heart_model.pkl"),
            "scaler": joblib.load("models/heart_scaler.pkl")
        }
    except:
        print("Heart model not found")

    try:
        models["pcos"] = {
            "model": joblib.load("models/pcos_model.pkl"),
            "scaler": joblib.load("models/pcos_scaler.pkl")
        }
    except:
        print("PCOS model not found")

    return models