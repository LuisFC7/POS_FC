from backpos.Models.usuarios_model import Usuario
from django.db import connection

def mostrar_datos_usuario(usuario_param):
    try:
        usuario = Usuario.objects.get(correo_usuario=usuario_param)
        
        if usuario.validation_user is None:
            raise ValueError("Error: acceso denegado")
        
        with connection.cursor() as cursor:
            cursor.callproc("sp_get_opciones_usuario", [usuario_param]) 
            resultados = cursor.fetchall()

       
        opciones_usuario = [
            {"Usuario": row[0], "Opcion": row[1], "Subopcion": row[2]} for row in resultados
        ]

     
        return {
            "datos": f"Bienvenido {usuario.nombre_usuario}",
            "opciones": opciones_usuario
        }

    except Usuario.DoesNotExist:
        return {"codigo": 1, "error": "Usuario no encontrado"}
    except ValueError as e:
        return {"codigo": 2, "error": str(e)}
