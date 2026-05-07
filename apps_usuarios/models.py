from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    # Definimos los roles para los turnos
    ROLES = (
        ('admin', 'Administrador (Fernando)'),
        ('monitor', 'Monitor de Turno'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='monitor')
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"