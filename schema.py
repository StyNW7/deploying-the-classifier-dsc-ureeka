from pydantic import BaseModel, Field


class ShopperInput(BaseModel):
    """Raw input columns from the original online shoppers dataset."""

    Administrative: float = Field(0, ge=0)
    Administrative_Duration: float = Field(0, ge=0)
    Informational: float = Field(0, ge=0)
    Informational_Duration: float = Field(0, ge=0)
    ProductRelated: float = Field(0, ge=0)
    ProductRelated_Duration: float = Field(0, ge=0)
    BounceRates: float = Field(0, ge=0)
    ExitRates: float = Field(0, ge=0)
    PageValues: float = Field(0, ge=0)
    SpecialDay: float = Field(0, ge=0)

    Month: str = "Nov"
    OperatingSystems: int = Field(2, ge=1)
    Browser: int = Field(2, ge=1)
    Region: int = Field(1, ge=1)
    TrafficType: int = Field(2, ge=1)
    VisitorType: str = "Returning_Visitor"
    Weekend: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "Administrative": 0,
                "Administrative_Duration": 0,
                "Informational": 0,
                "Informational_Duration": 0,
                "ProductRelated": 5,
                "ProductRelated_Duration": 320.5,
                "BounceRates": 0.02,
                "ExitRates": 0.05,
                "PageValues": 15.3,
                "SpecialDay": 0,
                "Month": "Nov",
                "OperatingSystems": 2,
                "Browser": 2,
                "Region": 1,
                "TrafficType": 2,
                "VisitorType": "Returning_Visitor",
                "Weekend": False,
            }
        }
    }


class PredictionResponse(BaseModel):
    will_purchase: bool
    prediction: int
    prediction_label: str
    probability: float
    threshold: float