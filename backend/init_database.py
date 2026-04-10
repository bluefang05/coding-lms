"""
Database Initialization Script for Pandas Gamified LMS
Creates all necessary tables and inserts initial curriculum data
"""

import sqlite3
import os
from datetime import datetime

def init_database():
    """Initialize the SQLite database with all required tables"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'pandas_lms.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            xp_points INTEGER DEFAULT 0,
            level TEXT DEFAULT 'Novato',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create modules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_number INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            narrative_mission TEXT,
            xp_reward INTEGER DEFAULT 100,
            order_index INTEGER NOT NULL
        )
    ''')
    
    # Create lessons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            lesson_type TEXT DEFAULT 'theory',
            order_index INTEGER NOT NULL,
            xp_reward INTEGER DEFAULT 20,
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    ''')
    
    # Create exercises table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            starter_code TEXT,
            solution_code TEXT,
            test_cases TEXT,
            difficulty TEXT DEFAULT 'easy',
            xp_reward INTEGER DEFAULT 30,
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
    ''')
    
    # Create mini_projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mini_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            dataset_path TEXT,
            requirements TEXT,
            rubric TEXT,
            xp_reward INTEGER DEFAULT 200,
            FOREIGN KEY (module_id) REFERENCES modules(id)
        )
    ''')
    
    # Create badges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            icon TEXT,
            criteria TEXT,
            badge_type TEXT DEFAULT 'achievement'
        )
    ''')
    
    # Create user_badges table (many-to-many)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            badge_id INTEGER NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (badge_id) REFERENCES badges(id),
            UNIQUE(user_id, badge_id)
        )
    ''')
    
    # Create submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exercise_id INTEGER,
            project_id INTEGER,
            code TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            score INTEGER,
            feedback TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (exercise_id) REFERENCES exercises(id),
            FOREIGN KEY (project_id) REFERENCES mini_projects(id)
        )
    ''')
    
    # Create streaks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_activity DATE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id)
        )
    ''')
    
    # Create leaderboards view
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS leaderboard AS
        SELECT 
            u.id,
            u.username,
            u.xp_points,
            u.level,
            COUNT(ub.badge_id) as badge_count,
            COUNT(s.id) as submissions_count
        FROM users u
        LEFT JOIN user_badges ub ON u.id = ub.user_id
        LEFT JOIN submissions s ON u.id = s.user_id
        GROUP BY u.id
        ORDER BY u.xp_points DESC, badge_count DESC
    ''')
    
    # Insert initial modules
    modules_data = [
        (0, 'Preparación del Terreno de Datos', 'Configuración del entorno y primeros pasos con Pandas', 'Pasaporte de Datos', 100, 0),
        (1, 'Estructuras y Selección Precisa', 'Series, DataFrames y técnicas de indexación', 'Catálogo de Videojuegos', 150, 1),
        (2, 'Ingesta, Exploración y Limpieza Forense', 'Carga de datos desde múltiples fuentes y limpieza', 'Forense de Ventas', 200, 2),
        (3, 'Transformación y Remodelado de Datos', 'Apply, map, transform y reshape de datos', 'Transformador de Encuestas', 200, 3),
        (4, 'Agrupaciones, Tablas Dinámicas y Estadísticas', 'GroupBy, pivot tables y análisis agregado', 'Dashboard Ejecutivo', 250, 4),
        (5, 'Unión, Concatenación y Datos Relacionales', 'Merge, join, concat e integridad referencial', 'Arquitecto de Datos', 250, 5),
        (6, 'Series Temporales y Tipos Categóricos', 'DatetimeIndex, resample, rolling y categóricos', 'Analista Temporal', 250, 6),
        (7, 'Optimización, Desempeño y Buenas Prácticas', 'Perfilado de memoria, vectorización y optimización', 'Ingeniero de Rendimiento', 300, 7),
        (8, 'Integración con el Ecosistema', 'Visualización, ML prep y automatización', 'Pipeline de Producción', 300, 8),
        (9, 'Proyecto Final y Certificación', 'Proyecto integrador completo con revisión por pares', 'Proyecto Final', 500, 9)
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO modules 
        (module_number, title, description, narrative_mission, xp_reward, order_index)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', modules_data)
    
    # Insert initial badges
    badges_data = [
        ('🌱 Explorador del Entorno', 'Completa la configuración inicial del entorno', '🌱', 'setup_complete', 'achievement'),
        ('🕵️ Detective de Datos', 'Limpia exitosamente un dataset sucio', '🕵️', 'cleaning_master', 'skill'),
        ('🔗 Misión: Conexiones', 'Realiza uniones sin pérdida de datos', '🔗', 'join_master', 'skill'),
        ('Maestro del Groupby', 'Domina las operaciones de agrupación', '👨‍🏫', 'groupby_expert', 'skill'),
        ('Vectorizador', 'Escribe código 100% vectorizado', '⚡', 'vectorization_pro', 'skill'),
        ('Cazador de Nulos', 'Identifica y maneja todos los valores faltantes', '🎯', 'null_hunter', 'skill'),
        ('🛡️ Código de Acero', 'Optimiza un script en más del 70%', '🛡️', 'performance_master', 'achievement'),
        ('🏆 Certificado de Integrador', 'Completa el pipeline de producción', '🏆', 'pipeline_complete', 'certification'),
        ('Arquitecto de Datos', 'Completa todos los módulos', '🏛️', 'all_modules', 'completion')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO badges (name, description, icon, criteria, badge_type)
        VALUES (?, ?, ?, ?, ?)
    ''', badges_data)
    
    # Insert sample streak record template
    cursor.execute('''
        INSERT OR IGNORE INTO streaks (user_id, current_streak, longest_streak, last_activity)
        VALUES (0, 0, 0, NULL)
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized successfully at {db_path}")
    return db_path

if __name__ == '__main__':
    init_database()
