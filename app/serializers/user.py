from pydantic import BaseModel
from typing import Optional

class UserBaseSerializer(BaseModel):
    username: str
    email: Optional[str]
    phone_number: Optional[str]
    company_id: int

class UserSerializerIn(UserBaseSerializer):
    password: str

class UserSerializerOut(UserBaseSerializer):
    id: int