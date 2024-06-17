import hashlib
from fastapi import HTTPException
from sqlalchemy import or_
from authentication.models import user as user_models
from authentication.utils.auth_handler import create_access_and_refresh_token
from sqlalchemy import func

def signup(user,db):
    if db.query(user_models.User).filter(
            or_(user_models.User.email == user.email,user_models.User.phone_number == user.phone_number)
        ).first():
        raise HTTPException(detail={"error_msg":"Email or phone_number already exist"},status_code=200)    
    max_id = db.query(func.max(user_models.User.id)).scalar()
    new_id = max_id + 1 if max_id else 1
    user_data=user_models.User(
                            id = new_id,
                            username=user.first_name+" "+user.last_name,
                            first_name=user.first_name,
                            last_name=user.last_name,
                            email=user.email,
                            phone_number=user.phone_number,
                            password=hashlib.md5(user.password.encode('utf-8')).hexdigest(),
                          )
    
    db.add(user_data)
    db.commit()

    return user_data