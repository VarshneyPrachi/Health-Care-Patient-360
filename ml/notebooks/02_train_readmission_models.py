import os
import sys
import joblib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    roc_curve
)


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

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# =========================================================
# LOAD ML DATASET
# =========================================================

print("\nLoading readmission ML dataset...")

input_file = os.path.join(
    OUTPUT_DIR,
    "readmission_ml_dataset.csv"
)

df = pd.read_csv(
    input_file
)

print(
    f"Loaded {len(df):,} records."
)


# =========================================================
# DEFINE TARGET
# =========================================================

TARGET = "readmitted_30d"


X = df.drop(
    columns=[TARGET]
)

y = df[TARGET]


# =========================================================
# DISPLAY TARGET DISTRIBUTION
# =========================================================

print("\nTarget distribution:")

print(
    y.value_counts()
)


print("\nTarget percentage:")

print(
    y.value_counts(
        normalize=True
    )
    .mul(100)
    .round(2)
)


# =========================================================
# IDENTIFY FEATURE TYPES
# =========================================================

categorical_features = [
    "gender",
    "city",
    "insurance_type",
    "admission_type",
    "admission_source",
    "department_name"
]


numeric_features = [
    "patient_age",
    "previous_admissions",
    "days_since_previous_admission",
    "diagnosis_count",
    "treatment_count",
    "lab_test_count",
    "abnormal_lab_count"
]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

print("\nCreating train/test split...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print(
    f"Training records: {len(X_train):,}"
)

print(
    f"Testing records: {len(X_test):,}"
)


# =========================================================
# PREPROCESSING
# =========================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)


categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)


# =========================================================
# DEFINE MODELS
# =========================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=10,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
}


# =========================================================
# TRAIN MODELS
# =========================================================

results = []

trained_models = {}

roc_data = {}


for model_name, model in models.items():

    print("\n" + "=" * 60)

    print(
        f"Training {model_name}..."
    )

    print("=" * 60)


    # -----------------------------------------------------
    # Create pipeline
    # -----------------------------------------------------

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )


    # -----------------------------------------------------
    # Train
    # -----------------------------------------------------

    pipeline.fit(
        X_train,
        y_train
    )


    # -----------------------------------------------------
    # Predictions
    # -----------------------------------------------------

    y_pred = pipeline.predict(
        X_test
    )

    y_probability = pipeline.predict_proba(
        X_test
    )[:, 1]


    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )


    # -----------------------------------------------------
    # Store results
    # -----------------------------------------------------

    results.append(
        {
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1_Score": f1,
            "ROC_AUC": roc_auc
        }
    )


    trained_models[
        model_name
    ] = pipeline


    # -----------------------------------------------------
    # ROC curve data
    # -----------------------------------------------------

    fpr, tpr, _ = roc_curve(
        y_test,
        y_probability
    )

    roc_data[
        model_name
    ] = {
        "fpr": fpr,
        "tpr": tpr,
        "roc_auc": roc_auc
    }


    # -----------------------------------------------------
    # Print metrics
    # -----------------------------------------------------

    print(
        f"\nAccuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )


    # -----------------------------------------------------
    # Classification report
    # -----------------------------------------------------

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Not Readmitted",
                "Readmitted"
            ],
            zero_division=0
        )
    )


    # -----------------------------------------------------
    # Confusion matrix
    # -----------------------------------------------------

    cm = confusion_matrix(
        y_test,
        y_pred
    )


    print(
        "Confusion Matrix:"
    )

    print(
        cm
    )


    # -----------------------------------------------------
    # Save confusion matrix
    # -----------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(6, 5)
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=[
            "Not Readmitted",
            "Readmitted"
        ]
    )

    display.plot(
        ax=ax
    )

    ax.set_title(
        f"{model_name} - Confusion Matrix"
    )

    plt.tight_layout()


    safe_name = (
        model_name
        .lower()
        .replace(" ", "_")
    )


    confusion_file = os.path.join(
        OUTPUT_DIR,
        f"{safe_name}_confusion_matrix.png"
    )


    plt.savefig(
        confusion_file,
        dpi=150
    )

    plt.close()


    # -----------------------------------------------------
    # Save predictions
    # -----------------------------------------------------

    prediction_df = X_test.copy()

    prediction_df[
        "actual_readmitted"
    ] = y_test.values

    prediction_df[
        "predicted_readmitted"
    ] = y_pred

    prediction_df[
        "readmission_probability"
    ] = y_probability


    prediction_file = os.path.join(
        OUTPUT_DIR,
        f"{safe_name}_predictions.csv"
    )


    prediction_df.to_csv(
        prediction_file,
        index=False
    )


    # -----------------------------------------------------
    # Save model
    # -----------------------------------------------------

    model_file = os.path.join(
        MODEL_DIR,
        f"{safe_name}.joblib"
    )


    joblib.dump(
        pipeline,
        model_file
    )


# =========================================================
# MODEL COMPARISON
# =========================================================

results_df = pd.DataFrame(
    results
)


print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print(
    results_df.to_string(
        index=False
    )
)


comparison_file = os.path.join(
    OUTPUT_DIR,
    "readmission_model_comparison.csv"
)


results_df.to_csv(
    comparison_file,
    index=False
)


# =========================================================
# ROC CURVE
# =========================================================

plt.figure(
    figsize=(8, 6)
)


for model_name, data in roc_data.items():

    plt.plot(
        data["fpr"],
        data["tpr"],
        label=(
            f"{model_name} "
            f"(AUC = {data['roc_auc']:.3f})"
        )
    )


plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)


plt.xlabel(
    "False Positive Rate"
)

plt.ylabel(
    "True Positive Rate"
)

plt.title(
    "Readmission Prediction - ROC Curve"
)

plt.legend()

plt.tight_layout()


roc_file = os.path.join(
    OUTPUT_DIR,
    "readmission_roc_curve.png"
)


plt.savefig(
    roc_file,
    dpi=150
)

plt.close()


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 60)
print("MODEL TRAINING COMPLETED")
print("=" * 60)


print(
    "\nModel files saved in:"
)

print(
    MODEL_DIR
)


print(
    "\nComparison file:"
)

print(
    comparison_file
)


print(
    "\nROC curve:"
)

print(
    roc_file
)


print(
    "\nReadmission prediction pipeline completed successfully."
)