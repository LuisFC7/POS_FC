class UsuarioCrearDTO:
    def __init__(self, nombre_usuario, alias_usuario, correo_usuario, password_usuario):
        self.nombre_usuario = nombre_usuario
        self.alias_usuario = alias_usuario
        self.correo_usuario = correo_usuario
        self.password_usuario = password_usuario


    def __str__(self):
        return f"UsuarioCrearDTO(nombre_usuario={self.nombre_usuario}, alias_usuario={self.alias_usuario}, correo_usuario={self.correo_usuario})"
