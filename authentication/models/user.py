import uuid
import sqlalchemy as db
from datetime import datetime,timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(String,nullable=False)
    first_name = Column(String,nullable=True)
    last_name = Column(String,nullable=True)
    email = Column(String,index=True,nullable=False)
    phone_number = Column(String,index=True,nullable=False)
    password =Column(String,nullable=True)
    dt_created= Column(DateTime, default=datetime.utcnow)

class OTP(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    otp_code=Column(String(length=6))
    expire_at= Column(DateTime, default=datetime.now()+timedelta(minutes=30))
    created_at=Column(DateTime,default=datetime.now())