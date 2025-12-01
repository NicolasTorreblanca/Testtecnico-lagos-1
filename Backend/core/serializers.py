# core/serializers.py

from rest_framework import serializers
from .models import Product, ShoppingList, ListItem

# -------------------------------------------------------------------------
# 1. Serializadores de Sostenibilidad y Métricas (Requisito: Scoring)
# -------------------------------------------------------------------------

class SustainabilityScoreSerializer(serializers.Serializer):
    """
    Serializa el desglose del impacto ambiental y social del producto.
    Cumple con el requisito: "Sistema de Scoring de Sostenibilidad".
    """
    co2_footprint = serializers.FloatField(help_text="Huella de carbono estimada en kg")
    sustainability_score = serializers.IntegerField(
        min_value=0, max_value=100, 
        help_text="Puntaje global calculado (0-100)"
    )
    packaging_recyclable = serializers.BooleanField(default=False)
    # Ejemplo de campo social (Fair Trade, etc.)
    social_impact_badge = serializers.CharField(required=False, allow_blank=True)

# -------------------------------------------------------------------------
# 2. Serializadores de Producto
# -------------------------------------------------------------------------

class ProductSerializer(serializers.ModelSerializer):
    # Anidamos las métricas para no "ensuciar" la data principal del producto
    # Esto asume que tu modelo Product tiene una property o relación 'metrics'
    metrics = SustainabilityScoreSerializer(source='*', read_only=True)

    class Meta:
        model = Product
        # Es mejor ser explícito con los campos en lugar de '__all__' para seguridad
        fields = [
            'id', 'name', 'price', 'barcode', 'category', 'brand',
            'image_url', 'metrics', 'description'
        ]

# -------------------------------------------------------------------------
# 3. Serializadores de Items y Sustitución (Requisito: Sustitución Inteligente)
# -------------------------------------------------------------------------

class SubstitutionDetailSerializer(serializers.Serializer):
    """
    Explica por qué se sustituyó un producto (Requisito: Bonus Sustitución [cite: 11]).
    """
    original_product_name = serializers.CharField()
    reason = serializers.CharField(help_text="Ej: 'Ahorro de precio' o 'Mejor impacto ecológico'")
    price_difference = serializers.DecimalField(max_digits=10, decimal_places=2)
    co2_saved = serializers.FloatField(required=False)

class ListItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    # Write-only: Para crear el item solo con el ID
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    
    # Campo anidado para detalles si hubo un cambio algorítmico
    substitution_details = SubstitutionDetailSerializer(read_only=True, required=False)

    class Meta:
        model = ListItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 
            'is_suggested_alternative', 'substitution_details'
        ]

# -------------------------------------------------------------------------
# 4. Serializadores de Lista de Compras (Requisito: Dashboard y Ahorros)
# -------------------------------------------------------------------------

class ShoppingListSerializer(serializers.ModelSerializer):
    items = ListItemSerializer(many=True, read_only=True)
    
    # Campos calculados para el "Dashboard de ahorros e impacto" [cite: 14]
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_co2_impact = serializers.FloatField(read_only=True)
    sustainability_grade = serializers.CharField(read_only=True, help_text="A, B, C based on score")

    class Meta:
        model = ShoppingList
        fields = [
            'id', 'created_at', 'budget_limit', 'is_optimized', 
            'total_savings', 'total_price', 'total_co2_impact', 
            'sustainability_grade', 'items'
        ]

# -------------------------------------------------------------------------
# 5. Serializadores de Entrada / Input (Requisito: Algoritmos)
# -------------------------------------------------------------------------

class OptimizationParamsSerializer(serializers.Serializer):
    """
    Input para el endpoint de optimización.
    Necesario para el "Algoritmo de Mochila Multi-objetivo".
    """
    shopping_list_id = serializers.IntegerField()
    budget_limit = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    # Pesos para el algoritmo multi-objetivo (0.0 a 1.0)
    # Permite al usuario decidir qué le importa más
    importance_price = serializers.FloatField(min_value=0.0, max_value=1.0, default=0.7)
    importance_sustainability = serializers.FloatField(min_value=0.0, max_value=1.0, default=0.3)
    
    allow_substitutions = serializers.BooleanField(default=True)

class ScanSerializer(serializers.Serializer):
    """
    Input para escáner [cite: 13]
    """
    barcode = serializers.CharField(max_length=50, required=False)
    search_query = serializers.CharField(max_length=255, required=False)
    
    def validate(self, data):
        if not data.get('barcode') and not data.get('search_query'):
            raise serializers.ValidationError("Debe proporcionar un código de barras o un término de búsqueda.")
        return data