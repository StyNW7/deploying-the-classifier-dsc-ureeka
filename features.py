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

    # TODO:
    # 1. Create model features