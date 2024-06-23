from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Comando(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    comando = models.TextField()
    fecha_creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre