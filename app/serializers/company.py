
from pydantic import BaseModel
from typing import Optional, List

class CompanyBaseSerializer(BaseModel):
    name: Optional[str]
    description: Optional[str]

class CompanySerializerIn(CompanyBaseSerializer):
    pass

class CompanySerializerOut(CompanyBaseSerializer):
    id: int
    users: Optional[List[int]]

    class Config:
        orm_mode = True