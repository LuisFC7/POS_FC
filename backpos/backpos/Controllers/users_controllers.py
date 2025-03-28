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
from backpos.Services.user_services import mostrar_usuarios, actualizar_usuario

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
    
    
@api_view(['POST'])
def actualizar_usuarios_controller(request):
    try:
        token = request.COOKIES.get('access_token')
        if not token:
            return Response({"codigo": 2, "error": "Acceso Denegado"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = verificar_token(token)
        
        if not payload:
            return Response({"codigo": 2, "error": "Acceso Denegado"}, status=status.HTTP_401_UNAUTHORIZED)

        user = payload.get("usuario_id")
        user_up_id = request.data.get("usuario_ac_id")
        user_up_nombre = request.data.get("usuario_ac_nombre")
        user_up_usuario = request.data.get("usuario_ac_usuario")
        user_up_correo = request.data.get("usuario_ac_correo")
        user_up_password = request.data.get("usuario_ac_password")
        user_up_status = request.data.get("usuario_ac_status")
        user_up_tipo = request.data.get("usuario_ac_tipo")

        data = actualizar_usuario(user, user_up_id, user_up_nombre, user_up_usuario, user_up_correo, user_up_password, user_up_status, user_up_tipo)

        error_mapping = {
            1: {"error": "Ha ocurrido error en la sesión", "status": status.HTTP_401_UNAUTHORIZED},
            2: {"error": "Error al actualizar usuario", "status": status.HTTP_404_NOT_FOUND},
            3: {"error": f"Datos inválidos: {data['error']}", "status": status.HTTP_400_BAD_REQUEST},
            4: {"error": "Acceso denegado", "status": status.HTTP_403_FORBIDDEN},
            5: {"error": "Error inesperado en el servidor", "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
        }

        if data.get("codigo") in error_mapping:
            error_info = error_mapping[data.get("codigo")]
            return Response({"codigo": data["codigo"], "error": error_info["error"]}, status=error_info["status"])

        return Response({"mensaje": "Usuario actualizado con éxito"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"codigo": 5, "error": "Error inesperado en el servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)