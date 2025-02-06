from django.db import models

class Empresa(models.Model):
    
    nombre_empresa = models.CharField(max_length=255)
    razon_social_empresa = models.CharField(max_length=255)
    rfc_empresa = models.CharField(max_length=255, null=True, blank=True)
    telefono_empresa = models.CharField(max_length=255, null=True, blank=True)
    correo_electronico_empresa = models.EmailField(max_length=255)
    direccion_empresa = models.CharField(max_length=255)
    ciudad_empresa = models.IntegerField()
    id_estado_empresa = models.SmallIntegerField()
    codigo_postal_empresa = models.CharField(max_length=10)
    status_empresa = models.SmallIntegerField()

    
    def __str__(self):
        return self.nombre_empresa