from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

# from Models.usuarios_model import Usuario
from backpos.Models.usuarios_model import Usuario

def login():
    return "Hola"

def crear_usuario(nombre_usuario, alias_usuario, correo_usuario, password_usuario,id_empresa):

    usuario = Usuario(
        nombre_usuario = nombre_usuario,
        alias_usuario = alias_usuario,
        correo_usuario = correo_usuario,
        password_usuario = password_usuario,
        tipo_usuario = 1,
        status = 1,
        id_empresa_usuario = id_empresa
    )
    
    usuario.password_usuario = make_password(password_usuario)
    
    usuario.save()
    return 1