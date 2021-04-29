from datetime import datetime, timedelta
from uuid import uuid4

import jwt
import pytz
from app.settings import settings
from jwt.exceptions import DecodeError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.db_setup.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login/')


class JWTHelper:
    """Helper class to faciltate the usage of JWT authentication."""

    def __init__(self, refresh_token=None, access_token=None):
        """Initialize an instance of the helper class based on given token."""
        if not refresh_token and not access_token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='A token is required for authentication')
        self.token, self.token_type = (refresh_token, 'refresh') if refresh_token else (access_token, 'access')
        try:
            self.payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
        except DecodeError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Corrupt token')

    @staticmethod
    def generate_access_and_refresh_tokens(username):
        """Return access and refresh tokens based on username"""
        access_token_expiration_timestamp = (
            datetime.now(pytz.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION)).timestamp()
        access_token = jwt.encode(
            {
                'name': username,
                'iat': access_token_expiration_timestamp,
                'jti': str(uuid4())
            },
            settings.SECRET_KEY,
            algorithm='HS256')

        refresh_token_expiration_timestamp = (
            datetime.now(pytz.utc) + timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRATION)).timestamp()
        refresh_token = jwt.encode(
            {
                'access': access_token,
                'iat': refresh_token_expiration_timestamp,
                'jti': str(uuid4())
            },
            settings.SECRET_KEY,
            algorithm='HS256')

        return access_token, refresh_token

    def is_expired(self):
        """Check if token has expired."""
        expiration_time = datetime.utcfromtimestamp(self.payload.get('iat'))
        if datetime.now(pytz.utc) > pytz.utc.localize(expiration_time):
            return True
        return False

    def get_access_info(self):
        """Return `username` from token."""
        if self.token_type == 'refresh':
            original_access_token = self.payload.get('access')
            try:
                original_access_payload = jwt.decode(original_access_token, settings.SECRET_KEY, algorithms=['HS256'])
            except DecodeError:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Corrupt token')
            username = original_access_payload.get('name')
        else:
            username = self.payload.get('name')
        return username

    def refresh_access_token(self):
        """Return a new access token based on the given refresh token."""
        if self.token_type != 'refresh':
            raise AssertionError('Provided token should be a refresh token.')
        original_access_token = self.payload.get('access')
        try:
            original_access_payload = jwt.decode(original_access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except DecodeError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Corrupt token')
        name = original_access_payload.get('name')
        new_access_token_expiration_timestamp = (
            datetime.now(pytz.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION)).timestamp()
        new_access_token = jwt.encode(
            {
                'name': name,
                'iat': new_access_token_expiration_timestamp,
                'jti': str(uuid4())
            },
            settings.SECRET_KEY,
            algorithm='HS256')

        return new_access_token

def authenticate_user(access_token: str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
    jwt_helper = JWTHelper(access_token=access_token)
    if jwt_helper.is_expired():
        return None
    username = jwt_helper.get_access_info()
    user = db.query(User).filter(User.username==username).one()
    return user
