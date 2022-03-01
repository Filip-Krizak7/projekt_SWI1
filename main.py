import fastapi
import schemas

tags_metadata = [
    {
        "name": "Booking reservations",
        "description": "Api used to book your hotel reservations.",
    }
]

app = fastapi.FastAPI(
    title="Booking service",
    description="something special",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2:scheme = OAuth2PasswordBearer(tokenUrl="token")
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username.__eq__(#username from database):
        user_dict = {
            "username": #username,
            "hashed_password": #hashedpasswd from database,
        }
        return schemas.UserInDB(**user_dict)
    return None
        
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
        
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
            }
    try:
        payload = jwt.decode(
            token,
            key=#token_bearer,
            algorithms=[#algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError as token_error:
        raise credentials_exception from token_error
    user = get_user(username=token_data.username)
    if user is None:
        raise credential_exception
    return user
