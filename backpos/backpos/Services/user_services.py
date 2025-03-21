from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import check_password

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import DatabaseError

from backpos.Models.empresas_model import Empresa
from backpos.Models.usuarios_model import Usuario
from backpos.utilidades import generar_token


#LAFC [CREACIÓN DE SERVICIO PARA MOSTRAR USUARIOS COMUNES QUE NO SEAN ADMIN]
def mostrar_usuarios(identificador_admin):
    try:
        usuario = Usuario.objects.get(correo_usuario = identificador_admin)
        
        if usuario.validation_user is None:
            raise ValueError("Error: acceso denegado")
        
        all_users = Usuario.objects.exclude(status=0).values(
            "nombre_usuario", "alias_usuario","correo_usuario"
        )  
        
        return {
            "data": list(all_users) 
        }
    #EXCEPT PARA VALIDACION DE USUARIO
    except ObjectDoesNotExist:
        return {"codigo": 1, "error": "Ha ocurrido un error en el administrador."}
    except Exception as e:
        return {"codigo": 5, "error": f"Error inesperado: {str(e)}"}

    

def actualizar_usuario(identificador_admin, nombre_usuario_sub, usuario_sub, correo_usuario_sub, password_usuario_sub):
    #PRIMERO VALIDAR EL TOKEN PARA EL ADMIN
    try:
        usuario = Usuario.objects.get(correo_usuario = identificador_admin)
    except Usuario.DoesNotExist:
        return {"codigo": 1, "error": "Ha ocurrido un error con el administrador al momento de actualizar"}
    
    #AHORA SE HACE LA VALIDACION PARA ACTUALIZACIÓN DEL USUARIO