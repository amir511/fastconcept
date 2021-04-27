
from pydantic import BaseModel

class CompanyBaseSerializer(BaseModel):
    name: str

class CompanySerializerIn(CompanyBaseSerializer):
    pass

class CompanySerializerOut(CompanyBaseSerializer):
    id: int

    class Config:
        orm_mode = True