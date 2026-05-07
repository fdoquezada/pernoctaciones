from django.urls import path
from .views import declarar_pernoctacion

urlpatterns = [
    # El <uuid:token> es lo que hace que el link sea único y seguro
    path('declarar/<uuid:token>/', declarar_pernoctacion, name='declarar_pernoctacion'),
]