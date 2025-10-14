from passlib.context import CryptContext

pwd_cxt=CryptContext(schemes=['bcrypt'],deprecated='auto')

class Hash():
    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_cxt.verify(plain_password, hashed_password)


