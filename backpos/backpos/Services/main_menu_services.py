from backpos.Models.usuarios_model import Usuario

def mostrar_datos_usuario(usuario):
    try:
        usuario = Usuario.objects.get(correo_usuario = usuario)
    except Usuario.DoesNotExist:
        return {"codigo": 1, "error": "Usuario no encontrado"}
    
    return {
        'datos': f"Bienvenido {usuario.nombre_usuario}" 
    }