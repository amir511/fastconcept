from app.models.db_setup.session import BaseModel
import sqlalchemy as sql
from sqlalchemy.orm import validates
from hashlib import sha256


class User(BaseModel):
    '''
    User model is the place to store all the information related to the user
    It should have also a password field that is being hashed before stored
    For this purpose we can create a method similar to Django: set_password
    The user should also have a flag is_admin (False by default)
    Admins are the ones that can create other users
    as well as some other stuff that cannot be done by regular users
    There should be a foreignKey relationship between the user and the company
    i.e. A company can have many users, but a user is assigned only to one company
    Other info are:
    username
    email
    phone number

    '''
    __tablename__ = 'users'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    username = sql.Column(sql.String(30), unique=True, nullable=False)
    email = sql.Column(sql.String, nullable=True)
    phone_number = sql.Column(sql.Text, nullable=True)
    password = sql.Column(sql.String, nullable=False)
    company_id = sql.Column(sql.Integer, sql.ForeignKey('companies.id'), nullable=False)

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def set_password(self, new_password):
        hashed_password = sha256(new_password.encode()).hexdigest()
        self.password = hashed_password
    
    def verify_password(self, received_password):
        hashed_password = sha256(received_password.encode()).hexdigest()
        return self.password == hashed_password

        
