from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.hashers import check_password

from backpos.Models.empresas_model import Empresa
from backpos.Models.usuarios_model import Usuario
from backpos.utilidades import generar_token

def login():
    return "Hola"

def crear_usuario(nombre_usuario, alias_usuario, correo_usuario, password_usuario):

    #PRIMERO VERIFICAR QUE EL CORREO Y EL USUARIO NO EXISTA EN LA DB
    usuario = Usuario(
        nombre_usuario = nombre_usuario,
        alias_usuario = alias_usuario,
        correo_usuario = correo_usuario,
        password_usuario = password_usuario,
        tipo_usuario = 1,
        status = 1,
    )
    
    search_correo = Usuario.objects.filter(correo_usuario = correo_usuario)
    search_usuario = Usuario.objects.filter(alias_usuario = alias_usuario)
   
    if search_correo.exists():  
        return 1
    if search_usuario.exists():
        return 2
    
    empresa = Empresa.objects.get(id_empresa = 1)
    usuario.id_empresa_usuario = empresa
    usuario.password_usuario = make_password(password_usuario)
    
    usuario.save()
    return 0

        
def login_usuario(identificador_user, password_user):
    
    try:
        usuario = Usuario.objects.get(correo_usuario = identificador_user)
    except Usuario.DoesNotExist:
        return {"codigo": 1, "error": "Usuario no encontrado"}
    

    if not check_password(password_user, usuario.password_usuario):
        return {"codigo": 1, "error": "Contraseña incorrecta"}
       
    access_token = generar_token(usuario)
    
    usuario.validation_user = access_token
    # usuario.save()
    usuario.save(update_fields=['validation_user'])
    
    return {
        'access_token': access_token,
        'codigo': 0
    }


        