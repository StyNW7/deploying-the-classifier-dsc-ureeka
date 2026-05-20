import numpy as np
import pandas as pd

from model import model_columns
from schema import ShopperInput

MONTH_ORDER = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "June": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}

LOG_COLUMNS = [
    "Administrative_Duration",
    "Informational_Duration",
    "ProductRelated_Duration",
    "TotalDuration",
    "ProductDurationPerPage",
    "AdminDurationPerPage",
    "InfoDurationPerPage",
    "AvgDurationPerPage",
    "ProductEngagement",
    "DurationWeightedExit",
    "DurationWeightedBounce",
]


def create_model_features(input_data: ShopperInput) -> pd.DataFrame:
    """Create the same engineered features that were used in Session 1."""

    df = pd.DataFrame([input_data.model_dump()])

    base_numeric_columns = [
        "Administrative",
        "Administrative_Duration",
        "Informational",
        "Informational_Duration",
        "ProductRelated",
        "ProductRelated_Duration",
        "BounceRates",
        "ExitRates",
        "PageValues",
        "SpecialDay",
    ]

    for column in base_numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Step 1: totals
    df["TotalDuration"] = (
        df["Administrative_Duration"].fillna(0)
        + df["Informational_Duration"].fillna(0)
        + df["ProductRelated_Duration"].fillna(0)
    )
    df["TotalPages"] = (
        df["Administrative"].fillna(0)
        + df["Informational"].fillna(0)
        + df["ProductRelated"].fillna(0)
    )

    # Step 2: averages and ratios
    df["ProductDurationPerPage"] = df["ProductRelated_Duration"] / df["ProductRelated"].replace(0, np.nan)
    df["AdminDurationPerPage"] = df["Administrative_Duration"] / df["Administrative"].replace(0, np.nan)
    df["InfoDurationPerPage"] = df["Informational_Duration"] / df["Informational"].replace(0, np.nan)

    df["ProductPageRatio"] = df["ProductRelated"] / df["TotalPages"].replace(0, np.nan)
    df["AdminPageRatio"] = df["Administrative"] / df["TotalPages"].replace(0, np.nan)
    df["InfoPageRatio"] = df["Informational"] / df["TotalPages"].replace(0, np.nan)

    df["ProductDurationRatio"] = df["ProductRelated_Duration"] / df["TotalDuration"].replace(0, np.nan)
    df["AdminDurationRatio"] = df["Administrative_Duration"] / df["TotalDuration"].replace(0, np.nan)
    df["InfoDurationRatio"] = df["Informational_Duration"] / df["TotalDuration"].replace(0, np.nan)

    # Step 3: engagement signals
    df["AvgDurationPerPage"] = df["TotalDuration"] / df["TotalPages"].replace(0, np.nan)
    df["ExitBounceGap"] = df["ExitRates"] - df["BounceRates"]
    df["ExitBounceRatio"] = df["ExitRates"] / df["BounceRates"].replace(0, np.nan)
    df["ProductEngagement"] = df["ProductRelated"] * df["ProductDurationPerPage"]
    df["DurationWeightedExit"] = df["TotalDuration"] * (1 - df["ExitRates"])
    df["DurationWeightedBounce"] = df["TotalDuration"] * (1 - df["BounceRates"])

    # Step 4: month features
    df["MonthNum"] = df["Month"].map(MONTH_ORDER)
    df["IsHolidaySeason"] = df["Month"].isin(["Nov", "Dec"]).astype(int)

    # Step 5: log versions for highly skewed duration features
    for column in LOG_COLUMNS:
        df[column + "_log"] = np.log1p(df[column].clip(lower=0))

    return df[model_columns]