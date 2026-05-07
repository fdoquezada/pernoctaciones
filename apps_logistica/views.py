from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

# Importaciones de tu aplicación (Estandarizadas)
from django.utils.timezone import make_aware
from .models import ViajePernoctacion, Transportista
from .forms import UploadExcelForm  # <--- Antes decía ExcelUploadForm, aquí estaba el error
from .utils import procesar_excel_tms, enviar_notificacion_transportista
from django.utils.timezone import make_aware
import datetime
import pytz


@login_required
def dashboard(request):
    hoy = timezone.now().date()
    print(f"DEBUG: Cargando dashboard para la fecha {hoy}")
    form = UploadExcelForm()
    
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                conteo = procesar_excel_tms(request.FILES['archivo_excel'])
                messages.success(request, f"Se cargaron {conteo} registros correctamente.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")

    viajes = ViajePernoctacion.objects.filter(fecha_servicio=hoy).order_by('-id')
    
    context = {
        'viajes': viajes,
        'form': form,
        'viewer_date': hoy,
        'hora_actual': timezone.now(),
    }
    return render(request, 'logistica/dashboard.html', context)

@login_required
def limpiar_jornada(request):
    if request.method == 'POST':
        hoy = timezone.now().date()
        viajes_hoy = ViajePernoctacion.objects.filter(fecha_servicio=hoy)
        cantidad = viajes_hoy.count()
        viajes_hoy.delete()
        
        messages.success(request, f"Se han eliminado {cantidad} registros de la jornada de hoy.")
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def notificar_transportistas_masivo(request):
    if request.method == 'POST':
        hoy = timezone.now().date()
        viajes = ViajePernoctacion.objects.filter(fecha_servicio=hoy, link_respondido=False)
        
        contador_enviados = 0
        for viaje in viajes:
            try:
                enviar_notificacion_transportista(viaje)
                contador_enviados += 1
            except Exception as e:
                print(f"Error enviando a {viaje.patente}: {e}")
        
        messages.success(request, f"Se han enviado {contador_enviados} notificaciones con éxito.")
        return redirect('dashboard')
    return redirect('dashboard')


@login_required
def registrar_llegada(request, viaje_id):
    viaje = get_object_or_404(ViajePernoctacion, id=viaje_id)
    if request.method == 'POST':
        hora_manual = request.POST.get('hora_manual')
        if hora_manual:
            # 1. Extraemos hora y minuto
            h, m = map(int, hora_manual.split(':'))
            
            # 2. Creamos la fecha/hora combinada
            dt_nave = datetime.datetime.combine(viaje.fecha_servicio, datetime.time(h, m))
            
            # 3. Forzamos la zona horaria de Chile directamente
            tz_chile = pytz.timezone('America/Santiago')
            viaje.hora_llegada = tz_chile.localize(dt_nave)
            viaje.save()
            
            messages.success(request, f"Llegada manual registrada: {hora_manual}")
        return redirect('dashboard')
    
    return render(request, 'logistica/registrar_hora.html', {'viaje': viaje, 'tipo': 'Llegada'})

@login_required
def registrar_salida(request, viaje_id):
    viaje = get_object_or_404(ViajePernoctacion, id=viaje_id)
    if request.method == 'POST':
        hora_manual = request.POST.get('hora_manual')
        if hora_manual:
            viaje.hora_salida = f"{viaje.fecha_servicio} {hora_manual}"
            viaje.save()
            messages.success(request, f"Salida manual registrada para {viaje.patente}")
        return redirect('dashboard')
    
    return render(request, 'logistica/registrar_hora.html', {'viaje': viaje, 'tipo': 'Salida'})


@login_required
def resetear_dia(request):
    # 1. Identificamos el día hoy en Chile
    hoy = timezone.localtime(timezone.now()).date()
    
    # 2. Buscamos los viajes de AGUNSA/Serlog de esta jornada
    viajes_hoy = ViajePernoctacion.objects.filter(fecha_servicio=hoy)
    cantidad = viajes_hoy.count()
    
    # 3. Los eliminamos
    viajes_hoy.delete()
    
    # 4. Mandamos un aviso que aparecerá en el Dashboard
    messages.warning(request, f"Se han eliminado {cantidad} registros de la jornada.")
    
    # 5. ¡ESTA ES LA CLAVE! No hay HTML, volvemos al dashboard
    return redirect('dashboard')