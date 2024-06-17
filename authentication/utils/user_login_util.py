import hashlib
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from authentication.utils.auth_handler import create_access_and_refresh_token
from authentication.models import user as user_model
import math,random
import os, time
import jwt
from sqlalchemy import func
from app.core.config import settings
from datetime import datetime,timedelta
from dotenv import load_dotenv
from authentication.utils import email_util

def login(email, password, db):
    user_data = db.query(user_model.User).filter(user_model.User.email == email).first()
    if user_data:
        md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        if md5_password == user_data.password:
            token = create_access_and_refresh_token(user_data.id,user_data.first_name)
            return token
        else:
            raise HTTPException(detail={"error_msg": "Incorrect password"}, status_code=200)
    else:
        raise HTTPException(detail={"error_msg": "User does not exist"}, status_code=200)
      
def generate_access_token_using_refresh(refresh_token,db):
    try:
    
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_TOKEN_ACCESS_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        expires_at = payload.get("expires")
        if expires_at is not None and datetime.utcnow().timestamp() > expires_at:
            raise HTTPException(status_code=200, detail="Token has expired")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=200, detail="Token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    token = create_access_and_refresh_token(payload['user_id'],payload['first_name'])
    return token

def _generateOTP() :
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
   # length of password can be changed
   # by changing value in range
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def generate_otp_forget_password_phonenumber(phone_number, db):
    load_dotenv()
    user_data = db.query(user_model.User).filter(user_model.User.phone_number == phone_number).first()
    if user_data:
        user_id = user_data.id
        # Checking for old OTP and deleting
        db.query(user_model.OTP).filter(user_model.OTP.user_id == user_data.id).delete()
        otp = _generateOTP()
        expire_minutes = int(os.environ['OTP_EXPIRE_MINUTES'])
        current_datetime = datetime.now()
        expires_at = current_datetime + timedelta(minutes=expire_minutes)
        max_id = db.query(func.max(user_model.OTP.id)).scalar()
        new_id = max_id + 1 if max_id else 1
        otp_res = user_model.OTP(id=new_id, user_id=user_id, otp_code=otp, expire_at=expires_at)
        db.add(otp_res)
        db.commit()
        db.refresh(otp_res)
        print(otp)
        if otp_res:
            # Send OTP to the user's phone number
            # email_util.send_sms(user_data, otp)  # Assuming you have a function for sending SMS
            return {'otp_generated': True, 'otp': "", 'phone': phone_number}
        else:
            raise HTTPException(detail={"error_msg": "Problem in generating OTP"}, status_code=200)
    else:
        raise HTTPException(detail={"error_msg": "User does not exist"}, status_code=200)


def verify_otp_forget_password_phonenumber(phone_number, otp, db):
    load_dotenv()
    user_data = db.query(user_model.User).filter(user_model.User.phone_number == phone_number).first()
    if user_data:
        expires_at = datetime.now()
        check_otp = db.query(user_model.OTP).filter(user_model.OTP.user_id == user_data.id,
                                                    user_model.OTP.otp_code == otp).first()
        if check_otp:
            if expires_at < check_otp.expire_at:
                # OTP is valid, return user data or perform other actions
                db.delete(check_otp)
                db.commit()
                token = create_access_and_refresh_token(user_data.id,user_data.first_name)
                return token
               
            else:
                raise HTTPException(detail={"error_msg": "OTP expired"}, status_code=200)
        else:
            raise HTTPException(detail={"error_msg": "Invalid OTP"}, status_code=200)
    else:
        raise HTTPException(detail={"error_msg": "User does not exist"}, status_code=404)


def send_email(email, otp):
    subject = "Your Smartters One-Time Password (OTP)"
    body = "<p>Dear User,</p>\
<p>We received a request to reset the password for your Smartters account.</p>\
<p>To proceed with the password reset, please use the following One-Time Password (OTP) to verify your identity:</p>\
<p>OTP: ["+otp+"]</p>\
<p>This OTP is valid for a single use and will expire in 10 minutes. Please do not share this OTP with anyone for security reasons. Our team will never ask for your OTP.</p>\
<p>If you did not request this password reset, kindly ignore this email or report it to softwaresmartters@gmail.com.</p>\
<p>Thank you for choosing Smartters.</p>\
<p>Best regards,<br>Smartters Team</p>"
    
    email_util.send_email(email, subject, body)

def generate_otp_forget_password_email(email, db):
    load_dotenv()
    user_data = db.query(user_model.User).filter(user_model.User.email == email).first()
    if user_data:
        user_id = user_data.id
        # Checking for old OTP and deleting
        db.query(user_model.OTP).filter(user_model.OTP.user_id == user_data.id).delete()
        otp = _generateOTP()
        expire_minutes = int(os.environ['OTP_EXPIRE_MINUTES'])
        current_datetime = datetime.now()
        expires_at = current_datetime + timedelta(minutes=expire_minutes)
        max_id = db.query(func.max(user_model.OTP.id)).scalar()
        new_id = max_id + 1 if max_id else 1
        otp_res = user_model.OTP(id=new_id, user_id=user_id, otp_code=otp, expire_at=expires_at)
        db.add(otp_res)
        db.commit()
        db.refresh(otp_res)
        if otp_res:
            send_email(email, otp)
            return {'otp_generated': True, 'otp': "", 'Email': email}
        else:
            raise HTTPException(detail={"error_msg": "Problem in generating OTP"}, status_code=200)
    else:
        raise HTTPException(detail={"error_msg": "User does not exist"}, status_code=200)
    
def verify_otp_forget_password_email(email, otp, db):
    load_dotenv()
    user_data = db.query(user_model.User).filter(user_model.User.email == email).first()
    if user_data:
        expires_at = datetime.now()
        check_otp = db.query(user_model.OTP).filter(user_model.OTP.user_id == user_data.id,
                                                    user_model.OTP.otp_code == otp).first()
        if check_otp:
            if expires_at < check_otp.expire_at:
                # OTP is valid, return user data or perform other actions
                db.delete(check_otp)
                db.commit()
                token = create_access_and_refresh_token(user_data.id,user_data.first_name)
                return token
               
            else:
                raise HTTPException(detail={"error_msg": "OTP expired"}, status_code=200)
        else:
            raise HTTPException(detail={"error_msg": "Invalid OTP"}, status_code=200)
    else:
        raise HTTPException(detail={"error_msg": "User does not exist"}, status_code=404)

def generate_otp(email, db):
    user_data = db.query(user_model.User).filter(user_model.User.email == email).first()
    if user_data:
        user_id = user_data.id
        # Checking for old OTP and deleting
        db.query(user_model.OTP).filter(user_model.OTP.user_id == user_data.id).delete()
        otp = _generateOTP()
        expire_minutes = int(os.environ['OTP_EXPIRE_MINUTES'])
        current_datetime = datetime.now()
        expires_at = current_datetime + timedelta(minutes=expire_minutes)
        max_id = db.query(func.max(user_model.OTP.id)).scalar()
        new_id = max_id + 1 if max_id else 1
        otp_res = user_model.OTP(id=new_id, user_id=user_id, otp_code=otp, expire_at=expires_at)
        db.add(otp_res)
        db.commit()
        db.refresh(otp_res)
        if otp_res:
            send_email_OTP(email, otp)
            return {'otp_generated': True, 'otp': "", 'Email': email}
        else:
            raise HTTPException(detail={"error_msg": "Problem in generating OTP"}, status_code=200)
    else:
        raise HTTPException(detail={"error_msg": "User does not exist"}, status_code=200)
    
def otp_login(email, otp, db):
    load_dotenv()
    user_data = db.query(user_model.User).filter(user_model.User.email == email).first()
    if user_data:
        expires_at = datetime.now() 
        check_otp = db.query(user_model.OTP).filter(user_model.OTP.user_id == user_data.id,
                                                    user_model.OTP.otp_code == otp).first()
        if check_otp:
            if expires_at < check_otp.expire_at:
                token = create_access_and_refresh_token(user_data.id,user_data.first_name)
                db.delete(check_otp)
                db.commit()
                return token
            else:
                raise HTTPException(detail={"error_msg": "OTP Expired"}, status_code=200)    
        else:
            raise HTTPException(detail={"error_msg": "OTP Invalid"}, status_code=200)
            
    else:
        raise HTTPException(detail={"error_msg": "User does not exist"}, status_code=200)
    
def send_email_OTP(email, otp):
    subject = "Your Smartters One-Time Password (OTP)"
    body = "<p>Dear User,</p>\
<p>We received a request to login via OTP for your Smartters account.</p>\
<p>To proceed with the OTP login, please use the following One-Time Password (OTP) to verify your identity:</p>\
<p>OTP: ["+otp+"]</p>\
<p>This OTP is valid for a single use and will expire in 10 minutes. Please do not share this OTP with anyone for security reasons. Our team will never ask for your OTP.</p>\
<p>If you did not request this  OTP login, kindly ignore this email or report it to softwaresmartters@gmail.com.</p>\
<p>Thank you for choosing Smartters.</p>\
<p>Best regards,<br>Smartters Team</p>"
    email_util.send_email(email, subject, body)