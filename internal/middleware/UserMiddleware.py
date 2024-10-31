from datetime import datetime, timedelta

from fastapi import HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import base64

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserMiddleware():

    SECRET_KEY: str = "SOIGjsd9os2osjASF3rft243637tnmdsLkVGSo4o030fOSNMp0e4r3i90NFSUrtALSVfG0342trSAVOGf3204tsLfv4t3he"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    def __init__(self):
        pass
    
    def get_current_user_id(self, request: Request, is_raise_exception: bool = False) -> int:
        """Получение user_id из JWT"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if token is None:
            if is_raise_exception:
                raise credentials_exception
            return 0
        token = token.replace("Bearer ", "")

        user_id: int = 0
        try:
            payload = jwt.decode(token, base64.b64encode(self.SECRET_KEY.encode()), algorithms=[self.ALGORITHM])
            user_id_str: str = payload.get("sub")
            if user_id_str is None:
                if is_raise_exception:
                    raise credentials_exception
                else:
                    return 0
            user_id = int(user_id_str)
        except JWTError:
            if is_raise_exception:
                raise credentials_exception
            else:
                return 0
        return user_id

    def create_access_token(self, response: Response, user_id: int) -> str:
        to_encode = {"sub": str(user_id)}
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        base64_bytes = base64.b64encode(self.SECRET_KEY.encode())
        encoded_jwt = jwt.encode(to_encode, base64_bytes, algorithm=self.ALGORITHM)
        return encoded_jwt