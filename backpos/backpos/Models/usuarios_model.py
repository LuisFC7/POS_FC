from django.db import models
from .empresas_model import Empresa


class Usuario(models.Model): 
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=255)
    alias_usuario = models.CharField(max_length=100, unique=True)
    correo_usuario = models.EmailField(max_length=255, unique=True)
    password_usuario = models.CharField(max_length=255)  
    tipo_usuario = models.SmallIntegerField()
    status = models.SmallIntegerField()
    id_empresa_usuario = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column="id_empresa_usuario")  # Usa el nombre correcto

    class Meta:
        db_table = "usuarios"
        
    def __str__(self):
        return self.nombre_usuario

