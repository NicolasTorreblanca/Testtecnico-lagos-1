from django.db import models

# Create your models here.
# core/models.py

from django.db import models
# Note: JSONField is built-in to Django's ORM when using PostgreSQL
from django.contrib.postgres.fields import JSONField 

class Product(models.Model):
    # ... existing fields ...
    barcode = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    
    # --- NEW FIELDS FOR PRESENTATION ---
    brand = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True) 
    
    # Keep your existing fields
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sustainability_score = models.JSONField(default=dict)
    carbon_footprint = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return self.name

class ShoppingList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Optimization results
    is_optimized = models.BooleanField(default=False)
    total_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"List {self.id}"

class ListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    # Flag to identify items suggested by the optimization algorithm
    is_suggested_alternative = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in List {self.shopping_list.id}"