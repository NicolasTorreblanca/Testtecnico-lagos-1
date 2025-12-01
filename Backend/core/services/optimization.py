# core/services/optimization.py
from decimal import Decimal
from ..models import ShoppingList, ListItem

class OptimizationService:
    """
    Servicio que implementa el Algoritmo de Mochila Multi-objetivo.
    """

    def run_optimization(self, shopping_list, budget_limit, weight_price=0.5, weight_eco=0.5):
        """
        Ejecuta Knapsack Problem (0/1) considerando DOS objetivos:
        1. Minimizar gasto (o maximizar valor por dinero).
        2. Maximizar sustentabilidad.
        
        weight_price (0.0 - 1.0): Qué tanto le importa el ahorro al usuario.
        weight_eco (0.0 - 1.0): Qué tanto le importa el planeta.
        """
        items = list(shopping_list.items.all()) # Convertir QuerySet a lista
        n = len(items)
        budget = int(budget_limit)
        
        # Validación de seguridad
        if n == 0 or budget <= 0:
            return {'optimized_items': [], 'total_savings': 0}

        # 1. PREPARACIÓN DE VECTORES
        prices = [int(item.product.price) for item in items]
        
        # Aquí está la magia "Multi-objetivo":
        # Calculamos el "Valor" (Utility) de cada producto combinando sus atributos.
        # Un producto es valioso si: Es barato (para el usuario ahorrador) Y es ecológico.
        values = []
        for item in items:
            # Normalizamos precio inverso (0-100 aprox): Más barato = Más puntos
            # Asumimos un precio maximo de referencia de 20000 para normalizar
            price_score = max(0, 100 - (item.product.price / 200)) 
            
            # Score ecológico (ya viene calculado 0-100 en el modelo o se calcula al vuelo)
            eco_score = getattr(item.product, 'sustainability_score', 50) 
            
            # COMBINACIÓN PONDERADA
            combined_value = (price_score * weight_price) + (eco_score * weight_eco)
            values.append(int(combined_value))

        # 2. ALGORITMO KNAPSACK (Programación Dinámica)
        # K[i][w] = Máximo valor conseguido con primeros i items y peso w
        K = [[0 for x in range(budget + 1)] for x in range(n + 1)]

        for i in range(n + 1):
            for w in range(budget + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif prices[i-1] <= w:
                    # Decisión: Max(Incluir item, No incluir item)
                    include_val = values[i-1] + K[i-1][w-prices[i-1]]
                    exclude_val = K[i-1][w]
                    K[i][w] = max(include_val, exclude_val)
                else:
                    K[i][w] = K[i-1][w]

        # 3. RECONSTRUCCIÓN (Backtracking para ver qué items ganaron)
        res = K[n][budget]
        w = budget
        selected_ids = []
        total_cost = 0
        original_cost = sum(prices)

        for i in range(n, 0, -1):
            if res <= 0: break
            if res == K[i-1][w]:
                continue
            else:
                # Item seleccionado
                item = items[i-1]
                selected_ids.append(item.id)
                total_cost += item.product.price
                
                res = res - values[i-1]
                w = w - prices[i-1]

        # 4. RESULTADO
        # En una app real, marcaríamos los items como "seleccionados" en la DB.
        return {
            'kept_items_count': len(selected_ids),
            'original_cost': original_cost,
            'optimized_cost': total_cost,
            'total_savings': original_cost - total_cost,
            'eco_utility_score': K[n][budget],
            'selected_item_ids': selected_ids
        }