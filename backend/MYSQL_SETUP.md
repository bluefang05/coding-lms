# Configuración de MySQL para la Plataforma de Aprendizaje

## Variables de Entorno

Crea un archivo `.env` en el directorio `backend/` con la siguiente configuración:

```bash
# Configuración de MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=learning_platform
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña_segura

# Opcional: Para entornos de desarrollo
MYSQL_ROOT_PASSWORD=tu_contraseña_root
```

## Instalación de Dependencias

```bash
pip install mysql-connector-python
pip install python-dotenv
```

## Creación de la Base de Datos

### Opción 1: Automática (Recomendada)
El script `auto_insert_curriculum.py` creará automáticamente la base de datos y las tablas al ejecutarse:

```bash
cd backend
python auto_insert_curriculum.py
```

### Opción 2: Manual
```sql
CREATE DATABASE IF NOT EXISTS learning_platform 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE learning_platform;
```

## Estructura de la Base de Datos

La plataforma utiliza 5 tablas principales:

1. **technologies** - Tecnologías enseñadas (Python, JavaScript, Angular, etc.)
2. **modules** - Módulos de aprendizaje por tecnología
3. **lessons** - Lecciones individuales dentro de cada módulo
4. **exercises** - Ejercicios prácticos con validación automática
5. **user_progress** - Seguimiento del progreso del usuario

## Características MySQL

- **Motor**: InnoDB con soporte para transacciones
- **Codificación**: UTF8MB4 (soporte completo para caracteres especiales y emojis)
- **Claves Foráneas**: Con CASCADE DELETE para integridad referencial
- **Auto-incremento**: IDs automáticos para todas las tablas
- **Timestamps**: Seguimiento automático de creación y actualización

## Conexión desde Python

```python
from auto_insert_curriculum import CurriculumLoader

# Configuración personalizada
loader = CurriculumLoader(
    host='localhost',
    database='learning_platform',
    user='root',
    password='tu_contraseña',
    port=3306
)

try:
    loader.connect()
    loader.create_tables()
    loader.load_python_pandas_curriculum()
finally:
    loader.close()
```

## Docker (Opcional)

Para usar MySQL en Docker:

```yaml
# docker-compose.yml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    container_name: learning_platform_db
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: learning_platform
      MYSQL_USER: learner
      MYSQL_PASSWORD: learner_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password

volumes:
  mysql_data:
```

Ejecutar:
```bash
docker-compose up -d
```

Luego actualiza el `.env`:
```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=learning_platform
MYSQL_USER=learner
MYSQL_PASSWORD=learner_password
```

## Seguridad

⚠️ **Importante**: 
- Nunca subas el archivo `.env` a control de versiones
- Cambia las contraseñas por defecto en producción
- Usa variables de entorno para manejar credenciales sensibles
- Considera usar conexiones SSL para MySQL en producción
