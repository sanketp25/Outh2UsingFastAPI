from fastapi import Depends, FastAPI,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel

from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext

SECRET_KEY ="36a116464d89348c45e137e5d1577f1192f88bd624a92590320b8905331ee20"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
    "sanketp25":{
        "username" : "sanketp25",
        "full_name" : "Sanket Purohit",
        "email": "sanketpurohit@gmail.com",
        "hashed_password": "$2b$12$2bLVpx4CSY9v7j5KJ.bd1OIaXm3UD8k9uxasNBMJy1zdPaw3V9BNq",
        "disabled": False

    },
    "tim":{
        "username" : "tim",
        "full_name" : "Tim Howard",
        "email": "timhoward@gmail.com",
        "hashed_password": "$2b$12$2bLVpx4CSY9v7j5KJ.bd1OIaXm3UD8k9uxasNBMJy1zdPaw3V9BNq",
        "disabled": False

    }

}


# pwd = get_password_hash("1223")
# print("Password: ",pwd)

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str or None = None


class User(BaseModel):
    username:str
    email:str or None = None
    full_name: str or None = None
    disabled: bool or None = None 

class UserInDB(User):
    hashed_password:str

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")   

app = FastAPI()

#to verify if hash is correct
def verify_password(plain_password,hashed_password):    
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db,username:str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)    #** unpacks the data, that means it will give infor like name = sanket, etc
def authenicate_user(db,username:str,password:str):
    user = get_user(db,username)  
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user

def create_access_token(data:dict,expires_delta:timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15) 
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate Credentials", headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')  #this is key from the token created on line 105
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user(db,username=token_data.username)
    if user is None:
        raise credential_exception
    return user


async def get_current_active_user(current_user:UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive User")
    return current_user


@app.post('/token/',response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm = Depends()):

    print("Password entered during authorization:", form_data.password)
    print("Password hash: ",get_password_hash(form_data.password))
    #get username and password from the form
    user = authenicate_user(db,form_data.username,form_data.password)  
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Username or Password",headers={"WWW-Authenticate":"Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub':user.username},expires_delta=access_token_expires)
    return {'access_token':access_token,'token_type':'bearer'}  #these are the properties of token class


@app.get('/users/me/',response_model=User)
async def read_users_me(current_user:User = Depends(get_current_active_user)):
    return current_user

@app.get('/users/me/items')
async def read_own_items(current_user:User = Depends(get_current_active_user)):
    return [{'item_id':1,'owner':current_user}]


                             

# class Data(BaseModel):
#     name:str

# @app.post('/create')
# async def create(data:Data):
#     return {'data':data}    xw

# # @app.get("/test/")
# @app.get("/test/{item_id}")
# async def test(item_id:str, query: int = 1):
#     return {'hello':item_id}