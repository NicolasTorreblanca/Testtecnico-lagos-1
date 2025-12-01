from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ProductSerializer, ScanSerializer # Import serializers
from .services import optimization, sustainability # <-- Ensure sustainability is imported

from .models import Product, ShoppingList, ListItem  # <--- CRITICAL: ADD ListItem HERE
from .serializers import ProductSerializer, ShoppingListSerializer, ScanSerializer
# Import the custom modules you created
from .services import optimization, sustainability 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScanSerializer
from .services.sustainability import SustainabilityService


# ------------------- Product Endpoints (Scanning & Data) -------------------

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Custom endpoint: POST /api/products/scan/
    @action(detail=False, methods=['post'], url_path='scan')
    def scan_product(self, request):
        serializer = ScanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        barcode = serializer.validated_data.get('barcode')
        search_query = serializer.validated_data.get('search_query')

        if not (barcode or search_query):
             return Response({"detail": "Provide a barcode or a search query."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. CHECK LOCAL DATABASE FIRST
        try:
            if barcode:
                product = Product.objects.get(barcode=barcode)
            else:
                product = Product.objects.get(name__icontains=search_query) 
            
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            # 2. IF NOT FOUND, FETCH DATA (La API externa ahora devuelve todo listo)
            product_data = sustainability.fetch_product_data(barcode=barcode, search_query=search_query)
            
            if not product_data:
                 return Response(
                    {"detail": f"Product '{barcode or search_query}' not found externally."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # --- CORRECCIÓN: YA NO LLAMAMOS A calculate_sustainability_score ---
            # El diccionario product_data ya trae el precio y el CO2 calculados.
            
            # 3. PREPARE DATA FOR LOCAL SAVE
            product_for_db = {
                'barcode': product_data.get('barcode', barcode),
                'name': product_data.get('name', search_query),
                'brand': product_data.get('brand'),          # Nuevo campo
                'image_url': product_data.get('image_url'),  # Nuevo campo
                'category': product_data.get('category', 'Uncategorized'),
                'price': product_data.get('price', 0.0),
                
                # El valor ya viene en kg desde nuestro servicio actualizado, no dividimos por 1000
                'carbon_footprint': product_data.get('carbon_footprint', 0.0), 
                
                # Guardamos la nota (A, B, C...) en el JSON
                'sustainability_score': {'grade': product_data.get('sustainability_score', 'Unknown')}, 
            }

            # 4. SAVE NEW PRODUCT TO DB
            new_product = Product.objects.create(**product_for_db)
            
            return Response(ProductSerializer(new_product).data, status=status.HTTP_201_CREATED)
    
    # GET /api/products/{id}/alternative/
    @action(detail=True, methods=['get'])
    def alternative(self, request, pk=None):
        product = self.get_object()
        # Llama a la lógica de sustitución que creamos
        suggestion = sustainability.suggest_alternative(product)
        return Response(suggestion, status=status.HTTP_200_OK)

# ------------------- Shopping List Endpoints (Optimization) -------------------
class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    # 1. NEW ACTION: Add a product to the list
    # POST /api/lists/{id}/add_item/
    @action(detail=True, methods=['post'], url_path='add_item')
    def add_item(self, request, pk=None):
        shopping_list = self.get_object()
        
        # Get data from the React POST request
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
            
            # Create or update the ListItem
            item, created = ListItem.objects.get_or_create(
                shopping_list=shopping_list,
                product=product,
                defaults={'quantity': quantity}
            )

            # If item already exists in list, just increase quantity
            if not created:
                item.quantity += quantity
                item.save()

            return Response(
                {"status": "Item added", "list_id": shopping_list.id, "product": product.name}, 
                status=status.HTTP_200_OK
            )

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    
    @action(detail=True, methods=['post'])
    def optimize(self, request, pk=None):
        shopping_list = self.get_object()
        
        try:
            optimized_results = optimization.run_knapsack_optimization(
                shopping_list=shopping_list,
                budget_limit=shopping_list.budget_limit 
            )
            
            shopping_list.is_optimized = True
            shopping_list.total_savings = optimized_results.get('total_savings', 0) 
            shopping_list.save()
            
            serializer = self.get_serializer(shopping_list)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Optimization failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # NUEVO: Endpoint para agregar items a la lista
    # POST /api/lists/{id}/add_item/
    @action(detail=True, methods=['post'], url_path='add_item')
    def add_item(self, request, pk=None):
        shopping_list = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
            # Crea o actualiza el item en la lista (evita duplicados)
            item, created = ListItem.objects.get_or_create(
                shopping_list=shopping_list, 
                product=product
            )
            
            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity
                
            item.save()
            return Response({"status": "Item added", "product": product.name}, status=200)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        """
        Endpoint para recibir un producto y agregarlo a la lista
        """
        shopping_list = self.get_object()
        
        # 1. Obtener datos del frontend
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "Falta product_id"}, status=400)

        # 2. Verificar que el producto exista
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "El producto no existe en la base de datos local"}, status=404)

        # 3. Crear o actualizar el item en la lista
        item, created = ListItem.objects.get_or_create(
            shopping_list=shopping_list,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # Si ya existía, sumamos la cantidad
            item.quantity += quantity
            item.save()

        # 4. Devolver la lista actualizada
        serializer = self.get_serializer(shopping_list)
        return Response(serializer.data)        


class ProductScanView(APIView):
    """
    Vista simple para manejar el escaneo/búsqueda de productos
    """
    def post(self, request):
        serializer = ScanSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener el término de búsqueda o código de barras
            query = serializer.validated_data.get('search_query') or serializer.validated_data.get('barcode')
            
            # Llamar a tu servicio (la lógica que ya creamos)
            service = SustainabilityService()
            product_data = service.fetch_product_data(barcode=query)
            
            if product_data:
                return Response(product_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)