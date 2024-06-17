from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from authentication import schemas 
from app.core.config import settings
from app.database import get_db
from authentication.schemas import user as user_schemas
from authentication.utils import auth_handler,user_signup,user_login_util,change_pass

user_router=APIRouter(prefix='/users')

@user_router.post('/create',tags=['Authentication Management'], name='Sign-up', response_model=user_schemas.UserOut)
def create_user(user_data:schemas.user.User, db:Session = Depends(get_db)):
    response_data = user_signup.signup(user_data, db)
    return response_data

@user_router.post('/login',tags=['Authentication Management'],name='Login')
def user_login(user_data:user_schemas.UserLogin, db: Session = Depends(get_db)):
    response__data=user_login_util.login(user_data.email,user_data.password,db)
    return response__data

@user_router.post('/changepassword',tags=['Authentication Management'],name='changepassword')
def user_profile(user_data:schemas.user.ChangePassword,user_id: str = Depends(auth_handler.authenticate_access_token),db: Session = Depends(get_db)):
    respons_data=change_pass.change_password(user_data,user_id,db)
    return respons_data

@user_router.post('/refresh',tags=['Authentication Management'],name='refresh')
def user_profile(user_data:user_schemas.UserRefreshToken,db: Session = Depends(get_db)):
    respons_data=user_login_util.generate_access_token_using_refresh(user_data.refresh_token,db)
    return respons_data

@user_router.post('/forgotpassword_phonenumber', tags=['Authentication Management'], name='Forgot Password Phonenumber')
def forgot_password(user_data:user_schemas.ForgotPasswordPhonenumber, db: Session = Depends(get_db)):
    response_data = user_login_util.generate_otp_forget_password_phonenumber(user_data.phone_number, db)
    return response_data

@user_router.post('/otp_verification_forgotpassword_phonenumber', tags=['Authentication Management'], name='OTP Verification Phonenumber')
def otp_verification(user_data:user_schemas.OTPVerificationPhonenumber, db: Session = Depends(get_db)):
    response_data = user_login_util.verify_otp_forget_password_phonenumber(user_data.phone_number, user_data.otp, db)
    return response_data

@user_router.post('/forgotpassword_email', tags=['Authentication Management'], name='Forgot Password Email')
def send_mail(user_data:user_schemas.ForgotPasswordEmail, db: Session = Depends(get_db)):
    response_data = user_login_util.generate_otp_forget_password_email(user_data.email, db)
    return response_data

@user_router.post('/otp_verification_forgotpassword_email', tags=['Authentication Management'], name='OTP Verification Email')
def otp_verification(user_data:user_schemas.OTPVerificationEmail, db: Session = Depends(get_db)):
    response_data = user_login_util.verify_otp_forget_password_email(user_data.email, user_data.otp, db)
    return response_data

@user_router.post('/forgotpassword_changepassword',tags=['Authentication Management'],name='ForgotPassword changepassword')
def user_profile(user_data:schemas.user.Forgotpassword_ChangePassword,user_id: str = Depends(auth_handler.authenticate_access_token),db: Session = Depends(get_db)):
    respons_data=change_pass.forgot_password(user_data,user_id,db)
    return respons_data

@user_router.post('/login-generateotp', tags=['Authentication Management'], name='Generate OTP Login')
def generate_otp(user_data:user_schemas.Usergenerateotplogin, db: Session = Depends(get_db)):
    response_data = user_login_util.generate_otp(user_data.email, db)
    return response_data

@user_router.post('/otp-login', tags=['Authentication Management'], name='OTP Login')
def otp_login(user_data:user_schemas.Useremailotplogin, db: Session = Depends(get_db)):
    response_data = user_login_util.otp_login(user_data.email, user_data.otp, db)
    return response_data