from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    
    # --- Campos que faltaban y causaban el error ---
    brand = models.CharField(max_length=100, blank=True, null=True, default="Genérico")
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # --- Campos de Sostenibilidad ---
    co2_footprint = models.FloatField(default=0.0, help_text="CO2 en kg")
    sustainability_score = models.IntegerField(default=0, help_text="0-100 Score")
    is_fair_trade = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class ShoppingList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    # --- Campos calculados para el Dashboard [cite: 14] ---
    total_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_optimized = models.BooleanField(default=False)

class ListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    # --- Campos para el Algoritmo de Sustitución [cite: 61] ---
    is_suggested_alternative = models.BooleanField(default=False)
    substitution_reason = models.CharField(max_length=255, blank=True, null=True)
    original_product_name = models.CharField(max_length=255, blank=True, null=True)