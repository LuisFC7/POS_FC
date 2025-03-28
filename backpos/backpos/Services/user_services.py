from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import check_password
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import DatabaseError
from django.core.exceptions import ValidationError

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
            "id_usuario", "nombre_usuario", "alias_usuario","correo_usuario","tipo_usuario"
        )  
        
        return {
            "data": list(all_users) 
        }
    #EXCEPT PARA VALIDACION DE USUARIO
    except ObjectDoesNotExist:
        return {"codigo": 1, "error": "Ha ocurrido un error en el administrador."}
    except Exception as e:
        return {"codigo": 5, "error": f"Error inesperado: {str(e)}"}

    
#SERVICIO PARA ACTUALIZAR UN USUARIO
def actualizar_usuario(identificador_admin, identificador_actualizar, nombre_usuario_up=None, usuario_up=None, correo_usuario_up=None, password_usuario_up=None, status_usuario_up=None, tipo_usuario_up=None):
    try:

        admin_existe = Usuario.objects.get(correo_usuario=identificador_admin)
        
        if not admin_existe:
            return {"codigo": 1, "error": "Ha ocurrido error en la sesión"}
        
        if admin_existe.validation_user is None:
            raise ValueError("Error: acceso denegado")

        updates = {}

        if nombre_usuario_up is not None:
            updates['nombre_usuario'] = nombre_usuario_up
        if usuario_up is not None:
            updates['alias_usuario'] = usuario_up
        if correo_usuario_up is not None:
            updates['correo_usuario'] = correo_usuario_up
        if password_usuario_up is not None:
            updates['password_usuario'] = make_password(password_usuario_up)
        if status_usuario_up is not None:
            updates['status'] = status_usuario_up
        if tipo_usuario_up is not None:
            updates['tipo_usuario'] = tipo_usuario_up

        Usuario.objects.filter(id_usuario=identificador_actualizar).update(**updates, fecha_actualizacion_usuario=datetime.now())
        return {"codigo": 0, "error": "Usuario actualizado correctamente"}

    except Usuario.DoesNotExist:
        return {"codigo": 2, "error": "Usuario no encontrado"}
    except ValidationError as e:
        return {"codigo": 3, "error": f"Datos inválidos: {str(e)}"}
    except ValueError as e:
        return {"codigo": 4, "error": str(e)}
    except Exception as e:
        return {"codigo": 5, "error": f"Error inesperado en el servidor: {str(e)}"}

