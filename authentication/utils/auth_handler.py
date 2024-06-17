import jwt
import os, time
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from app.core.config import settings
from datetime import datetime,timedelta
from fastapi import Request, HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme=HTTPBearer()

def create_access_and_refresh_token(user_id:int,first_name:str) -> dict:
    load_dotenv()
    access_expire_time = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
    refresh_expire_time = int(os.environ['REFRESH_TOKEN_EXPIRE_MINUTES'])
    access_token_payload = {
        "user_id": user_id,
        "first_name":first_name,
        "expires": datetime.timestamp(datetime.utcnow()+ timedelta(minutes=access_expire_time))
    }
    refresh_token_payload = {
        "user_id": user_id,
        "first_name":first_name,
        "expires": datetime.timestamp(datetime.utcnow() + timedelta(minutes=refresh_expire_time))
    }
    access_token = jwt.encode(access_token_payload , settings.JWT_ACCESS_TOKEN_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    refresh_token=jwt.encode(refresh_token_payload,settings.JWT_REFRESH_TOKEN_ACCESS_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
    return {"access_token":access_token,"refresh_token":refresh_token}

def authenticate_access_token(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(token.credentials, settings.JWT_ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        expires_at = payload.get("expires")
        if expires_at is not None and datetime.utcnow().timestamp() > expires_at:
            raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user_id

def authenticate_refresh_token(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(token.credentials, settings.JWT_REFRESH_TOKEN_ACCESS_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        expires_at = payload.get("expires")
        if expires_at is not None and datetime.utcnow().timestamp() > expires_at:
            raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user_id

def decodeAccessToken(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.credentials,settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        current_time = datetime.now()
        current_time_stamp = datetime.timestamp(current_time)
        return decoded_token if decoded_token["exp"] >=  current_time_stamp else None
    except:
        return None