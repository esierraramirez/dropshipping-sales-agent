from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


ToneType = Literal["formal", "friendly", "sales", "empathetic"]


class VendorSettingsUpsertRequest(BaseModel):
    business_start_hour: Optional[str] = Field(default=None, examples=["08:00"])
    business_end_hour: Optional[str] = Field(default=None, examples=["18:00"])
    off_hours_message: Optional[str] = Field(default=None, max_length=500)
    agent_enabled: bool = True
    tone: Optional[ToneType] = "friendly"

    @field_validator("business_start_hour", "business_end_hour")
    @classmethod
    def validate_hour_format(cls, value):
        if value is None:
            return value

        parts = value.split(":")
        if len(parts) != 2:
            raise ValueError("La hora debe tener formato HH:MM")

        hour, minute = parts
        if not hour.isdigit() or not minute.isdigit():
            raise ValueError("La hora debe contener solo números")

        h = int(hour)
        m = int(minute)

        if h < 0 or h > 23 or m < 0 or m > 59:
            raise ValueError("La hora debe estar en un rango válido")

        return value


class VendorSettingsResponse(BaseModel):
    vendor_id: int
    business_start_hour: Optional[str] = None
    business_end_hour: Optional[str] = None
    off_hours_message: Optional[str] = None
    agent_enabled: bool
    tone: Optional[str] = None

    class Config:
        from_attributes = True
