# core/services/sustainability.py
import requests

from django.conf import settings

import requests
import json

def fetch_product_data(barcode=None, search_query=None):
    # 1. Obtener datos base de OpenFoodFacts
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    product_info = None
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 1:
                raw = data['product']
                name = raw.get('product_name', 'Unknown Product')
                category = raw.get('categories', 'General').split(',')[0]
                
                # INTENTO 1: Ver si OpenFoodFacts ya tiene la huella de carbono
                # (A veces viene en 'ecoscore_data' -> 'agribalyse' -> 'co2_total')
                carbon_footprint = raw.get('ecoscore_data', {}).get('agribalyse', {}).get('co2_total')
                
                # INTENTO 2: Si es None, usamos la API externa (Carbon Interface)
                if carbon_footprint is None:
                    # Estimamos el transporte de 1kg de este producto
                    carbon_footprint = fetch_carbon_interface_estimate(weight_kg=1.0)

                # --- NUEVA LÓGICA DE PRECIOS INTELIGENTE ---

                # Get Name and Category to decide the price
                name = raw.get('product_name', 'Unknown Product')
                category_tags = raw.get('categories_tags', []) # e.g. ["en:beverages", "en:sugary-snacks"]
                categories_str = " ".join(category_tags).lower() + " " + name.lower()
                
                # --- GENERATE DYNAMIC PRICE ---
                # It will change every time, but stay within a logical range
                price = generate_deterministic_price(categories_str)
                product_info = {
                    'barcode': barcode,
                    'name': name,
                    'brand': raw.get('brands', 'Marca Desconocida'),
                    'image_url': raw.get('image_front_url', ''),
                    'category': raw.get('categories', 'General').split(',')[0],
                    'price': price,  # <--- Precio generado matemáticamente
                    
                    # Huella de carbono: Si OpenFoodFacts no la tiene, generamos una proporcional al precio
                    # (Asumiendo que cosas más caras suelen procesarse más)
                    'carbon_footprint': raw.get('ecoscore_data', {}).get('agribalyse', {}).get('co2_total') or (price / 5000),
                    'sustainability_score': raw.get('ecoscore_grade', 'c').upper()
                }
    except Exception as e:
        print(f"Error fetching product: {e}")

    return product_info



# --- NUEVA FUNCIÓN: CARBON INTERFACE API ---
def fetch_carbon_interface_estimate(weight_kg=1.0):
    """
    Usa la API de Carbon Interface para estimar la huella de 
    transportar este producto.
    """
    url = "https://www.carboninterface.com/api/v1/estimates"
    
    # NECESITAS UNA API KEY (Es gratis registrarse en su web)
    # Si no tienes, esto fallará y usará el 'except'.
    headers = {
        "Authorization": "Bearer TU_API_KEY_DE_CARBON_INTERFACE",
        "Content-Type": "application/json"
    }

    # Payload: Estimamos un envío de 'weight_kg' por 100km en camión
    payload = {
        "type": "shipping",
        "weight_value": weight_kg,
        "weight_unit": "kg",
        "distance_value": 100, # Asumimos 100km de transporte promedio
        "distance_unit": "km",
        "transport_method": "truck"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=3)
        
        if response.status_code == 201: # 201 Created es éxito en esta API
            data = response.json()
            # La API devuelve 'carbon_kg'
            return data.get('data', {}).get('attributes', {}).get('carbon_kg', 0.5)
        else:
            print(f"Carbon API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error conectando a Carbon Interface: {e}")

    # FALLBACK: Si no hay API Key o falla, devolvemos un promedio seguro
    return 0.45 # 0.45 kg CO2 promedio

# --- FUNCIÓN GENERADORA DE PRECIOS ---
def generate_deterministic_price(barcode):
    """
    Genera un precio que parece real y es consistente para cada producto.
    No requiere API externa.
    """
    if not barcode:
        return 1990.0 # Precio por defecto si buscan por nombre
    
    # 1. Convertimos el código de barras en un número "semilla"
    # Esto asegura que el mismo código de barras SIEMPRE dé el mismo precio.
    semilla = int(hashlib.sha256(barcode.encode('utf-8')).hexdigest(), 16) % 10**8
    random.seed(semilla)
    
    # 2. Generamos un precio entre $800 y $15.000 CLP
    precio_base = random.randint(8, 150) * 100 # Genera múltiplos de 100 (ej: 800, 1500, 12300)
    
    # 3. Agregamos el típico "90" al final (ej: $1.990, $4.590) para que parezca de súper
    precio_final = precio_base + 90
    
    return float(precio_final)

# Agrega al final de core/services/sustainability.py

def suggest_alternative(product_obj):
    """
    Busca un producto más barato o más ecológico en la misma categoría.
    """
    from core.models import Product # Import local para evitar ciclos
    
    # Buscamos productos de la misma categoría
    alternatives = Product.objects.filter(
        category=product_obj.category
    ).exclude(id=product_obj.id) # Que no sea el mismo producto
    
    best_option = None
    
    for alt in alternatives:
        # Criterio: Si tiene menos CO2 y es más barato
        if alt.carbon_footprint < product_obj.carbon_footprint and alt.price < product_obj.price:
            best_option = alt
            break # Encontramos uno bueno, nos quedamos con ese
            
    if best_option:
        return {
            "found": True,
            "name": best_option.name,
            "reason": f"Ahorras ${product_obj.price - best_option.price} y generas menos CO2"
        }
    
    return {"found": False}