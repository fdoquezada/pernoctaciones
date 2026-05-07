from django.contrib import admin
from .models import Transportista, ViajePernoctacion

@admin.register(Transportista)
class TransportistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email_contacto')
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(ViajePernoctacion)
class ViajeAdmin(admin.ModelAdmin):
    # Columnas que verás en la lista
    list_display = ('patente', 'conductor', 'transportista', 'fecha_servicio', 'lugar_pernoctacion', 'link_respondido')
    
    # Filtros laterales para buscar rápido
    list_filter = ('fecha_servicio', 'link_respondido', 'transportista')
    
    # Buscador por patente o conductor
    search_fields = ('patente', 'conductor')
    
    # Para que no puedan editar el Token de seguridad manualmente
    readonly_fields = ('token_acceso',)
    
    # Ordenar por los más nuevos primero
    ordering = ('-fecha_servicio',)