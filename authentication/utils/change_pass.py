import hashlib
from fastapi import HTTPException
from fastapi.responses   import JSONResponse
from authentication.models.user import User


def change_password(userdata,user_id,db):
    user=db.query(User).get(user_id)
    if not user:
        raise HTTPException(detail={"error_msg":"User does not exist"},status_code=400)
    old_password=hashlib.md5(userdata.current_password.encode('utf-8')).hexdigest()
    if user.password!=old_password:
        raise HTTPException(detail={"error_msg":"Old password is incorrect"},status_code=400)
    user.password=hashlib.md5(userdata.new_password.encode('utf-8')).hexdigest()
    db.commit()
    db.refresh(user)
    return JSONResponse({"msg":"Password change successfully"},status_code=200)

def forgot_password(userdata, user_id, db):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(detail={"error_msg":"User does not exist"},status_code=400)
    user.password=hashlib.md5(userdata.new_password.encode('utf-8')).hexdigest()
    db.commit()
    db.refresh(user)
    return JSONResponse({"msg":"Password change successfully"},status_code=200)