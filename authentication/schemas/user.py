from typing import Optional
from pydantic import BaseModel,EmailStr,validator,Field,constr


class User(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    phone_number:str
    password:str

class UserOut(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    phone_number:str
    # token: dict
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values):
        if 'new_password' in values and confirm_password != values['new_password']:
            raise ValueError("Passwords do not match")
        return confirm_password
    
class UserRefreshToken(BaseModel):
    refresh_token:str

class ForgotPasswordPhonenumber(BaseModel):
    phone_number:constr(regex=r"^\d{10}$")

class OTPVerificationPhonenumber(BaseModel):
    phone_number:constr(regex=r"^\d{10}$")
    otp:str

class ForgotPasswordEmail(BaseModel):
    email:EmailStr

class OTPVerificationEmail(BaseModel):
    email:EmailStr
    otp:str

class Forgotpassword_ChangePassword(BaseModel):
    new_password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values):
        if 'new_password' in values and confirm_password != values['new_password']:
            raise ValueError("Passwords do not match")
        return confirm_password
    
class Usergenerateotplogin(BaseModel):
    email:EmailStr

class Useremailotplogin(BaseModel):
    email: EmailStr
    otp: str