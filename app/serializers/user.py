from pydantic import BaseModel
from typing import Optional

class UserBaseSerializer(BaseModel):
    username: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    company_id: Optional[int]

class UserSerializerIn(UserBaseSerializer):
    password: Optional[str]

class UserSerializerOut(UserBaseSerializer):
    
    id: int

    class Config:
        orm_mode = True