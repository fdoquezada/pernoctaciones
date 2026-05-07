from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class Transportista(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    email_contacto = models.EmailField()

    def __str__(self):
        return self.nombre

class ViajePernoctacion(models.Model):
    # Datos del Servicio
    patente = models.CharField(max_length=10)
    conductor = models.CharField(max_length=200)
    transportista = models.ForeignKey(Transportista, on_delete=models.CASCADE)
    fecha_servicio = models.DateField(default=timezone.now)
    
    # Datos de Pernoctación (llenados por el transportista o monitor)
    lugar_pernoctacion = models.CharField(max_length=255, null=True, blank=True)
    hora_llegada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    
    # Gestión del Link Seguro
    token_acceso = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    link_respondido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Viaje de Pernoctación"
        verbose_name_plural = "Viajes de Pernoctación"

    def __str__(self):
        return f"{self.patente} - {self.fecha_servicio}"

    # --- LÓGICA DEL SEMÁFORO ---

@property
def cumple_llegada(self):
    if not self.hora_llegada:
        return False
    
    # Convertimos la hora almacenada a la hora local de Chile antes de sacar la fecha
    llegada_chile = timezone.localtime(self.hora_llegada)
    
    # Si la fecha de llegada (en Chile) es el mismo día del servicio: CUMPLE
    return llegada_chile.date() <= self.fecha_servicio

@property
def cumple_8_horas(self):
        """
        Verifica que el descanso sea de al menos 8 horas entre llegada y salida.
        """
        if self.hora_llegada and self.hora_salida:
            diferencia = self.hora_salida - self.hora_llegada
            return diferencia >= timedelta(hours=8)
        return False