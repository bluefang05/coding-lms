"""
Módulo de auto-inserción de currículo en la base de datos.
Permite cargar lecciones, ejercicios y rutas de aprendizaje automáticamente.
"""

import sqlite3
from datetime import datetime
import json

class CurriculumLoader:
    def __init__(self, db_path="learning_platform.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Conectar a la base de datos SQLite"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"✓ Conectado a base de datos: {self.db_path}")
    
    def create_tables(self):
        """Crear tablas si no existen"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS technologies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                difficulty_level TEXT DEFAULT 'beginner',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                technology_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                order_index INTEGER,
                estimated_duration_minutes INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (technology_id) REFERENCES technologies(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_id INTEGER,
                title TEXT NOT NULL,
                content_type TEXT DEFAULT 'text',
                content_data TEXT,
                order_index INTEGER,
                estimated_duration_minutes INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (module_id) REFERENCES modules(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lesson_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                difficulty TEXT DEFAULT 'easy',
                starter_code TEXT,
                expected_output TEXT,
                test_cases TEXT,
                points INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lesson_id INTEGER,
                exercise_id INTEGER,
                completed BOOLEAN DEFAULT FALSE,
                score INTEGER,
                attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id),
                FOREIGN KEY (exercise_id) REFERENCES exercises(id)
            )
            """
        ]
        
        for table_sql in tables:
            self.cursor.execute(table_sql)
        
        self.conn.commit()
        print("✓ Tablas creadas exitosamente")
    
    def insert_technology(self, name, description, difficulty_level='beginner'):
        """Insertar una tecnología (Python, JavaScript, Angular, etc.)"""
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO technologies (name, description, difficulty_level) VALUES (?, ?, ?)",
                (name, description, difficulty_level)
            )
            self.conn.commit()
            
            # Obtener el ID
            self.cursor.execute("SELECT id FROM technologies WHERE name = ?", (name,))
            tech_id = self.cursor.fetchone()[0]
            print(f"✓ Tecnología insertada: {name} (ID: {tech_id})")
            return tech_id
        except Exception as e:
            print(f"✗ Error al insertar tecnología {name}: {e}")
            return None
    
    def insert_module(self, technology_id, title, description, order_index, estimated_duration=30):
        """Insertar un módulo de aprendizaje"""
        try:
            self.cursor.execute(
                """INSERT INTO modules 
                   (technology_id, title, description, order_index, estimated_duration_minutes) 
                   VALUES (?, ?, ?, ?, ?)""",
                (technology_id, title, description, order_index, estimated_duration)
            )
            self.conn.commit()
            
            module_id = self.cursor.lastrowid
            print(f"  ✓ Módulo insertado: {title} (ID: {module_id})")
            return module_id
        except Exception as e:
            print(f"  ✗ Error al insertar módulo {title}: {e}")
            return None
    
    def insert_lesson(self, module_id, title, content_type, content_data, order_index, estimated_duration=15):
        """Insertar una lección"""
        try:
            # Si content_data es un dict o lista, convertirlo a JSON
            if isinstance(content_data, (dict, list)):
                content_data = json.dumps(content_data, ensure_ascii=False)
            
            self.cursor.execute(
                """INSERT INTO lessons 
                   (module_id, title, content_type, content_data, order_index, estimated_duration_minutes) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (module_id, title, content_type, content_data, order_index, estimated_duration)
            )
            self.conn.commit()
            
            lesson_id = self.cursor.lastrowid
            print(f"    ✓ Lección insertada: {title} (ID: {lesson_id})")
            return lesson_id
        except Exception as e:
            print(f"    ✗ Error al insertar lección {title}: {e}")
            return None
    
    def insert_exercise(self, lesson_id, title, description, difficulty, 
                       starter_code=None, expected_output=None, 
                       test_cases=None, points=10):
        """Insertar un ejercicio práctico"""
        try:
            # Convertir listas/dicts a JSON si es necesario
            if isinstance(test_cases, (list, dict)):
                test_cases = json.dumps(test_cases, ensure_ascii=False)
            
            self.cursor.execute(
                """INSERT INTO exercises 
                   (lesson_id, title, description, difficulty, starter_code, 
                    expected_output, test_cases, points) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (lesson_id, title, description, difficulty, starter_code, 
                 expected_output, test_cases, points)
            )
            self.conn.commit()
            
            exercise_id = self.cursor.lastrowid
            print(f"      ✓ Ejercicio insertado: {title} (ID: {exercise_id}, Puntos: {points})")
            return exercise_id
        except Exception as e:
            print(f"      ✗ Error al insertar ejercicio {title}: {e}")
            return None
    
    def load_python_pandas_curriculum(self):
        """Cargar automáticamente el currículo completo de Python + Pandas"""
        print("\n🚀 Iniciando carga automática del currículo Python + Pandas...\n")
        
        # 1. Insertar tecnología Python
        python_id = self.insert_technology(
            name="Python",
            description="Lenguaje de programación versátil y poderoso, ideal para análisis de datos, automatización y desarrollo web.",
            difficulty_level="beginner"
        )
        
        if not python_id:
            print("✗ No se pudo insertar Python. Deteniendo carga.")
            return
        
        # 2. Módulos de Python Básico
        print("\n📚 Cargando módulos de Python Básico...")
        
        # Módulo 1: Introducción a Python
        module1 = self.insert_module(
            technology_id=python_id,
            title="Introducción a Python",
            description="Conceptos básicos: variables, tipos de datos, operadores y estructuras de control",
            order_index=1,
            estimated_duration=60
        )
        
        if module1:
            # Lecciones del Módulo 1
            lesson1_1 = self.insert_lesson(
                module_id=module1,
                title="Variables y Tipos de Datos",
                content_type="interactive",
                content_data={
                    "theory": """
# Variables y Tipos de Datos en Python

## ¿Qué es una variable?
Una variable es como una caja donde guardamos información que podemos usar después.

## Tipos de datos principales:
- **int**: Números enteros (ej: 5, -10, 42)
- **float**: Números decimales (ej: 3.14, -0.5)
- **str**: Texto o cadenas (ej: "Hola", 'Python')
- **bool**: Valores booleanos (True, False)
- **list**: Listas ordenadas (ej: [1, 2, 3])
- **dict**: Diccionarios clave-valor (ej: {"nombre": "Ana"})

## Ejemplos:
```python
edad = 25              # int
precio = 19.99         # float
nombre = "Carlos"      # str
es_estudiante = True   # bool
numeros = [1, 2, 3]    # list
persona = {"nombre": "Ana", "edad": 30}  # dict
```
                    """,
                    "examples": [
                        {"code": "x = 5\ny = 3.14\nnombre = 'Python'\nprint(type(x), type(y), type(nombre))", 
                         "output": "<class 'int'> <class 'float'> <class 'str'>"}
                    ],
                    "tips": ["Usa nombres descriptivos para tus variables", "Python es sensible a mayúsculas/minúsculas"]
                },
                order_index=1,
                estimated_duration=20
            )
            
            # Ejercicios para la lección 1.1
            if lesson1_1:
                self.insert_exercise(
                    lesson_id=lesson1_1,
                    title="Declaración de Variables",
                    description="Crea tres variables: una para tu edad (entero), otra para tu altura en metros (float) y otra para tu nombre (string). Luego imprímelas.",
                    difficulty="easy",
                    starter_code="# Completa el código abajo:\nedad = \naltura = \nnombre = \n\n# Imprime las variables\nprint(edad, altura, nombre)",
                    expected_output="El usuario debe declarar las tres variables correctamente",
                    test_cases=[
                        {"input": "", "checks": ["edad is int or edad is float", "altura is float or altura is int", "isinstance(nombre, str)"]}
                    ],
                    points=10
                )
                
                self.insert_exercise(
                    lesson_id=lesson1_1,
                    title="Operaciones Matemáticas Básicas",
                    description="Dadas dos variables a=10 y b=3, calcula y muestra: suma, resta, multiplicación, división y módulo.",
                    difficulty="easy",
                    starter_code="a = 10\nb = 3\n\n# Calcula las operaciones\nsuma = \nresta = \nmultiplicacion = \ndivision = \nmodulo = \n\nprint(suma, resta, multiplicacion, division, modulo)",
                    expected_output="13 7 30 3.3333333333333335 1",
                    test_cases=[
                        {"input": "a=10, b=3", "expected": {"suma": 13, "resta": 7, "multiplicacion": 30}}
                    ],
                    points=15
                )
            
            # Lección 1.2: Estructuras de Control
            lesson1_2 = self.insert_lesson(
                module_id=module1,
                title="Estructuras de Control: if, elif, else",
                content_type="interactive",
                content_data={
                    "theory": """
# Estructuras de Control en Python

## Condicionales (if, elif, else)
Nos permiten tomar decisiones en nuestro código.

```python
edad = 18

if edad >= 18:
    print("Eres mayor de edad")
elif edad >= 13:
    print("Eres adolescente")
else:
    print("Eres niño")
```

## Operadores de comparación:
- `==` Igual a
- `!=` Diferente de
- `>` Mayor que
- `<` Menor que
- `>=` Mayor o igual que
- `<=` Menor o igual que

## Operadores lógicos:
- `and`: Y lógico
- `or`: O lógico
- `not`: Negación
                    """,
                    "examples": [
                        {"code": "nota = 85\nif nota >= 90:\n    print('A')\nelif nota >= 80:\n    print('B')\nelse:\n    print('C')", 
                         "output": "B"}
                    ]
                },
                order_index=2,
                estimated_duration=25
            )
            
            if lesson1_2:
                self.insert_exercise(
                    lesson_id=lesson1_2,
                    title="Clasificador de Números",
                    description="Escribe un programa que dado un número, indique si es positivo, negativo o cero.",
                    difficulty="easy",
                    starter_code="numero = 5  # Cambia este valor para probar\n\n# Tu código aquí:\n\n",
                    expected_output="positivo, negativo o cero según el valor",
                    test_cases=[
                        {"input": "numero=5", "expected_output": "positivo"},
                        {"input": "numero=-3", "expected_output": "negativo"},
                        {"input": "numero=0", "expected_output": "cero"}
                    ],
                    points=15
                )
        
        # Módulo 2: Introducción a Pandas
        print("\n📊 Cargando módulos de Pandas...")
        
        module2 = self.insert_module(
            technology_id=python_id,
            title="Análisis de Datos con Pandas",
            description="Aprende a manipular y analizar datos usando la librería Pandas",
            order_index=2,
            estimated_duration=90
        )
        
        if module2:
            lesson2_1 = self.insert_lesson(
                module_id=module2,
                title="Introducción a Pandas: Series y DataFrames",
                content_type="interactive",
                content_data={
                    "theory": """
# Pandas: Tu Herramienta para Análisis de Datos

## ¿Qué es Pandas?
Pandas es una librería de Python especializada en manipulación y análisis de datos.

## Instalación:
```bash
pip install pandas
```

## Conceptos Clave:

### 1. Series
Una Serie es como una columna de una tabla. Es un array unidimensional.

```python
import pandas as pd

# Crear una Serie
edades = pd.Series([25, 30, 35, 40])
nombres = pd.Series(["Ana", "Carlos", "María", "Juan"])
```

### 2. DataFrame
Un DataFrame es como una tabla completa (filas y columnas).

```python
# Crear un DataFrame
datos = {
    'Nombre': ['Ana', 'Carlos', 'María', 'Juan'],
    'Edad': [25, 30, 35, 40],
    'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla']
}

df = pd.DataFrame(datos)
print(df)
```

Salida:
```
    Nombre  Edad     Ciudad
0     Ana    25     Madrid
1   Carlos   30  Barcelona
2    María   35   Valencia
3     Juan   40    Sevilla
```
                    """,
                    "examples": [
                        {
                            "code": "import pandas as pd\n\ndatos = {'Producto': ['A', 'B', 'C'], 'Precio': [10, 20, 30]}\ndf = pd.DataFrame(datos)\nprint(df)",
                            "output": "  Producto  Precio\n0        A      10\n1        B      20\n2        C      30"
                        }
                    ],
                    "tips": ["Usa df.head() para ver las primeras filas", "Usa df.info() para ver información general del DataFrame"]
                },
                order_index=1,
                estimated_duration=30
            )
            
            if lesson2_1:
                self.insert_exercise(
                    lesson_id=lesson2_1,
                    title="Creación de tu Primer DataFrame",
                    description="Crea un DataFrame con información de 3 libros: título, autor y año de publicación.",
                    difficulty="easy",
                    starter_code="import pandas as pd\n\n# Crea tu DataFrame aquí\nlibros = {\n    # Completa con 3 libros\n}\n\ndf_libros = pd.DataFrame(libros)\nprint(df_libros)",
                    expected_output="Un DataFrame con 3 filas y 3 columnas (título, autor, año)",
                    test_cases=[
                        {"input": "", "checks": ["len(df_libros) == 3", "'titulo' in df_libros.columns or 'título' in df_libros.columns"]}
                    ],
                    points=20
                )
                
                self.insert_exercise(
                    lesson_id=lesson2_1,
                    title="Exploración de Datos",
                    description="Dado un DataFrame existente, usa .head(), .info() y .describe() para explorarlo.",
                    difficulty="medium",
                    starter_code="import pandas as pd\n\n# DataFrame de ejemplo\ndatos = {\n    'Nombre': ['Ana', 'Carlos', 'María', 'Juan', 'Luisa'],\n    'Edad': [25, 30, 35, 40, 28],\n    'Salario': [30000, 45000, 50000, 60000, 35000]\n}\n\ndf = pd.DataFrame(datos)\n\n# Explora el DataFrame:\n# 1. Muestra las primeras 3 filas\n# 2. Muestra información general\n# 3. Muestra estadísticas descriptivas\n",
                    expected_output="Uso correcto de head(3), info() y describe()",
                    points=25
                )
            
            lesson2_2 = self.insert_lesson(
                module_id=module2,
                title="Filtrado y Selección de Datos",
                content_type="interactive",
                content_data={
                    "theory": """
# Filtrado y Selección de Datos en Pandas

## Seleccionar Columnas
```python
# Una columna (retorna Serie)
edades = df['Edad']

# Varias columnas (retorna DataFrame)
subset = df[['Nombre', 'Edad']]
```

## Filtrar Filas por Condición
```python
# Mayores de 30 años
mayores_30 = df[df['Edad'] > 30]

# Múltiples condiciones
filtro = df[(df['Edad'] > 30) & (df['Salario'] > 40000)]
```

## loc y iloc
- `loc`: Selección por etiquetas/nombres
- `iloc`: Selección por posición numérica

```python
# Primera fila, columna 'Nombre'
valor = df.loc[0, 'Nombre']

# Primera fila, primera columna
valor = df.iloc[0, 0]
```
                    """,
                    "examples": [
                        {
                            "code": "import pandas as pd\n\ndf = pd.DataFrame({'A': [1,2,3,4,5], 'B': [10,20,30,40,50]})\nprint(df[df['A'] > 2])",
                            "output": "   A   B\n2  3  30\n3  4  40\n4  5  50"
                        }
                    ]
                },
                order_index=2,
                estimated_duration=35
            )
            
            if lesson2_2:
                self.insert_exercise(
                    lesson_id=lesson2_2,
                    title="Filtrado Avanzado",
                    description="Filtra un DataFrame para encontrar empleados que ganen más de 40000 Y tengan menos de 35 años.",
                    difficulty="medium",
                    starter_code="import pandas as pd\n\ndf = pd.DataFrame({\n    'Nombre': ['Ana', 'Carlos', 'María', 'Juan', 'Luisa'],\n    'Edad': [25, 30, 35, 40, 28],\n    'Salario': [30000, 45000, 50000, 60000, 35000]\n})\n\n# Filtra según las condiciones\nresultado = \n\nprint(resultado)",
                    expected_output="DataFrame con Carlos (30 años, 45000) y Luisa (28 años, 35000)",
                    points=30
                )
        
        # Módulo 3: Visualización con Pandas (preparación para JS/Angular)
        module3 = self.insert_module(
            technology_id=python_id,
            title="Visualización de Datos",
            description="Gráficos básicos con Pandas y preparación para visualizaciones web",
            order_index=3,
            estimated_duration=60
        )
        
        if module3:
            lesson3_1 = self.insert_lesson(
                module_id=module3,
                title="Gráficos Básicos con Pandas",
                content_type="interactive",
                content_data={
                    "theory": """
# Visualización de Datos con Pandas

Pandas integra matplotlib para crear gráficos fácilmente.

## Tipos de Gráficos:

### Gráfico de Líneas
```python
df.plot(kind='line', x='Mes', y='Ventas')
```

### Gráfico de Barras
```python
df.plot(kind='bar', x='Categoría', y='Valor')
```

### Histograma
```python
df['Columna'].plot(kind='hist')
```

### Gráfico de Dispersión
```python
df.plot(kind='scatter', x='Edad', y='Salario')
```

## Personalización:
```python
df.plot(
    kind='bar',
    figsize=(10, 6),
    title='Ventas por Mes',
    xlabel='Mes',
    ylabel='Ventas (€)',
    color='blue',
    legend=True
)
```
                    """,
                    "examples": [
                        {
                            "code": "import pandas as pd\nimport matplotlib.pyplot as plt\n\ndatos = {'Mes': ['Ene', 'Feb', 'Mar', 'Abr'], 'Ventas': [100, 150, 200, 180]}\ndf = pd.DataFrame(datos)\ndf.plot(kind='bar', x='Mes', y='Ventas')\nplt.show()",
                            "output": "[Gráfico de barras mostrado]"
                        }
                    ],
                    "note": "Este contenido prepara el terreno para visualizaciones más avanzadas con JavaScript (D3.js, Chart.js) y Angular"
                },
                order_index=1,
                estimated_duration=40
            )
            
            if lesson3_1:
                self.insert_exercise(
                    lesson_id=lesson3_1,
                    title="Crea tu Primer Gráfico",
                    description="Genera un gráfico de líneas que muestre la evolución de temperaturas durante una semana.",
                    difficulty="medium",
                    starter_code="import pandas as pd\nimport matplotlib.pyplot as plt\n\n# Datos de temperatura\ndatos = {\n    'Día': ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],\n    'Temperatura': [22, 24, 19, 25, 27, 30, 28]\n}\n\ndf = pd.DataFrame(datos)\n\n# Crea el gráfico de líneas aquí\n\nplt.show()",
                    expected_output="Gráfico de líneas con 7 puntos de datos",
                    points=25
                )
        
        print("\n✅ ¡Carga del currículo Python + Pandas completada!")
        print("\n📋 Resumen:")
        print(f"   - 1 Tecnología: Python")
        print(f"   - 3 Módulos cargados")
        print(f"   - Múltiples lecciones interactivas")
        print(f"   - Ejercicios prácticos con validación")
        print("\n🔜 Próximamente: JavaScript y Angular")
    
    def load_javascript_curriculum(self, auto_insert=False):
        """Preparar estructura para currículo de JavaScript (lista para activar)"""
        if not auto_insert:
            print("\n⏸️  Módulo de JavaScript preparado pero no insertado.")
            print("   Usa load_javascript_curriculum(auto_insert=True) para activarlo.")
            return
        
        print("\n🚀 Cargando currículo de JavaScript...")
        # Implementación similar a Python cuando esté listo
        js_id = self.insert_technology(
            name="JavaScript",
            description="Lenguaje de programación para desarrollo web interactivo",
            difficulty_level="intermediate"
        )
        # ... continuar con módulos de JS
    
    def load_angular_curriculum(self, auto_insert=False):
        """Preparar estructura para currículo de Angular (lista para activar)"""
        if not auto_insert:
            print("\n⏸️  Módulo de Angular preparado pero no insertado.")
            print("   Usa load_angular_curriculum(auto_insert=True) para activarlo.")
            return
        
        print("\n🚀 Cargando currículo de Angular...")
        # Implementación similar cuando esté listo
        angular_id = self.insert_technology(
            name="Angular",
            description="Framework de TypeScript para aplicaciones web escalables",
            difficulty_level="advanced"
        )
        # ... continuar con módulos de Angular
    
    def get_curriculum_summary(self):
        """Mostrar resumen del currículo cargado"""
        print("\n📊 RESUMEN DEL CURRÍCULO EN BASE DE DATOS\n")
        
        # Tecnologías
        self.cursor.execute("SELECT COUNT(*), GROUP_CONCAT(name) FROM technologies")
        count, names = self.cursor.fetchone()
        print(f"🔧 Tecnologías ({count}): {names}")
        
        # Módulos
        self.cursor.execute("""
            SELECT t.name, COUNT(m.id) 
            FROM technologies t 
            LEFT JOIN modules m ON t.id = m.technology_id 
            GROUP BY t.id
        """)
        print("\n📚 Módulos por tecnología:")
        for tech, mod_count in self.cursor.fetchall():
            print(f"   • {tech}: {mod_count} módulos")
        
        # Lecciones
        self.cursor.execute("""
            SELECT m.title, COUNT(l.id) 
            FROM modules m 
            LEFT JOIN lessons l ON m.id = l.module_id 
            GROUP BY m.id
        """)
        print("\n📖 Lecciones por módulo:")
        for mod, lesson_count in self.cursor.fetchall():
            print(f"   • {mod}: {lesson_count} lecciones")
        
        # Ejercicios
        self.cursor.execute("""
            SELECT l.title, COUNT(e.id) 
            FROM lessons l 
            LEFT JOIN exercises e ON l.id = e.lesson_id 
            GROUP BY l.id
        """)
        print("\n✏️ Ejercicios por lección:")
        for lesson, ex_count in self.cursor.fetchall():
            if ex_count > 0:
                print(f"   • {lesson}: {ex_count} ejercicios")
        
        # Total de puntos disponibles
        self.cursor.execute("SELECT SUM(points) FROM exercises")
        total_points = self.cursor.fetchone()[0] or 0
        print(f"\n🏆 Puntos totales disponibles: {total_points}")
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            print("\n✓ Conexión cerrada")


# Función principal para ejecutar la carga automática
def auto_insert_curriculum(db_path="learning_platform.db", include_js=False, include_angular=False):
    """
    Función principal para auto-insertar el currículo en la base de datos.
    
    Args:
        db_path: Ruta a la base de datos SQLite
        include_js: Booleano para incluir JavaScript (default: False)
        include_angular: Booleano para incluir Angular (default: False)
    """
    loader = CurriculumLoader(db_path)
    
    try:
        loader.connect()
        loader.create_tables()
        loader.load_python_pandas_curriculum()
        
        if include_js:
            loader.load_javascript_curriculum(auto_insert=True)
        
        if include_angular:
            loader.load_angular_curriculum(auto_insert=True)
        
        loader.get_curriculum_summary()
        
    finally:
        loader.close()


if __name__ == "__main__":
    # Ejecutar carga automática
    auto_insert_curriculum()
