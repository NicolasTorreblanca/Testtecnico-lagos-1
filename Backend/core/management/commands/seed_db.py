from django.core.management.base import BaseCommand
from core.models import Product, ShoppingList, ListItem

class Command(BaseCommand):
    help = 'Puebla la BD con productos REALES (KitKat, Nutella, Coke, etc.)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🧹 Limpiando base de datos antigua...'))
        ListItem.objects.all().delete()
        ShoppingList.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('🌱 Sembrando productos con TUS códigos reales...')

        products_data = [
            # --- CHOCOLATES Y DULCES ---
            {
                "name": "KitKat Chocolate Leche",
                "barcode": "8445290728791",
                "brand": "Nestlé",
                "category": "Snacks",
                "price": 1200,
                "co2_footprint": 0.8,
                "sustainability_score": 30, # Bajo: Aceite de palma/Azúcar
                "image_url": "https://images.openfoodfacts.org/images/products/844/529/072/8791/front_es.6.400.jpg",
                "description": "Oblea cubierta de chocolate."
            },
            {
                "name": "Nutella Crema de Avellanas",
                "barcode": "3017620422003",
                "brand": "Ferrero",
                "category": "Despensa",
                "price": 4500,
                "co2_footprint": 2.5, # Alto: Uso intensivo de recursos
                "sustainability_score": 20, 
                "image_url": "https://images.openfoodfacts.org/images/products/301/762/042/2003/front_fr.244.400.jpg",
                "description": "Crema de cacao y avellanas."
            },
            {
                "name": "Galletas Oreo Original",
                "barcode": "8410000810004",
                "brand": "Oreo",
                "category": "Snacks",
                "price": 1400,
                "co2_footprint": 1.1,
                "sustainability_score": 15, # Muy procesado
                "image_url": "https://images.openfoodfacts.org/images/products/841/000/081/0004/front_es.18.400.jpg",
                "description": "Galletas sandwich sabor chocolate."
            },

            # --- BEBIDAS (Comparativa Ideal: Zero vs Normal) ---
            {
                "name": "Coca-Cola Zero",
                "barcode": "5000112611762",
                "brand": "Coca-Cola",
                "category": "Bebidas",
                "price": 1800,
                "co2_footprint": 0.5, 
                "sustainability_score": 45, # Mejor que la normal
                "image_url": "https://images.openfoodfacts.org/images/products/500/011/261/1762/front_en.16.400.jpg",
                "description": "Bebida sin azúcar."
            },
            {
                "name": "Coca-Cola Sabor Original",
                "barcode": "5449000267412",
                "brand": "Coca-Cola",
                "category": "Bebidas",
                "price": 1800,
                "co2_footprint": 0.6,
                "sustainability_score": 10, # Peor score por azúcar
                "image_url": "https://images.openfoodfacts.org/images/products/544/900/026/7412/front_en.167.400.jpg",
                "description": "Bebida gaseosa azucarada."
            },
            {
                "name": "Cerveza Stella Artois",
                "barcode": "5014379008036",
                "brand": "Stella Artois",
                "category": "Alcohol",
                "price": 1100,
                "co2_footprint": 0.9, # Vidrio pesa en transporte
                "sustainability_score": 50,
                "image_url": "https://images.openfoodfacts.org/images/products/501/437/900/8036/front_en.13.400.jpg",
                "description": "Cerveza Lager Premium."
            },

            # --- SNACKS SALADOS ---
            {
                "name": "Papas Lays Corte Clásico",
                "barcode": "3168930169314",
                "brand": "Lays",
                "category": "Snacks",
                "price": 2200,
                "co2_footprint": 1.4,
                "sustainability_score": 35,
                "image_url": "https://images.openfoodfacts.org/images/products/316/893/016/9314/front_fr.45.400.jpg",
                "description": "Papas fritas con sal."
            },
            {
                "name": "Papas Lays (Variedad 2)",
                "barcode": "3168930171768",
                "brand": "Lays",
                "category": "Snacks",
                "price": 2300,
                "co2_footprint": 1.4,
                "sustainability_score": 35,
                "image_url": "https://images.openfoodfacts.org/images/products/316/893/017/1768/front_fr.4.400.jpg",
                "description": "Papas fritas saborizadas."
            },

            # --- SALSAS Y ADEREZOS ---
            {
                "name": "Ketchup Heinz",
                "barcode": "8715700110103",
                "brand": "Heinz",
                "category": "Despensa",
                "price": 2800,
                "co2_footprint": 1.2,
                "sustainability_score": 60,
                "image_url": "https://images.openfoodfacts.org/images/products/871/570/011/0103/front_en.35.400.jpg",
                "description": "Ketchup de tomate clásico."
            },
            {
                "name": "Mayonesa Kraft",
                "barcode": "0068100048728",
                "brand": "Kraft",
                "category": "Despensa",
                "price": 3200,
                "co2_footprint": 1.8,
                "sustainability_score": 40,
                "image_url": "https://images.openfoodfacts.org/images/products/006/810/004/8728/front_en.13.400.jpg",
                "description": "Mayonesa real."
            },

            # --- EL "ECO-HERO" (Agregado secretamente para que el algoritmo funcione) ---
            # Agregamos esto para que el algoritmo tenga ALGO contra qué comparar tus Lays
            {
                "name": "Chips de Manzana Deshidratada",
                "barcode": "1111222233334", # Código Ficticio de soporte
                "brand": "Tika",
                "category": "Snacks",
                "price": 2500,
                "co2_footprint": 0.3, # Muy bajo
                "sustainability_score": 95, # Excelente
                "image_url": "https://via.placeholder.com/150",
                "description": "Alternativa saludable."
            }
        ]

        # 1. Crear Productos
        for p_data in products_data:
            Product.objects.update_or_create(
                barcode=p_data['barcode'],
                defaults=p_data
            )
            self.stdout.write(f"- Procesado: {p_data['name']}")

        # 2. Crear Lista de Prueba (ID 1)
        self.stdout.write('\n🛒 Creando Lista Demo...')
        demo_list, _ = ShoppingList.objects.get_or_create(
            id=1,
            defaults={'budget_limit': 15000, 'is_optimized': False}
        )
        
        # Le ponemos productos "problemáticos" (Coca Normal y Lays) para que optimices
        coca_normal = Product.objects.get(barcode="5449000267412")
        lays = Product.objects.get(barcode="3168930169314")
        
        ListItem.objects.get_or_create(shopping_list=demo_list, product=coca_normal, defaults={'quantity': 2})
        ListItem.objects.get_or_create(shopping_list=demo_list, product=lays, defaults={'quantity': 1})

        self.stdout.write(self.style.SUCCESS('✅ ¡Base de datos lista con TUS productos!'))
        self.stdout.write(self.style.SUCCESS('Prueba escaneando tu Coca-Cola: 5449000267412'))