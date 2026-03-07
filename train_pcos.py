import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, confusion_matrix
import joblib
import os

# =========================
# Load Dataset
# =========================
data = pd.read_csv("data/pcos.csv")
data.columns = data.columns.str.strip()  # Remove spaces

target_column = "PCOS_Diagnosis"

# Separate features and target
y = data[target_column]
X = data.drop(target_column, axis=1)

# Fill missing values
X = X.fillna(X.mean())

# =========================
# Feature Scaling
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# Train-Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# =========================
# Hyperparameter Tuning
# =========================
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

rf = RandomForestClassifier(random_state=42)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=cv,
    n_jobs=-1,
    verbose=2,
    scoring='roc_auc'
)

# Train model
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

print("Best Hyperparameters:", grid_search.best_params_)

# =========================
# Predictions & Evaluation
# =========================
y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# =========================
# Save Model & Scaler
# =========================
os.makedirs("models", exist_ok=True)
joblib.dump(best_model, "models/pcos_model.pkl")
joblib.dump(scaler, "models/pcos_scaler.pkl")

print("\n✅ PCOS model and scaler saved successfully!")
print(f"Total features used: {X.shape[1]}")