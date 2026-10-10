import os
import sys

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
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
# LOAD DATASET
# =========================================================

print("\nLoading LOS ML dataset...")

input_file = os.path.join(
    OUTPUT_DIR,
    "los_ml_dataset.csv"
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

TARGET = "length_of_stay"

X = df.drop(
    columns=[TARGET]
)

y = df[TARGET]


# =========================================================
# FEATURE TYPES
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
    random_state=42
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
# MODELS
# =========================================================

models = {

    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        max_depth=14,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1
    )
}


# =========================================================
# TRAIN MODELS
# =========================================================

results = []

trained_models = {}


for model_name, model in models.items():

    print("\n" + "=" * 60)

    print(
        f"Training {model_name}..."
    )

    print("=" * 60)


    # -----------------------------------------------------
    # Pipeline
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
    # Predict
    # -----------------------------------------------------

    y_pred = pipeline.predict(
        X_test
    )


    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    mae = mean_absolute_error(
        y_test,
        y_pred
    )


    rmse = mean_squared_error(
        y_test,
        y_pred
    ) ** 0.5


    r2 = r2_score(
        y_test,
        y_pred
    )


    # -----------------------------------------------------
    # Save results
    # -----------------------------------------------------

    results.append(
        {
            "Model": model_name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }
    )


    trained_models[
        model_name
    ] = pipeline


    # -----------------------------------------------------
    # Display metrics
    # -----------------------------------------------------

    print(
        f"\nMAE : {mae:.4f} days"
    )

    print(
        f"RMSE: {rmse:.4f} days"
    )

    print(
        f"R²  : {r2:.4f}"
    )


    # -----------------------------------------------------
    # Save predictions
    # -----------------------------------------------------

    prediction_df = X_test.copy()

    prediction_df[
        "actual_length_of_stay"
    ] = y_test.values

    prediction_df[
        "predicted_length_of_stay"
    ] = y_pred.round(2)


    safe_name = (
        model_name
        .lower()
        .replace(" ", "_")
    )


    prediction_file = os.path.join(
        OUTPUT_DIR,
        f"{safe_name}_los_predictions.csv"
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
        f"{safe_name}_los.joblib"
    )


    joblib.dump(
        pipeline,
        model_file
    )


    # -----------------------------------------------------
    # Actual vs Predicted Plot
    # -----------------------------------------------------

    plt.figure(
        figsize=(7, 6)
    )


    plt.scatter(
        y_test,
        y_pred,
        alpha=0.4
    )


    # Perfect prediction line
    min_value = min(
        y_test.min(),
        y_pred.min()
    )

    max_value = max(
        y_test.max(),
        y_pred.max()
    )


    plt.plot(
        [min_value, max_value],
        [min_value, max_value],
        linestyle="--"
    )


    plt.xlabel(
        "Actual Length of Stay"
    )

    plt.ylabel(
        "Predicted Length of Stay"
    )

    plt.title(
        f"{model_name} - Actual vs Predicted LOS"
    )


    plt.tight_layout()


    plot_file = os.path.join(
        OUTPUT_DIR,
        f"{safe_name}_los_actual_vs_predicted.png"
    )


    plt.savefig(
        plot_file,
        dpi=150
    )

    plt.close()


# =========================================================
# MODEL COMPARISON
# =========================================================

results_df = pd.DataFrame(
    results
)


print("\n")
print("=" * 60)
print("LOS MODEL COMPARISON")
print("=" * 60)


print(
    results_df.to_string(
        index=False
    )
)


comparison_file = os.path.join(
    OUTPUT_DIR,
    "los_model_comparison.csv"
)


results_df.to_csv(
    comparison_file,
    index=False
)


# =========================================================
# RANDOM FOREST FEATURE IMPORTANCE
# =========================================================

print("\nCalculating Random Forest feature importance...")


rf_model = trained_models[
    "Random Forest"
]


rf_preprocessor = (
    rf_model
    .named_steps["preprocessor"]
)


rf_regressor = (
    rf_model
    .named_steps["model"]
)


feature_names = (
    rf_preprocessor
    .get_feature_names_out()
)


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


feature_importance = pd.DataFrame(
    {
        "feature": clean_feature_names,
        "importance": (
            rf_regressor
            .feature_importances_
        )
    }
)


feature_importance = (
    feature_importance
    .sort_values(
        "importance",
        ascending=False
    )
)


importance_file = os.path.join(
    OUTPUT_DIR,
    "los_random_forest_feature_importance.csv"
)


feature_importance.to_csv(
    importance_file,
    index=False
)


# =========================================================
# FEATURE IMPORTANCE PLOT
# =========================================================

top_features = (
    feature_importance
    .head(15)
    .sort_values(
        "importance"
    )
)


plt.figure(
    figsize=(10, 7)
)


plt.barh(
    top_features["feature"],
    top_features["importance"]
)


plt.xlabel(
    "Feature Importance"
)

plt.ylabel(
    "Feature"
)

plt.title(
    "Random Forest - LOS Feature Importance"
)

plt.tight_layout()


importance_plot = os.path.join(
    OUTPUT_DIR,
    "los_random_forest_feature_importance.png"
)


plt.savefig(
    importance_plot,
    dpi=150
)

plt.close()


# =========================================================
# DISPLAY FEATURE IMPORTANCE
# =========================================================

print("\n")
print("=" * 60)
print("TOP LOS FEATURES")
print("=" * 60)


print(
    feature_importance
    .head(15)
    .to_string(
        index=False
    )
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 60)
print("LOS MODEL TRAINING COMPLETED")
print("=" * 60)


print(
    "\nModels saved in:"
)

print(
    MODEL_DIR
)


print(
    "\nModel comparison:"
)

print(
    comparison_file
)


print(
    "\nFeature importance:"
)

print(
    importance_file
)


print(
    "\nLOS prediction pipeline completed successfully."
)