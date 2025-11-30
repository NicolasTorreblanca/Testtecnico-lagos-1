# core/serializers.py

from rest_framework import serializers
from .models import Product, ShoppingList, ListItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' # Include all fields from the Product model

# Serializer for items within a list
class ListItemSerializer(serializers.ModelSerializer):
    # Read-only field to display product details when viewing a list
    product = ProductSerializer(read_only=True) 
    
    # Write-only field used when creating a list item (requires only product ID)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = ListItem
        fields = ['id', 'product', 'product_id', 'quantity', 'is_suggested_alternative']

# Main serializer for ShoppingList
class ShoppingListSerializer(serializers.ModelSerializer):
    # This ensures that when you retrieve a list, it includes all its items (nested data)
    items = ListItemSerializer(many=True, read_only=True) 

    class Meta:
        model = ShoppingList
        fields = ['id', 'created_at', 'budget_limit', 'is_optimized', 'total_savings', 'items']
        
# Input serializer for the scan endpoint
class ScanSerializer(serializers.Serializer):
    barcode = serializers.CharField(max_length=50, required=False)
    search_query = serializers.CharField(max_length=255, required=False)