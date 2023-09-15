from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    'dimas': {
        'id': '123dfkdfk',
        'nama': 'Dimas Fitrio',
        'email': 'dimasfk@example.com',
        'phone': '08123456789',
        'address': 'Jalanin aja dulu',
        'username': 'dimas',
        'password': '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
        'status': True,
        'createdTime': datetime(2000, 12, 25),
        'createdBy': 'dimas',
        'updatedTime': datetime.now(),
        'updatedBy': 'dimas',
    }
}

class User(BaseModel):
    id: str
    nama: str
    email: str | None = None
    phone: str
    address: str
    username: str
    password: str
    status: bool
    createdTime: datetime
    createdBy: str
    updatedTime: datetime
    updatedBy: str

class Token(BaseModel):
    status_code: int
    message: str
    access_token: str
    data: User

class TokenData(BaseModel):
    username: str | None = None
    userId: str
    nama: str
    email: str
    phone: str
    exp: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.status:
        raise HTTPException(status_code=400, detail='User tidak aktif')
    return current_user

@app.post('/login', response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = get_user(fake_users_db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User tidak ditemukan',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User tidak aktif',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Password salah',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'status_code':200, 'message': 'Berhasil Login', 'access_token': access_token, 'data': user}

# @app.post('/token', response_model=Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Incorrect username or password',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={'sub': user.username}, expires_delta=access_token_expires
#     )
#     return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/user/', response_model=User)
async def read_user(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


# @app.get('/users/me/items/')
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{'item_id': 'Foo', 'owner': current_user.username}]
