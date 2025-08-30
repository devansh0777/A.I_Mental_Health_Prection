from preprocessing import df_copy
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


X = df_copy.drop(columns=["treatment"])
y = df_copy["treatment"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Select categorical & numerical columns
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

# Preprocess separately for categorical & numerical
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),   # Scale numerical features
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)  # Encode categorical features
    ]
)

log_reg_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Fit the pipeline
log_reg_pipeline.fit(X_train, y_train)

# Accuracy
train_acc = log_reg_pipeline.score(X_train, y_train)
test_acc = log_reg_pipeline.score(X_test, y_test)

print("Training Accuracy:", train_acc)
print("Test Accuracy:", test_acc)

cv_scores = cross_val_score(log_reg_pipeline, X, y, cv=5, scoring="f1")
print("Cross-validated F1 score:", cv_scores.mean())

import joblib

# Save model
joblib.dump(log_reg_pipeline, "mental_health_model.pkl")

# Load model
loaded_model = joblib.load("mental_health_model.pkl")

# Use for prediction
y_pred = loaded_model.predict(X_test)
