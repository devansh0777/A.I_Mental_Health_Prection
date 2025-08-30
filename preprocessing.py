import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder,StandardScaler,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report,confusion_matrix

df=pd.read_csv("mental_health.csv")
print(df.head())
print("Null Values")
print(df.isnull().sum())

df_copy=df.copy()
df_copy.drop(["Timestamp","obs_consequence","state","comments","Country","no_employees","anonymity","leave"], axis=1, inplace=True)
print(df_copy.info())
df_copy.dropna(inplace=True)
print(df_copy.isnull().sum())
print(df_copy.info())

# Convert string into lower
for col in df_copy.select_dtypes(include='object').columns:
    df_copy[col] = df_copy[col].astype(str).str.lower()

# Lowercase and strip spaces
df_copy['Gender'] = df_copy['Gender'].str.lower().str.strip()

# Replace common variations with standard ones
df_copy['Gender'] = df_copy['Gender'].replace({
    # Male variations
    'm': 'male', 'male ': 'male', 'man': 'male', 'mail': 'male',
    'make': 'male', 'mal': 'male', 'malr': 'male', 'msle': 'male',
    'cis male': 'male', 'cis man': 'male', 'male-ish': 'male', 'male leaning androgynous': 'male',
    'guy (-ish) ^_^': 'male', 'ostensibly male, unsure what that really means': 'male',

    # Female variations
    'f': 'female', 'femail': 'female', 'female ': 'female',
    'cis female': 'female', 'cis-female/femme': 'female',
    'female (cis)': 'female', 'woman': 'female',

    # Others / Non-binary
    'trans woman': 'other', 'trans-female': 'other', 'female (trans)': 'other',
    'non-binary': 'other', 'enby': 'other', 'genderqueer': 'other',
    'queer': 'other', 'queer/she/they': 'other', 'fluid': 'other',
    'androgyne': 'other', 'agender': 'other', 'neuter': 'other',
    'nah': 'other', 'all': 'other', 'p': 'other', 'a little about you': 'other'
})

gender_encoded = pd.get_dummies(df_copy['Gender'], prefix='Gender')
df_copy = pd.concat([df_copy.drop(columns=['Gender']), gender_encoded], axis=1)
le = LabelEncoder()
df_copy["treatment"] = le.fit_transform(df_copy["treatment"])

#Identify categorical and numeric columns
categorical_cols = df_copy.select_dtypes(include="object").columns
# numeric_cols = df_copy.select_dtypes(include=["int64", "float64"]).columns.drop("treatment", errors="ignore")

#One Hot Encoding for categorical variables
ohe = OneHotEncoder(drop="first", sparse_output=False)

# drop="first" avoids dummy variable trap (removes one redundant column)
ohe_encoded = pd.DataFrame(
    ohe.fit_transform(df_copy[categorical_cols]),
    columns=ohe.get_feature_names_out(categorical_cols),
    index=df_copy.index
)

# Concatenate back to df
df_copy = pd.concat([df_copy.drop(columns=categorical_cols), ohe_encoded], axis=1)

# Remove Outliers
df_copy = df_copy[(df_copy["Age"] > 10) & (df_copy["Age"] < 100)]

# Convert into standard scaler
scaler = StandardScaler()
df_copy["Age"]=scaler.fit_transform(df_copy[["Age"]])

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df_copy.head())
print(df_copy.info())

# Split Data

X=df_copy.drop("treatment",axis=1)
y=df_copy["treatment"]

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

print("Train set size:", X_train.shape)
print("Test set size:", X_test.shape)

# Train the model
results={}
# 1. Logistic Regression
log_res = LogisticRegression(max_iter=1000)
log_res.fit(X_train, y_train)

y_pred_lr = log_res.predict(X_test)
results["Logistic Regression"] = {
    "Accuracy": accuracy_score(y_test, y_pred_lr),
    "Precision": precision_score(y_test, y_pred_lr),
    "Recall": recall_score(y_test, y_pred_lr),
    "F1 Score": f1_score(y_test, y_pred_lr)
}

# 2. Random Forest
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
results["Random Forest"] = {
    "Accuracy": accuracy_score(y_test, y_pred_rf),
    "Precision": precision_score(y_test, y_pred_rf),
    "Recall": recall_score(y_test, y_pred_rf),
    "F1 Score": f1_score(y_test, y_pred_rf)
}

# 3. XGBoost
xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42)
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
results["XGBoost"] = {
    "Accuracy": accuracy_score(y_test, y_pred_xgb),
    "Precision": precision_score(y_test, y_pred_xgb),
    "Recall": recall_score(y_test, y_pred_xgb),
    "F1 Score": f1_score(y_test, y_pred_xgb)
}

# Print Results
print("\n🔹 Model Performance Comparison 🔹")
results_df = pd.DataFrame(results).T
print(results_df)
print("Classification Report")
print(classification_report(y_test, y_pred_lr))
conf_matrix=confusion_matrix(y_test,y_pred_lr)

plt.figure(figsize=(10,10))
sns.heatmap(conf_matrix,annot=True,fmt="d",cmap="YlGnBu",xticklabels=["Fail","Pass"],yticklabels=["Fail","Pass"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

import joblib
joblib.dump(log_res, "mental_model_logistic.pkl")

