from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShoppingListViewSet, ProductScanView # <--- 1. ¿Está importada la vista?

router = DefaultRouter()
router.register(r'shopping-lists', ShoppingListViewSet, basename='shopping-list')

urlpatterns = [
    path('', include(router.urls)), # Rutas automáticas de las listas
    
    # --- ZONA DE PELIGRO ---
    # La línea de scan debe estar DENTRO de los corchetes de urlpatterns,
    # alineada a la misma altura que la línea de arriba.
    path('scan/', ProductScanView.as_view(), name='product-scan'), 
]