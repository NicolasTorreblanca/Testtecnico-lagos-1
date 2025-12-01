from django.core.management.base import BaseCommand
from core.models import Product, ShoppingList, ListItem
import random

class Command(BaseCommand):
    help = 'Puebla la base de datos con datos estratégicos para el Test Técnico'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Eliminando datos antiguos...'))
        ListItem.objects.all().delete()
        ShoppingList.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Creando Productos Estratégicos...')

        # --- ESTRATEGIA DE DATOS ---
        # Creamos pares de productos para probar el ALGORITMO DE SUSTITUCIÓN.
        # Caso A: Producto "Sucio" (Barato, Alto CO2)
        # Caso B: Producto "Limpio" (Más caro, Bajo CO2)
        
        products_data = [
            # CATEGORÍA: LECHES (Prueba de sustitución clásica)
            {
                "name": "Leche Entera Económica",
                "category": "Lácteos",
                "price": 990,
                "co2_footprint": 3.2, # Alto impacto (vacas)
                "sustainability_score": 30,
                "barcode": "780123456001"
            },
            {
                "name": "Leche de Almendras Bio",
                "category": "Lácteos",
                "price": 1890, # Más cara
                "co2_footprint": 0.7, # Bajo impacto
                "sustainability_score": 85,
                "barcode": "780123456002"
            },

            # CATEGORÍA: CARNES (Prueba de alto impacto en presupuesto y CO2)
            {
                "name": "Hamburguesa de Res (Pack 4)",
                "category": "Carnes",
                "price": 4500,
                "co2_footprint": 15.0, # Muy alto
                "sustainability_score": 10,
                "barcode": "780123456003"
            },
            {
                "name": "Hamburguesa NotBurger (Plant Based)",
                "category": "Carnes",
                "price": 4990, # Un poco más cara (Trade-off)
                "co2_footprint": 1.5, # Mucho menos CO2
                "sustainability_score": 90,
                "barcode": "780123456004"
            },
            {
                "name": "Carne Molida 5% Grasa",
                "category": "Carnes",
                "price": 6200,
                "co2_footprint": 12.0,
                "sustainability_score": 25,
                "barcode": "780123456005"
            },

            # CATEGORÍA: BEBIDAS (Prueba de productos baratos)
            {
                "name": "Bebida Cola 2L",
                "category": "Bebidas",
                "price": 1800,
                "co2_footprint": 0.5, # Plástico
                "sustainability_score": 20, # Mala salud (azúcar)
                "barcode": "780123456006"
            },
            {
                "name": "Agua Mineral Vidrio",
                "category": "Bebidas",
                "price": 1200, 
                "co2_footprint": 0.3, 
                "sustainability_score": 80,
                "barcode": "780123456007"
            },

            # CATEGORÍA: LIMPIEZA (Relleno para la lista)
            {
                "name": "Detergente Líquido",
                "category": "Limpieza",
                "price": 8990,
                "co2_footprint": 2.0,
                "sustainability_score": 40,
                "barcode": "780123456008"
            },
            {
                "name": "Detergente Eco-Friendly Recargable",
                "category": "Limpieza",
                "price": 9500,
                "co2_footprint": 0.8,
                "sustainability_score": 95,
                "barcode": "780123456009"
            }
        ]

        created_products = {}
        for p_data in products_data:
            prod = Product.objects.create(**p_data)
            created_products[prod.name] = prod
            self.stdout.write(f"- Creado: {prod.name}")

        # --- ESCENARIO DE PRUEBA ---
        self.stdout.write(self.style.SUCCESS('\nCreando Lista de Compras para DEMO...'))

        # Creamos una lista "Suecia" (No optimizada) con productos contaminantes.
        # Esto sirve para ejecutar el endpoint /optimize/ y ver la magia.
        demo_list = ShoppingList.objects.create(
            budget_limit=20000, # Presupuesto ajustado para forzar al algoritmo a pensar
            is_optimized=False
        )

        items_to_add = [
            ("Leche Entera Económica", 2), # El algoritmo debería sugerir cambiar a Almendras si el usuario prioriza eco
            ("Hamburguesa de Res (Pack 4)", 1), # Gran candidato a sustitución
            ("Bebida Cola 2L", 3),
            ("Detergente Líquido", 1)
        ]

        for prod_name, qty in items_to_add:
            if prod_name in created_products:
                ListItem.objects.create(
                    shopping_list=demo_list,
                    product=created_products[prod_name],
                    quantity=qty
                )

        self.stdout.write(self.style.SUCCESS(f'¡Listo! Lista creada con ID: {demo_list.id}'))
        self.stdout.write(self.style.SUCCESS(f'Presupuesto: ${demo_list.budget_limit}'))
        self.stdout.write(self.style.SUCCESS('Usa este ID para probar el endpoint POST /shopping-lists/{id}/optimize/'))