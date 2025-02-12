import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from backpos.settings import SECRET_KEY


def generar_token(usuario):
   
    tiempo_exp = datetime.now(timezone.utc) + timedelta(hours=1)
    
    payload = {
        "usuario_id": usuario.id_usuario,  
        "nombre_usuario": usuario.nombre_usuario,  
        "exp": tiempo_exp  
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS512")
    
    return token

def verificar_token(token):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS512"])
        return payload  
    except jwt.ExpiredSignatureError:
        return {"error": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"error": "Token inválido"}
