# 🌱 LiquiVerde - Plataforma de Retail Inteligente

> **Prueba Técnica Software Engineer I** - Grupo Lagos

Una aplicación Full-Stack diseñada para optimizar decisiones de compra, equilibrando el presupuesto del usuario con el impacto ambiental (huella de carbono) mediante algoritmos de optimización multi-objetivo.

---

## 📋 Tabla de Contenidos
1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Arquitectura y Algoritmos](#arquitectura-y-algoritmos)
4. [Instalación y Despliegue](#instalación-y-despliegue)
5. [Uso de la Aplicación](#uso-de-la-aplicación)
6. [Declaración de Uso de IA](#declaración-de-uso-de-ia)

---

## 📖 Descripción del Proyecto
Este sistema permite a los usuarios:
* **Escanear/Buscar productos** reales utilizando una base de datos local pre-cargada con códigos EAN-13 reales (Chile/Latam).
* **Generar listas de compras** y optimizarlas automáticamente.
* **Algoritmo Multi-Criterio:** El usuario define qué tanto le importa el "Ahorro" vs. el "Planeta", y el sistema reasigna los productos (ej: cambiando una Coca-Cola normal por una Zero o una Leche de Vaca por una Vegetal) para maximizar el puntaje.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.10+ | Django 5 | Django REST Framework (DRF)
* **Frontend:** React 18 | Vite | Axios | CSS3
* **Base de Datos:** PostgreSQL
* **APIs Externas:** OpenFoodFacts (Integrado en lógica de semillas)
* **Herramientas:** Git, Postman

---

## 🧠 Arquitectura y Algoritmos

### 1. Algoritmo de Mochila Multi-Objetivo (Knapsack)
Se implementó una variación del problema de la mochila (Knapsack Problem) utilizando **Programación Dinámica**.
* **Función de Valor:** `V = (w1 * Ahorro) + (w2 * Score_Sostenibilidad)`
* **Restricción:** El costo total no debe superar el `budget_limit`.
* **Lógica:** El algoritmo evalúa cada producto de la lista y sus posibles sustitutos para maximizar el valor `V` sin romper el presupuesto.

### 2. Scoring de Sostenibilidad
Cada producto tiene un `sustainability_score` (0-100) calculado basándose en:
* Huella de Carbono (kg CO2e).
* Sellos nutricionales y tipo de envase.
* Datos normalizados para facilitar la comparación entre categorías.

---

## 🚀 Instalación y Despliegue

Sigue estos pasos para ejecutar el proyecto localmente.

### Pre-requisitos
* Python 3.10+
* Node.js 16+
* PostgreSQL instalado y corriendo.

### Paso 1: Configuración del Backend (Django)

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/NicolasTorreblanca/Testtecnico-lagos-1.git
    cd Testtecnico-lagos-1/Backend
    ```

2.  **Crear entorno virtual e instalar dependencias:**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  **Configurar Base de Datos:**
    * Asegúrate de tener una BD en PostgreSQL llamada `liquiverde_db`.
    * Verifica las credenciales en `core/settings.py` o crea un archivo `.env`.

4.  **Migraciones y Datos Semilla (Importante):**
    Para que el escáner funcione con productos reales, ejecuta el script de población:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py seed_db  # <--- ¡CRUCIAL! Carga productos reales (Coca-Cola, Lays, etc.)
    ```

5.  **Correr el servidor:**
    ```bash
    python manage.py runserver
    ```
    *El backend estará disponible en `http://127.0.0.1:8000/`*

### Paso 2: Configuración del Frontend (React)

1.  **Instalar dependencias:**
    Abrir una nueva terminal y navegar a la carpeta del frontend:
    ```bash
    cd Frontend
    npm install
    ```

2.  **Ejecutar cliente de desarrollo:**
    ```bash
    npm run dev
    ```
    *El frontend estará disponible en `http://localhost:5173/` (o puerto similar).*

---

## 📱 Uso de la Aplicación

1.  **Escáner:** Ve a la pestaña "Escáner" e ingresa un código real (ej: `7801610001306` para Coca-Cola Original).
2.  **Agregar:** Presiona "Agregar a Lista".
3.  **Optimizador:** Ve a la pestaña principal. Verás tus productos.
4.  **Jugar con los Pesos:** Mueve el slider hacia "Eco" o "Ahorro" y presiona **"Optimizar"**. Verás cómo el algoritmo sugiere cambios (ej: Cambiar a Coca-Cola Zero o Leche Vegetal) dependiendo de tu preferencia.

---

## 🤖 Declaración de Uso de IA

De acuerdo con las instrucciones de la prueba técnica, declaro el uso de herramientas de Inteligencia Artificial Generativa durante el desarrollo:

* **Herramienta:** Google Gemini / ChatGPT.
* **Propósito:**
    * Generación de datos semilla (`seed_db`) con información realista de productos y códigos de barras.
    * Refactorización de componentes de React para asegurar buenas prácticas (Hooks).
    * Explicación y corrección de errores de configuración en Django (CORS y Migraciones).
    * Asistencia en la redacción de este README.
* **Validación:** Todo el código generado fue revisado, probado y adaptado manualmente para cumplir con la lógica de negocio específica de Grupo Lagos.