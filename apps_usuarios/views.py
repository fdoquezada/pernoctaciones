from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

class MiLoginView(LoginView):
    template_name = 'usuarios/login.html' # El archivo HTML que crearemos

class MiLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class MiLogoutView(LogoutView):
    # No necesita template_name si quieres que redirija directo al login
    # o si quieres usar el template de confirmación.
    pass # Apunta al nuevo archivo    