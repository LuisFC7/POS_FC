import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import JsonResponse
from backpos.Services.login_services import login
from backpos.Services.login_services import crear_usuario, login_usuario
from backpos.utilidades import verificar_token


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
    request_body=usuario_schema,  
    responses={201: "Usuario registrado exitosamente", 400: "Error en la validación", 500: "Error del servidor"}
)
@api_view(['POST'])
def registrar_usuario_controller(request):
    
    if request.method == 'POST':
        try:
            # Obtén el token desde la cabecera 'Authorization'
            print(request.headers)
            token = request.headers.get('Authorization')

            # Verifica que el token esté presente
            if not token:
                return Response({"error": "Token no proporcionado"}, status=status.HTTP_401_UNAUTHORIZED)

            # Si el token tiene el prefijo 'Bearer ', lo extraemos
            if " " in token:
                token = token.split(" ")[1]  # Extrae solo el token sin el prefijo 'Bearer'

            # Verifica si el token es válido
            payload = verificar_token(token)
            if not payload:
                return Response({"error": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)

            # Si el token es válido, continúa con la creación del usuario
            nombre_usuario = request.data.get('nombre')
            alias_usuario = request.data.get('usuario')
            correo_usuario = request.data.get('correo')
            password_usuario = request.data.get('password')

            # Validaciones de los campos
            password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~])[A-Za-z\d!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~]{8,}$'
            
            if not isinstance(nombre_usuario, str) or not nombre_usuario:
                return Response({"error": "El nombre debe estar en formato texto."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(alias_usuario, str) or not alias_usuario:
                return Response({"error": "El alias debe estar en formato texto."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(correo_usuario, str) or not correo_usuario:
                return Response({"error": "El correo debe estar en formato texto."}, status=status.HTTP_400_BAD_REQUEST)

            if not re.match(password_regex, password_usuario):
                return Response({"error": "La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, un dígito y un carácter especial."}, status=status.HTTP_400_BAD_REQUEST)

            # Suponiendo que tienes una función para crear el usuario
            code_servicio = crear_usuario(nombre_usuario, alias_usuario, correo_usuario, password_usuario)

            if code_servicio == 1:
                return Response({"error": "El correo ingresado ya existe, intente con otro."}, status=status.HTTP_409_CONFLICT)

            if code_servicio == 2:
                return Response({"error": "El usuario ingresado ya existe, intente con otro."}, status=status.HTTP_409_CONFLICT)

            return Response({"message": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# SERVICIO PARA INICIO DE SESIÓN
request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['usuario', 'password'],
    properties={
        'usuario': openapi.Schema(type=openapi.TYPE_STRING, description="Correo o alias del usuario"),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description="Contraseña del usuario"),
    },
)

response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de éxito"),
        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Token de acceso"),
        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Token de refresco"),
    },
)

error_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de error"),
    },
)

@swagger_auto_schema(
    method='post',
    operation_summary="Autenticación de usuario",
    operation_description="Este endpoint permite autenticar a un usuario y obtener un token JWT.",
    request_body=request_schema,
    responses={
        200: response_schema,
        400: error_schema,
        401: error_schema,
        500: error_schema
    },
)
@api_view(['POST'])
def login_usuario_controller(request):
    if request.method == 'POST':
        try:
            identificador = request.data.get('usuario')
            password_usuario = request.data.get('password')

            if not isinstance(identificador, str) or identificador is None:
                return Response({"error": "Debe ingresarse el correo o usuario."}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(password_usuario, str) or password_usuario is None:
                return Response({"error": "Debe ingresar la contraseña"}, status=status.HTTP_400_BAD_REQUEST)

            response_servicio = login_usuario(identificador, password_usuario)

            access_token = response_servicio.get('access_token')
            codigo = response_servicio.get('codigo')

            if codigo == 1:
                return Response({"error": "Credenciales incorrectas o usuario inexistente"}, status=status.HTTP_401_UNAUTHORIZED)

            # Crear respuesta sin token en el cuerpo
            response = Response(
                {"mensaje": "Inicio de sesión exitoso"},
                status=status.HTTP_200_OK
            )

            # Configurar cookie segura con el token
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,  # No accesible por JavaScript (protege contra XSS)
                secure=True,  # Solo se envía en HTTPS
                samesite="Strict",  # Previene CSRF en la mayoría de los casos
                max_age=3600  # Expira en 1 hora
            )

            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)