from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    location: str = Field(..., min_length=2)
    area: float = Field(..., gt=0)
    bedrooms: int = Field(..., ge=1)
    bathrooms: int = Field(..., ge=1)
    property_type: str = Field(..., min_length=2)
    floor: int = Field(..., ge=0)
    parking: int = Field(..., ge=0)
    age: int = Field(..., ge=0)


class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    estimated_price_lakhs: float
    price_range_lakhs: dict
    model_used: str
    metrics: dict
    input_summary: dict
