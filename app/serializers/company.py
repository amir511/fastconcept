
from pydantic import BaseModel
from typing import Optional, List
from app.serializers.user import UserSerializerOut

class CompanyBaseSerializer(BaseModel):
    name: Optional[str]
    description: Optional[str]

class CompanySerializerIn(CompanyBaseSerializer):
    pass

class CompanySerializerOut(CompanyBaseSerializer):
    id: int
    users: Optional[List[UserSerializerOut]]

    class Config:
        orm_mode = True