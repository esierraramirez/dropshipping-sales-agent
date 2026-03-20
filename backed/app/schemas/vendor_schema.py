from pydantic import BaseModel


class VendorResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True