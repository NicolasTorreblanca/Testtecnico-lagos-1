from django.urls import path, include
from rest_framework.routers import DefaultRouter
# This import works here because views.py is inside the same 'core' folder
from .views import ProductViewSet, ShoppingListViewSet 

router = DefaultRouter()

# Register your ViewSets
router.register(r'products', ProductViewSet, basename='product')
router.register(r'lists', ShoppingListViewSet, basename='list')

urlpatterns = router.urls