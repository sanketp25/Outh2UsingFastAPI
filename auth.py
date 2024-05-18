from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Leads,LeadState
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
SECRET_KEY = os.getenv("SECRET_KEY")   #paste your secret key
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")   

class LeadState(str,Enum):
    PENDING = 'PENDING'
    REACHED_OUT = 'REACHED_OUT'


class CreateLeads(BaseModel):
    #id: int
    username:str
    first_name: str
    last_name: str
    email: str
    password:str
    resume: str
    state:LeadState

class Token(BaseModel):
    access_token:str
    token_type:str   

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()   


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_leads(leads:CreateLeads, db:Session=Depends(get_db)):
    leads_model = Leads()
    leads_model.username = leads.username
    leads_model.first_name = leads.first_name
    leads_model.last_name = leads.last_name
    leads_model.email = leads.email
    leads_model.hashed_password = bcrypt_context.hash(leads.password)
    leads_model.resume = leads.resume
    leads_model.state = leads.state

    db.add(leads_model)
    db.commit()
    #return leads
@router.post('/token',response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    lead = authenticate_lead(form_data.username,form_data.password,db)  
    if not lead:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate User') 
    token = create_access_token(data={'sub':lead.username},expires_delta = timedelta(minutes=20)) 
    return {'access_token':token,'token_type':'bearer'}

def authenticate_lead(username:str,password:str,db):
    lead = db.query(Leads).filter(Leads.username == username).first()
    if not lead:
        return False
    if not bcrypt_context.verify(password,lead.hashed_password):
        return False
    return lead

def create_access_token(data: dict[str,any],expires_delta:timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15) 
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)],db:Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub') 
        if username is None:
            raise credential_exception
        #token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    lead = db.query(Leads).filter(Leads.username == username).first()
    if lead is None:
        raise credential_exception
    return lead