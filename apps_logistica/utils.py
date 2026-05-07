import pandas as pd
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import ViajePernoctacion, Transportista

def enviar_notificacion_transportista(viaje):
    # Construimos el link completo (Ajusta el dominio cuando lo subas a Render)
    # Por ahora usamos localhost para tus pruebas
    dominio = "http://127.0.0.1:8000"
    url_declaracion = reverse('declarar_pernoctacion', kwargs={'token': viaje.token_acceso})
    link_final = f"{dominio}{url_declaracion}"

    asunto = f"Control Pernoctación - Equipo {viaje.patente}"
    
    mensaje_texto = f"""
    Estimado Transportista,
    
    Se ha registrado el servicio del equipo {viaje.patente} conducido por {viaje.conductor}.
    Para cumplir con el protocolo de descanso, por favor declare el lugar de pernoctación en el siguiente link:
    
    {link_final}
    
    Atentamente,
    Centro de Control Operativo - Pernoctaciones
    """
    
    # Solo enviamos si el transportista tiene un mail configurado
    if viaje.transportista.email_contacto and viaje.transportista.email_contacto != 'pendiente@correo.com':
        send_mail(
            asunto,
            mensaje_texto,
            settings.EMAIL_HOST_USER,
            [viaje.transportista.email_contacto],
            fail_silently=False,
        )
        
def procesar_excel_tms(archivo):
    df = pd.read_excel(archivo)
    viajes_creados = 0
    
    for index, row in df.iterrows():
        # Definimos las variables con los nombres exactos del Excel de AGUNSA
        nombre_transporte = str(row['Proveedor TTE']).strip()
        nombre_chofer = str(row['Chofer']).strip()
        patente_equipo = str(row['Patente Principal']).strip() # <--- AQUÍ SE DEFINE
        
        if patente_equipo == 'nan' or nombre_transporte == 'nan':
            continue

        # 1. Buscamos o creamos el Transportista
        obj_transp, created = Transportista.objects.get_or_create(
            nombre=nombre_transporte,
            defaults={'email_contacto': 'pendiente@correo.com'}
        )
        
        # 2. Creamos el Viaje (aquí usamos patente_equipo definida arriba)
        nuevo_viaje = ViajePernoctacion.objects.create(
            patente=patente_equipo,
            conductor=nombre_chofer,
            transportista=obj_transp,
            fecha_servicio=timezone.now().date()
        )
        
        # 3. Intentamos enviar el mail
        try:
            enviar_notificacion_transportista(nuevo_viaje)
        except Exception as e:
            print(f"Error enviando mail: {e}")
            
        viajes_creados += 1
        
    return viajes_creados    