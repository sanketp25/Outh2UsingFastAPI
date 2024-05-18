from sqlalchemy import Column, Integer, String, Enum as SQLAEnum
#from sqlalchemy.ext.declarative import declarative_base
from database import Base
import enum

#Base = declarative_base()

class LeadState(enum.Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class Leads(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    resume = Column(String)
    hashed_password = Column(String,index=True)
    state = Column(SQLAEnum(LeadState), default=LeadState.PENDING)
