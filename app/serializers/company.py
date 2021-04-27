
from pydantic import BaseModel
from typing import Optional

class CompanyBaseSerializer(BaseModel):
    name: Optional[str]
    description: Optional[str]

class CompanySerializerIn(CompanyBaseSerializer):
    pass

class CompanySerializerOut(CompanyBaseSerializer):
    id: int

    class Config:
        orm_mode = True