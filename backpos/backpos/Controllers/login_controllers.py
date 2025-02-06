import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import JsonResponse
from backpos.Services.login_services import login
from backpos.Services.login_services import crear_usuario




@api_view(['GET'])
def login_controller(request):
    mensaje = login()
    return Response({"mensaje": mensaje})



usuario_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['nombre', 'usuario', 'correo', 'password'],
    properties={
        'nombre': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre completo del usuario"),
        'usuario': openapi.Schema(type=openapi.TYPE_STRING, description="Alias o nombre de usuario"),
        'correo': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description="Correo electrónico del usuario"),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description="Contraseña segura con mínimo 8 caracteres, una mayúscula, un número y un carácter especial"),
    },
)

@swagger_auto_schema(
    method='post',
    request_body=usuario_schema,  # Indica a Swagger qué datos espera recibir
    responses={201: "Usuario registrado exitosamente", 400: "Error en la validación", 500: "Error del servidor"}
)
@api_view(['POST'])
def registrar_usuario_controller(request):
    if request.method == 'POST':
        try:
            nombre_usuario = request.data.get('nombre')
            alias_usuario = request.data.get('usuario')
            correo_usuario = request.data.get('correo')
            password_usuario = request.data.get('password')
            
            password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~])[A-Za-z\d!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~]{8,}$'
            
            if not isinstance(nombre_usuario, str) or nombre_usuario is None:
                return Response({"Error": "El correo proporcionado debe estar en formato texto."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not isinstance(alias_usuario, str) or alias_usuario is None:
                return Response({"Error": "El correo proporcionado debe estar en formato texto."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not isinstance(correo_usuario, str) or correo_usuario is None:
                return Response({"Error": "El correo proporcionado debe estar en formato texto."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not re.match(password_regex, password_usuario):
                return Response({"error": "La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, un dígito y un carácter especial."}, status=status.HTTP_400_BAD_REQUEST)
            
            crear_usuario(nombre_usuario, alias_usuario, correo_usuario, password_usuario,1)
            
            return Response({"message": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
