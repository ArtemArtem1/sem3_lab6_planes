from pydantic import BaseModel, ConfigDict, Field


class PlaneCreateSchema(BaseModel):
    registration: str = Field(min_length=1)
    model: str = Field(min_length=1)
    airline: str = Field(min_length=1)


class PlaneSchema(PlaneCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

