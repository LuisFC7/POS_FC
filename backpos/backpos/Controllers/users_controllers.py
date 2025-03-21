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
from backpos.Services.user_services import mostrar_usuarios

@api_view(['GET'])
def mostrar_usuarios_controller(request):
    """ Controlador para obtener los usuarios. """
    try:
        
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({"codigo": 2, "error": "Acceso Denegado"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = verificar_token(token)
        if not payload:
            return Response({"codigo": 2, "error": "Acceso Denegado"}, status=status.HTTP_401_UNAUTHORIZED)

        user = payload.get("usuario_id")

        data = mostrar_usuarios(user)

        if "codigo" in data:
            status_code = status.HTTP_404_NOT_FOUND if data["codigo"] == 1 else status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(data, status=status_code)

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"codigo": 5, "error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)