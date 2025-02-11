import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

def generar_token(usuario):

    tiempo_exp = datetime.now(timezone.utc) + timedelta(hours=1)
    
    payload = {
        'usuario': usuario.nombre_usuario,
        'exp': tiempo_exp
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS512')
    
    return token


def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS512'])
        return payload 
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None  