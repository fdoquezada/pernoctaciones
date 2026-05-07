from django.urls import path
from .views import dashboard, limpiar_jornada, notificar_transportistas_masivo, registrar_llegada, registrar_salida


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('limpiar/', limpiar_jornada, name='resetear_dia'),
    path('notificar-masivo/', notificar_transportistas_masivo, name='notificar_masivo'),
    path('llegada/<int:viaje_id>/', registrar_llegada, name='registrar_llegada'),
    path('salida/<int:viaje_id>/', registrar_salida, name='registrar_salida')
    
# ] Agrega aquí otras URLs de logística si es necesario
]