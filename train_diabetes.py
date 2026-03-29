import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Load dataset
data = pd.read_csv("data/diabetes.csv")

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Models
models = {
    "RandomForest": RandomForestClassifier(random_state=42),
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "GradientBoosting": GradientBoostingClassifier()
}

best_model = None
best_score = 0

print("\n=== Diabetes Model Comparison ===")

for name, model in models.items():
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_prob)

    print(f"{name} -> Accuracy: {acc:.4f}, ROC-AUC: {roc:.4f}")

    if roc > best_score:
        best_score = roc
        best_model = model

# Save best model
os.makedirs("models", exist_ok=True)
joblib.dump(best_model, "models/diabetes_model.pkl")
joblib.dump(scaler, "models/diabetes_scaler.pkl")

print("\n✅ Best Diabetes Model Saved!")