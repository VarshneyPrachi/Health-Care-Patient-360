import os
import sys

import joblib
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.append(PROJECT_ROOT)


# =========================================================
# DIRECTORIES
# =========================================================

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "ml",
    "outputs"
)

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "ml",
    "models"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# =========================================================
# MODEL FILES
# =========================================================

logistic_model_file = os.path.join(
    MODEL_DIR,
    "logistic_regression.joblib"
)

random_forest_model_file = os.path.join(
    MODEL_DIR,
    "random_forest.joblib"
)


# =========================================================
# LOAD MODELS
# =========================================================

print("\nLoading trained models...")

logistic_model = joblib.load(
    logistic_model_file
)

random_forest_model = joblib.load(
    random_forest_model_file
)

print("Models loaded successfully.")


# =========================================================
# GET FEATURE NAMES
# =========================================================

print("\nExtracting transformed feature names...")


preprocessor = (
    logistic_model
    .named_steps["preprocessor"]
)


feature_names = (
    preprocessor
    .get_feature_names_out()
)


# Remove pipeline prefixes for readability
clean_feature_names = [
    name.replace(
        "numeric__",
        ""
    ).replace(
        "categorical__",
        ""
    )
    for name in feature_names
]


# =========================================================
# LOGISTIC REGRESSION IMPORTANCE
# =========================================================

print("\nCalculating Logistic Regression importance...")


logistic_classifier = (
    logistic_model
    .named_steps["model"]
)


coefficients = (
    logistic_classifier
    .coef_[0]
)


logistic_importance = pd.DataFrame(
    {
        "feature": clean_feature_names,
        "coefficient": coefficients,
        "absolute_importance": abs(coefficients)
    }
)


logistic_importance = (
    logistic_importance
    .sort_values(
        "absolute_importance",
        ascending=False
    )
)


# =========================================================
# SAVE LOGISTIC RESULTS
# =========================================================

logistic_csv = os.path.join(
    OUTPUT_DIR,
    "logistic_regression_feature_importance.csv"
)


logistic_importance.to_csv(
    logistic_csv,
    index=False
)


# =========================================================
# LOGISTIC REGRESSION PLOT
# =========================================================

top_logistic = (
    logistic_importance
    .head(15)
    .sort_values(
        "coefficient"
    )
)


plt.figure(
    figsize=(10, 7)
)


plt.barh(
    top_logistic["feature"],
    top_logistic["coefficient"]
)


plt.xlabel(
    "Coefficient"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Logistic Regression - Top Feature Effects"
)

plt.tight_layout()


logistic_plot = os.path.join(
    OUTPUT_DIR,
    "logistic_regression_feature_importance.png"
)


plt.savefig(
    logistic_plot,
    dpi=150
)

plt.close()


# =========================================================
# RANDOM FOREST IMPORTANCE
# =========================================================

print(
    "\nCalculating Random Forest importance..."
)


rf_preprocessor = (
    random_forest_model
    .named_steps["preprocessor"]
)


rf_classifier = (
    random_forest_model
    .named_steps["model"]
)


rf_feature_names = (
    rf_preprocessor
    .get_feature_names_out()
)


rf_clean_feature_names = [
    name.replace(
        "numeric__",
        ""
    ).replace(
        "categorical__",
        ""
    )
    for name in rf_feature_names
]


rf_importance = pd.DataFrame(
    {
        "feature": rf_clean_feature_names,
        "importance": (
            rf_classifier
            .feature_importances_
        )
    }
)


rf_importance = (
    rf_importance
    .sort_values(
        "importance",
        ascending=False
    )
)


# =========================================================
# SAVE RANDOM FOREST RESULTS
# =========================================================

rf_csv = os.path.join(
    OUTPUT_DIR,
    "random_forest_feature_importance.csv"
)


rf_importance.to_csv(
    rf_csv,
    index=False
)


# =========================================================
# RANDOM FOREST PLOT
# =========================================================

top_rf = (
    rf_importance
    .head(15)
    .sort_values(
        "importance"
    )
)


plt.figure(
    figsize=(10, 7)
)


plt.barh(
    top_rf["feature"],
    top_rf["importance"]
)


plt.xlabel(
    "Feature Importance"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Random Forest - Top Feature Importance"
)

plt.tight_layout()


rf_plot = os.path.join(
    OUTPUT_DIR,
    "random_forest_feature_importance.png"
)


plt.savefig(
    rf_plot,
    dpi=150
)

plt.close()


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n")
print("=" * 60)
print("LOGISTIC REGRESSION - TOP FEATURES")
print("=" * 60)

print(
    logistic_importance
    .head(15)
    .to_string(index=False)
)


print("\n")
print("=" * 60)
print("RANDOM FOREST - TOP FEATURES")
print("=" * 60)

print(
    rf_importance
    .head(15)
    .to_string(index=False)
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 60)
print("MODEL EXPLAINABILITY COMPLETED")
print("=" * 60)


print(
    "\nLogistic Regression CSV:"
)

print(
    logistic_csv
)


print(
    "\nRandom Forest CSV:"
)

print(
    rf_csv
)


print(
    "\nLogistic Regression plot:"
)

print(
    logistic_plot
)


print(
    "\nRandom Forest plot:"
)

print(
    rf_plot
)