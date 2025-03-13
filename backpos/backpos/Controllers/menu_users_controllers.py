import re
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import JsonResponse
from backpos.Services.login_services import login
from backpos.Services.main_menu_services import mostrar_datos_usuario
from backpos.utilidades import verificar_token

menu_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'usuario_id': openapi.Schema(type=openapi.TYPE_STRING, description="Correo del usuario"),
        'nombre_usuario': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre completo del usuario"),
        'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje con los datos del usuario"),
    },
)

@swagger_auto_schema(
    method='get',
    responses={
        200: menu_schema,  # Respuesta exitosa con los datos del usuario
        401: "Token no proporcionado o inválido",  # Respuesta para token inválido
        500: "Error del servidor"  # Respuesta para error inesperado
    }
)
@api_view(['GET'])
def menu_principal_controller(request):
    if request.method == 'GET':
        try:
           
            token = request.COOKIES.get('access_token')

            if not token:
                return Response({"error": "Token no proporcionado"}, status=status.HTTP_401_UNAUTHORIZED)
            
            payload = verificar_token(token)
            if not payload:
                return Response({"error": "Token inválido o expirado"}, status=status.HTTP_401_UNAUTHORIZED)
           
            user = payload.get("usuario_id")
            
            data = mostrar_datos_usuario(user)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
