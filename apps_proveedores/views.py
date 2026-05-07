from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps_logistica.models import ViajePernoctacion

def declarar_pernoctacion(request, token):
    # Buscamos el viaje por el token único
    viaje = get_object_or_404(ViajePernoctacion, token_acceso=token)
    
    # Si ya respondió, no lo dejamos entrar de nuevo
    if viaje.link_respondido:
        return render(request, 'proveedores/ya_respondido.html')

    if request.method == 'POST':
        lugar = request.POST.get('lugar')
        # Guardamos la información
        viaje.lugar_pernoctacion = lugar
        viaje.link_respondido = True
        viaje.save()
        
        return render(request, 'proveedores/exito.html')

    return render(request, 'proveedores/formulario_externo.html', {'viaje': viaje})