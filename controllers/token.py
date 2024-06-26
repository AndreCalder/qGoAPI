from datetime import datetime, timedelta

import jwt
from os import environ

class TokenController:
    
    def create_access_token(self, payload):
        return self._create_token(payload, environ.get('ACCESS_TOKEN_SECRET'), 60)
    
    def create_refresh_token(self, payload):
        return self._create_token(payload, environ.get('REFRESH_TOKEN_SECRET'), 180)
        
    def _create_token(self, payload: dict, secret_key: str, expiration: int):
        payload["iat"] = datetime.utcnow()
        payload["exp"] = datetime.utcnow()+timedelta(minutes=expiration)
        token = jwt.encode(
            payload, 
            secret_key, 
            algorithm="HS256"
        )
        return token
    
    def check_token(self, token: str):
        tokenData = jwt.decode(token, options={"verify_signature": False})
        return tokenData
        