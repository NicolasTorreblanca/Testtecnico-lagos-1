# core/services/optimization.py

from ..models import ShoppingList, ListItem, Product # Import necessary models

# core/services/optimization.py

def run_knapsack_optimization(shopping_list, budget_limit):
    """
    Algoritmo de Mochila (Knapsack Problem).
    Intenta maximizar el 'Puntaje Ecológico' respetando el presupuesto.
    """
    items = shopping_list.items.all()
    
    # 1. Preparar datos
    # Valor (Beneficio) = Inverso de huella de carbono (menos carbono es mejor)
    # Peso (Costo) = Precio del producto
    
    n = len(items)
    budget = int(budget_limit) # El algoritmo clásico trabaja mejor con enteros
    
    # precios y 'valores' ecológicos
    prices = [int(item.product.price) for item in items]
    
    # Valor: Le damos más puntos a productos con menos CO2
    # Si CO2 es 0.5kg, valor es alto. Si es 50kg, valor es bajo.
    eco_values = [int(100 / (item.product.carbon_footprint + 0.1)) for item in items]

    # 2. Matriz de Programación Dinámica (DP)
    # K[i][w] guardará el mejor valor ecológico posible con i items y presupuesto w
    K = [[0 for x in range(budget + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(budget + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif prices[i-1] <= w:
                # Decisión: ¿Incluimos el item o no?
                # Max entre (Valor de este item + mejor valor con el resto del dinero) vs (No incluirlo)
                K[i][w] = max(eco_values[i-1] + K[i-1][w-prices[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    # 3. Reconstruir la solución (¿Qué items elegimos?)
    res = K[n][budget]
    w = budget
    selected_items = []
    total_cost = 0

    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i-1][w]:
            continue
        else:
            # Este item fue seleccionado
            selected_items.append(items[i-1].product.name)
            total_cost += items[i-1].product.price
            
            res = res - eco_values[i-1]
            w = w - prices[i-1]

    # 4. Retornar resultados
    # Calculamos el ahorro como la diferencia entre el total original y el optimizado
    original_total = sum(item.product.price for item in items)
    
    return {
        'optimized_items': selected_items,
        'total_cost': total_cost,
        'total_savings': original_total - total_cost, # Ahorro simple (dinero no gastado)
        'eco_score_total': K[n][budget]
    }