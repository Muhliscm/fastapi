from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from . import schema, models, database
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, key=settings.secret_key,
                             algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
