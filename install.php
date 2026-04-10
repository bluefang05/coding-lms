<?php
/**
 * Pandas Gamified LMS - Auto-Installer
 * WordPress-style installation wizard
 */

// Disable error display for security during installation
error_reporting(E_ALL);
ini_set('display_errors', 0);

// Configuration
$step = isset($_GET['step']) ? (int)$_GET['step'] : 1;
$db_configured = false;
$installation_complete = false;
$errors = [];
$success_messages = [];

// Check if already installed
if (file_exists(__DIR__ . '/config.php') && filesize(__DIR__ . '/config.php') > 100) {
    require_once __DIR__ . '/config.php';
    if (defined('DB_HOST')) {
        $db_configured = true;
        // Check if database has content
        try {
            $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $stmt = $pdo->query("SELECT COUNT(*) FROM users");
            $user_count = $stmt->fetchColumn();
            if ($user_count > 0) {
                // Already installed with data, redirect to login
                header('Location: login.php');
                exit;
            }
        } catch (Exception $e) {
            // Database might not be set up yet
        }
    }
}

// Handle form submissions
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['action'])) {
        switch ($_POST['action']) {
            case 'check_requirements':
                // Requirements already checked on page load
                break;
                
            case 'save_database':
                $db_host = trim($_POST['db_host'] ?? 'localhost');
                $db_port = trim($_POST['db_port'] ?? '3306');
                $db_name = trim($_POST['db_name'] ?? 'pandas_lms');
                $db_user = trim($_POST['db_user'] ?? '');
                $db_pass = $_POST['db_pass'] ?? '';
                $db_prefix = trim($_POST['db_prefix'] ?? 'pandas_');
                
                // Validate inputs
                if (empty($db_host)) {
                    $errors[] = "Database host is required";
                }
                if (empty($db_name)) {
                    $errors[] = "Database name is required";
                }
                if (empty($db_user)) {
                    $errors[] = "Database user is required";
                }
                
                if (empty($errors)) {
                    // Test connection
                    try {
                        $dsn = "mysql:host={$db_host};port={$db_port};charset=utf8mb4";
                        $test_pdo = new PDO($dsn, $db_user, $db_pass);
                        $test_pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                        
                        // Check if database exists, create if not
                        $stmt = $test_pdo->query("SHOW DATABASES LIKE '{$db_name}'");
                        $db_exists = $stmt->rowCount() > 0;
                        
                        if (!$db_exists) {
                            // Try to create database
                            try {
                                $test_pdo->exec("CREATE DATABASE `{$db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
                                $success_messages[] = "Database '{$db_name}' created successfully";
                            } catch (Exception $create_error) {
                                $errors[] = "Could not create database: " . $create_error->getMessage();
                                $errors[] = "Please create the database manually or use a user with CREATE privileges";
                            }
                        } else {
                            // Database exists, check if it has content
                            $test_pdo->exec("USE `{$db_name}`");
                            try {
                                $stmt = $test_pdo->query("SHOW TABLES");
                                $tables = $stmt->fetchAll(PDO::FETCH_COLUMN);
                                if (!empty($tables)) {
                                    // Check for existing data
                                    foreach ($tables as $table) {
                                        $count_stmt = $test_pdo->query("SELECT COUNT(*) FROM `{$table}`");
                                        $count = $count_stmt->fetchColumn();
                                        if ($count > 0) {
                                            $success_messages[] = "Existing data found in table '{$table}' ({$count} records). Will preserve existing content.";
                                            break;
                                        }
                                    }
                                }
                            } catch (Exception $e) {
                                // Tables might not exist yet
                            }
                        }
                        
                        if (empty($errors)) {
                            // Generate config.php
                            $config_content = "<?php\n";
                            $config_content .= "/**\n";
                            $config_content .= " * Pandas Gamified LMS Configuration\n";
                            $config_content .= " * Auto-generated by installer on " . date('Y-m-d H:i:s') . "\n";
                            $config_content .= " */\n\n";
                            $config_content .= "// Database Configuration\n";
                            $config_content .= "define('DB_HOST', '" . addslashes($db_host) . "');\n";
                            $config_content .= "define('DB_PORT', '" . addslashes($db_port) . "');\n";
                            $config_content .= "define('DB_NAME', '" . addslashes($db_name) . "');\n";
                            $config_content .= "define('DB_USER', '" . addslashes($db_user) . "');\n";
                            $config_content .= "define('DB_PASS', '" . addslashes($db_pass) . "');\n";
                            $config_content .= "define('DB_PREFIX', '" . addslashes($db_prefix) . "');\n\n";
                            $config_content .= "// Application Settings\n";
                            $config_content .= "define('SITE_NAME', 'Pandas Gamified LMS');\n";
                            $config_content .= "define('SITE_URL', '" . (isset($_SERVER['HTTPS']) ? 'https' : 'http') . "://" . $_SERVER['HTTP_HOST'] . rtrim(dirname($_SERVER['PHP_SELF']), '/\\') . "');\n";
                            $config_content .= "define('DEBUG_MODE', false);\n\n";
                            $config_content .= "// Security\n";
                            $config_content .= "define('SECRET_KEY', '" . bin2hex(random_bytes(32)) . "');\n";
                            
                            // Try to write config file
                            if (file_put_contents(__DIR__ . '/config.php', $config_content)) {
                                $db_configured = true;
                                define('DB_HOST', $db_host);
                                define('DB_PORT', $db_port);
                                define('DB_NAME', $db_name);
                                define('DB_USER', $db_user);
                                define('DB_PASS', $db_pass);
                                define('DB_PREFIX', $db_prefix);
                                $success_messages[] = "Configuration file created successfully";
                            } else {
                                $errors[] = "Could not write config.php file. Please check permissions.";
                            }
                        }
                    } catch (PDOException $e) {
                        $errors[] = "Database connection failed: " . $e->getMessage();
                    }
                }
                break;
                
            case 'create_tables':
                if (!$db_configured) {
                    $errors[] = "Database not configured yet";
                    break;
                }
                
                try {
                    $pdo = new PDO("mysql:host=" . DB_HOST . ";port=" . DB_PORT . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS);
                    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                    
                    // Create tables
                    $tables_sql = [
                        "users" => "CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            role VARCHAR(20) DEFAULT 'student',
                            xp_points INT DEFAULT 0,
                            level VARCHAR(50) DEFAULT 'Novato',
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            INDEX idx_username (username),
                            INDEX idx_email (email)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "modules" => "CREATE TABLE IF NOT EXISTS modules (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            module_number INT NOT NULL,
                            title VARCHAR(200) NOT NULL,
                            description TEXT,
                            narrative_mission TEXT,
                            xp_reward INT DEFAULT 100,
                            order_index INT NOT NULL,
                            UNIQUE KEY unique_module_number (module_number)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "lessons" => "CREATE TABLE IF NOT EXISTS lessons (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            module_id INT NOT NULL,
                            title VARCHAR(200) NOT NULL,
                            content LONGTEXT,
                            lesson_type VARCHAR(50) DEFAULT 'theory',
                            order_index INT NOT NULL,
                            xp_reward INT DEFAULT 20,
                            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
                            INDEX idx_module (module_id)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "exercises" => "CREATE TABLE IF NOT EXISTS exercises (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            lesson_id INT NOT NULL,
                            title VARCHAR(200) NOT NULL,
                            description TEXT,
                            starter_code TEXT,
                            solution_code TEXT,
                            test_cases TEXT,
                            difficulty VARCHAR(20) DEFAULT 'easy',
                            xp_reward INT DEFAULT 30,
                            FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
                            INDEX idx_lesson (lesson_id)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "mini_projects" => "CREATE TABLE IF NOT EXISTS mini_projects (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            module_id INT NOT NULL,
                            title VARCHAR(200) NOT NULL,
                            description TEXT,
                            dataset_path VARCHAR(500),
                            requirements TEXT,
                            rubric TEXT,
                            xp_reward INT DEFAULT 200,
                            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
                            INDEX idx_module (module_id)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "badges" => "CREATE TABLE IF NOT EXISTS badges (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(100) UNIQUE NOT NULL,
                            description TEXT,
                            icon VARCHAR(50),
                            criteria VARCHAR(200),
                            badge_type VARCHAR(50) DEFAULT 'achievement'
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "user_badges" => "CREATE TABLE IF NOT EXISTS user_badges (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id INT NOT NULL,
                            badge_id INT NOT NULL,
                            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                            FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE,
                            UNIQUE KEY unique_user_badge (user_id, badge_id)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "submissions" => "CREATE TABLE IF NOT EXISTS submissions (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id INT NOT NULL,
                            exercise_id INT,
                            project_id INT,
                            code LONGTEXT NOT NULL,
                            status VARCHAR(20) DEFAULT 'pending',
                            score INT,
                            feedback TEXT,
                            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                            FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE SET NULL,
                            FOREIGN KEY (project_id) REFERENCES mini_projects(id) ON DELETE SET NULL,
                            INDEX idx_user (user_id)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci",
                        
                        "streaks" => "CREATE TABLE IF NOT EXISTS streaks (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id INT UNIQUE NOT NULL,
                            current_streak INT DEFAULT 0,
                            longest_streak INT DEFAULT 0,
                            last_activity DATE,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
                    ];
                    
                    foreach ($tables_sql as $table_name => $sql) {
                        $pdo->exec($sql);
                        $success_messages[] = "Table '{$table_name}' created/verified";
                    }
                    
                    // Check if we should insert initial data (only if tables are empty)
                    $stmt = $pdo->query("SELECT COUNT(*) FROM modules");
                    $module_count = $stmt->fetchColumn();
                    
                    if ($module_count == 0) {
                        // Insert initial modules
                        $modules_data = [
                            [0, 'Preparación del Terreno de Datos', 'Configuración del entorno y primeros pasos con Pandas', 'Pasaporte de Datos', 100, 0],
                            [1, 'Estructuras y Selección Precisa', 'Series, DataFrames y técnicas de indexación', 'Catálogo de Videojuegos', 150, 1],
                            [2, 'Ingesta, Exploración y Limpieza Forense', 'Carga de datos desde múltiples fuentes y limpieza', 'Forense de Ventas', 200, 2],
                            [3, 'Transformación y Remodelado de Datos', 'Apply, map, transform y reshape de datos', 'Transformador de Encuestas', 200, 3],
                            [4, 'Agrupaciones, Tablas Dinámicas y Estadísticas', 'GroupBy, pivot tables y análisis agregado', 'Dashboard Ejecutivo', 250, 4],
                            [5, 'Unión, Concatenación y Datos Relacionales', 'Merge, join, concat e integridad referencial', 'Arquitecto de Datos', 250, 5],
                            [6, 'Series Temporales y Tipos Categóricos', 'DatetimeIndex, resample, rolling y categóricos', 'Analista Temporal', 250, 6],
                            [7, 'Optimización, Desempeño y Buenas Prácticas', 'Perfilado de memoria, vectorización y optimización', 'Ingeniero de Rendimiento', 300, 7],
                            [8, 'Integración con el Ecosistema', 'Visualización, ML prep y automatización', 'Pipeline de Producción', 300, 8],
                            [9, 'Proyecto Final y Certificación', 'Proyecto integrador completo con revisión por pares', 'Proyecto Final', 500, 9]
                        ];
                        
                        $stmt = $pdo->prepare("INSERT INTO modules (module_number, title, description, narrative_mission, xp_reward, order_index) VALUES (?, ?, ?, ?, ?, ?)");
                        foreach ($modules_data as $module) {
                            $stmt->execute($module);
                        }
                        $success_messages[] = "Initial curriculum modules inserted";
                        
                        // Insert initial badges
                        $badges_data = [
                            ['🌱 Explorador del Entorno', 'Completa la configuración inicial del entorno', '🌱', 'setup_complete', 'achievement'],
                            ['🕵️ Detective de Datos', 'Limpia exitosamente un dataset sucio', '🕵️', 'cleaning_master', 'skill'],
                            ['🔗 Misión: Conexiones', 'Realiza uniones sin pérdida de datos', '🔗', 'join_master', 'skill'],
                            ['Maestro del Groupby', 'Domina las operaciones de agrupación', '👨‍🏫', 'groupby_expert', 'skill'],
                            ['Vectorizador', 'Escribe código 100% vectorizado', '⚡', 'vectorization_pro', 'skill'],
                            ['Cazador de Nulos', 'Identifica y maneja todos los valores faltantes', '🎯', 'null_hunter', 'skill'],
                            ['🛡️ Código de Acero', 'Optimiza un script en más del 70%', '🛡️', 'performance_master', 'achievement'],
                            ['🏆 Certificado de Integrador', 'Completa el pipeline de producción', '🏆', 'pipeline_complete', 'certification'],
                            ['Arquitecto de Datos', 'Completa todos los módulos', '🏛️', 'all_modules', 'completion']
                        ];
                        
                        $stmt = $pdo->prepare("INSERT INTO badges (name, description, icon, criteria, badge_type) VALUES (?, ?, ?, ?, ?)");
                        foreach ($badges_data as $badge) {
                            $stmt->execute($badge);
                        }
                        $success_messages[] = "Initial badges inserted";
                    } else {
                        $success_messages[] = "Existing curriculum data preserved";
                    }
                    
                } catch (PDOException $e) {
                    $errors[] = "Database setup failed: " . $e->getMessage();
                }
                break;
                
            case 'create_admin':
                if (!$db_configured) {
                    $errors[] = "Database not configured yet";
                    break;
                }
                
                $admin_username = trim($_POST['admin_username'] ?? '');
                $admin_email = trim($_POST['admin_email'] ?? '');
                $admin_password = $_POST['admin_password'] ?? '';
                $admin_password_confirm = $_POST['admin_password_confirm'] ?? '';
                
                if (empty($admin_username)) {
                    $errors[] = "Admin username is required";
                }
                if (empty($admin_email)) {
                    $errors[] = "Admin email is required";
                }
                if (empty($admin_password)) {
                    $errors[] = "Admin password is required";
                }
                if ($admin_password !== $admin_password_confirm) {
                    $errors[] = "Passwords do not match";
                }
                if (strlen($admin_password) < 6) {
                    $errors[] = "Password must be at least 6 characters";
                }
                
                if (empty($errors)) {
                    try {
                        $pdo = new PDO("mysql:host=" . DB_HOST . ";port=" . DB_PORT . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS);
                        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                        
                        // Check if admin already exists
                        $stmt = $pdo->prepare("SELECT id FROM users WHERE role = 'admin'");
                        $stmt->execute();
                        $existing_admin = $stmt->fetch();
                        
                        if ($existing_admin) {
                            $success_messages[] = "Admin account already exists";
                        } else {
                            // Create admin user
                            $password_hash = password_hash($admin_password, PASSWORD_DEFAULT);
                            $stmt = $pdo->prepare("INSERT INTO users (username, email, password_hash, role, xp_points, level) VALUES (?, ?, ?, 'admin', 1000, 'Administrador')");
                            $stmt->execute([$admin_username, $admin_email, $password_hash]);
                            
                            // Create initial streak record
                            $user_id = $pdo->lastInsertId();
                            $stmt = $pdo->prepare("INSERT INTO streaks (user_id, current_streak, longest_streak) VALUES (?, 0, 0)");
                            $stmt->execute([$user_id]);
                            
                            $success_messages[] = "Admin account created successfully";
                        }
                        
                        $installation_complete = true;
                        
                    } catch (PDOException $e) {
                        $errors[] = "Failed to create admin account: " . $e->getMessage();
                    }
                }
                break;
        }
    }
}

// Check server requirements
function check_requirements() {
    $requirements = [
        'PHP Version' => [
            'required' => '7.4+',
            'current' => phpversion(),
            'pass' => version_compare(phpversion(), '7.4', '>=')
        ],
        'PDO MySQL' => [
            'required' => 'Enabled',
            'current' => extension_loaded('pdo_mysql') ? 'Enabled' : 'Disabled',
            'pass' => extension_loaded('pdo_mysql')
        ],
        'JSON Support' => [
            'required' => 'Enabled',
            'current' => extension_loaded('json') ? 'Enabled' : 'Disabled',
            'pass' => extension_loaded('json')
        ],
        'OpenSSL' => [
            'required' => 'Enabled',
            'current' => extension_loaded('openssl') ? 'Enabled' : 'Disabled',
            'pass' => extension_loaded('openssl')
        ],
        'cURL' => [
            'required' => 'Enabled',
            'current' => extension_loaded('curl') ? 'Enabled' : 'Disabled',
            'pass' => extension_loaded('curl')
        ],
        'File Uploads' => [
            'required' => 'Enabled',
            'current' => ini_get('file_uploads') ? 'Enabled' : 'Disabled',
            'pass' => ini_get('file_uploads')
        ],
        'Write Permissions' => [
            'required' => 'Writable',
            'current' => is_writable(__DIR__) ? 'Writable' : 'Not Writable',
            'pass' => is_writable(__DIR__)
        ]
    ];
    
    return $requirements;
}

$requirements = check_requirements();
$all_requirements_met = !in_array(false, array_column($requirements, 'pass'));

?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pandas Gamified LMS - Installation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .installer-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
            overflow: hidden;
        }
        
        .installer-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .installer-header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .installer-header p {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .progress-bar {
            display: flex;
            background: #f8f9fa;
            padding: 20px 30px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .progress-step {
            flex: 1;
            text-align: center;
            position: relative;
            padding: 0 10px;
        }
        
        .progress-step:not(:last-child)::after {
            content: '';
            position: absolute;
            top: 15px;
            right: -50%;
            width: 100%;
            height: 2px;
            background: #e9ecef;
        }
        
        .progress-step.active:not(:last-child)::after {
            background: #667eea;
        }
        
        .step-number {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #e9ecef;
            color: #6c757d;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-bottom: 5px;
            transition: all 0.3s;
        }
        
        .progress-step.active .step-number {
            background: #667eea;
            color: white;
        }
        
        .progress-step.completed .step-number {
            background: #28a745;
            color: white;
        }
        
        .step-label {
            font-size: 12px;
            color: #6c757d;
        }
        
        .progress-step.active .step-label {
            color: #667eea;
            font-weight: 600;
        }
        
        .installer-body {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-group small {
            display: block;
            margin-top: 5px;
            color: #6c757d;
            font-size: 12px;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .alert {
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .alert-error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        
        .alert-success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        
        .alert-warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        
        .requirements-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        
        .requirements-table th,
        .requirements-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        .requirements-table th {
            background: #f8f9fa;
            font-weight: 600;
        }
        
        .status-pass {
            color: #28a745;
            font-weight: 600;
        }
        
        .status-fail {
            color: #dc3545;
            font-weight: 600;
        }
        
        .hidden {
            display: none;
        }
        
        .success-box {
            text-align: center;
            padding: 30px;
        }
        
        .success-icon {
            width: 80px;
            height: 80px;
            background: #28a745;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 40px;
            margin-bottom: 20px;
        }
        
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        
        .row {
            display: flex;
            gap: 20px;
        }
        
        .col {
            flex: 1;
        }
    </style>
</head>
<body>
    <div class="installer-container">
        <div class="installer-header">
            <h1>🐼 Pandas Gamified LMS</h1>
            <p>Installation Wizard</p>
        </div>
        
        <div class="progress-bar">
            <div class="progress-step <?php echo $step >= 1 ? 'active' : ''; ?> <?php echo $step > 1 ? 'completed' : ''; ?>">
                <div class="step-number">1</div>
                <div class="step-label">Requirements</div>
            </div>
            <div class="progress-step <?php echo $step >= 2 ? 'active' : ''; ?> <?php echo $step > 2 ? 'completed' : ''; ?>">
                <div class="step-number">2</div>
                <div class="step-label">Database</div>
            </div>
            <div class="progress-step <?php echo $step >= 3 ? 'active' : ''; ?> <?php echo $step > 3 ? 'completed' : ''; ?>">
                <div class="step-number">3</div>
                <div class="step-label">Tables</div>
            </div>
            <div class="progress-step <?php echo $step >= 4 ? 'active' : ''; ?>">
                <div class="step-number">4</div>
                <div class="step-label">Admin</div>
            </div>
        </div>
        
        <div class="installer-body">
            <?php foreach ($errors as $error): ?>
                <div class="alert alert-error"><?php echo htmlspecialchars($error); ?></div>
            <?php endforeach; ?>
            
            <?php foreach ($success_messages as $message): ?>
                <div class="alert alert-success"><?php echo htmlspecialchars($message); ?></div>
            <?php endforeach; ?>
            
            <!-- Step 1: Requirements Check -->
            <?php if ($step === 1): ?>
                <h2 style="margin-bottom: 20px;">Server Requirements</h2>
                <p style="margin-bottom: 20px; color: #6c757d;">We're checking if your server meets the minimum requirements.</p>
                
                <table class="requirements-table">
                    <thead>
                        <tr>
                            <th>Requirement</th>
                            <th>Required</th>
                            <th>Current</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($requirements as $name => $req): ?>
                            <tr>
                                <td><?php echo $name; ?></td>
                                <td><?php echo $req['required']; ?></td>
                                <td><?php echo $req['current']; ?></td>
                                <td>
                                    <?php if ($req['pass']): ?>
                                        <span class="status-pass">✓ Pass</span>
                                    <?php else: ?>
                                        <span class="status-fail">✗ Fail</span>
                                    <?php endif; ?>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
                
                <?php if ($all_requirements_met): ?>
                    <div class="alert alert-success">All requirements are met! You can proceed with the installation.</div>
                    <div style="text-align: right;">
                        <a href="?step=2" class="btn btn-primary">Continue to Database Setup →</a>
                    </div>
                <?php else: ?>
                    <div class="alert alert-error">Some requirements are not met. Please fix them before continuing.</div>
                <?php endif; ?>
            
            <!-- Step 2: Database Configuration -->
            <?php elseif ($step === 2): ?>
                <?php if ($db_configured): ?>
                    <div class="alert alert-success">Database is already configured!</div>
                    <div style="text-align: right;">
                        <a href="?step=3" class="btn btn-primary">Continue to Table Setup →</a>
                    </div>
                <?php else: ?>
                    <h2 style="margin-bottom: 20px;">Database Configuration</h2>
                    <p style="margin-bottom: 20px; color: #6c757d;">Enter your database credentials. If the database doesn't exist, we'll try to create it.</p>
                    
                    <div class="info-box">
                        <strong>💡 Tip:</strong> If you're using a hosting provider, you can find these details in your control panel. For local development, use localhost with your MySQL root credentials.
                    </div>
                    
                    <form method="POST">
                        <input type="hidden" name="action" value="save_database">
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="db_host">Database Host *</label>
                                    <input type="text" id="db_host" name="db_host" value="localhost" required>
                                    <small>Usually 'localhost' or your database server address</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="db_port">Port</label>
                                    <input type="number" id="db_port" name="db_port" value="3306">
                                    <small>Default MySQL port is 3306</small>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="db_name">Database Name *</label>
                                    <input type="text" id="db_name" name="db_name" value="pandas_lms" required>
                                    <small>Will be created if it doesn't exist</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="db_prefix">Table Prefix</label>
                                    <input type="text" id="db_prefix" name="db_prefix" value="pandas_">
                                    <small>Useful for multiple installations</small>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="db_user">Database Username *</label>
                                    <input type="text" id="db_user" name="db_user" required>
                                    <small>MySQL username with database privileges</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="db_pass">Database Password</label>
                                    <input type="password" id="db_pass" name="db_pass">
                                    <small>Leave blank if no password</small>
                                </div>
                            </div>
                        </div>
                        
                        <div style="text-align: right; margin-top: 30px;">
                            <a href="?step=1" class="btn btn-secondary">← Back</a>
                            <button type="submit" class="btn btn-primary">Test Connection & Save →</button>
                        </div>
                    </form>
                <?php endif; ?>
            
            <!-- Step 3: Create Tables -->
            <?php elseif ($step === 3): ?>
                <?php if (!$db_configured): ?>
                    <div class="alert alert-error">Database not configured yet. Please go back and configure it first.</div>
                    <div style="text-align: right;">
                        <a href="?step=2" class="btn btn-secondary">← Back to Database Setup</a>
                    </div>
                <?php else: ?>
                    <h2 style="margin-bottom: 20px;">Create Database Tables</h2>
                    <p style="margin-bottom: 20px; color: #6c757d;">We'll create all necessary tables for the LMS platform.</p>
                    
                    <div class="info-box">
                        <strong>ℹ️ Note:</strong> If tables already exist with data, we'll preserve your existing content and only create missing tables.
                    </div>
                    
                    <form method="POST">
                        <input type="hidden" name="action" value="create_tables">
                        
                        <div style="text-align: right;">
                            <a href="?step=2" class="btn btn-secondary">← Back</a>
                            <button type="submit" class="btn btn-primary">Create Tables →</button>
                        </div>
                    </form>
                <?php endif; ?>
            
            <!-- Step 4: Create Admin Account -->
            <?php elseif ($step === 4): ?>
                <h2 style="margin-bottom: 20px;">Create Administrator Account</h2>
                <p style="margin-bottom: 20px; color: #6c757d;">Set up the main administrator account for your LMS.</p>
                
                <?php if ($installation_complete): ?>
                    <div class="success-box">
                        <div class="success-icon">✓</div>
                        <h3 style="color: #28a745; margin-bottom: 15px;">Installation Complete!</h3>
                        <p style="color: #6c757d; margin-bottom: 20px;">Your Pandas Gamified LMS is ready to use.</p>
                        <a href="login.php" class="btn btn-primary">Go to Login Page</a>
                    </div>
                <?php else: ?>
                    <form method="POST">
                        <input type="hidden" name="action" value="create_admin">
                        
                        <div class="form-group">
                            <label for="admin_username">Username *</label>
                            <input type="text" id="admin_username" name="admin_username" required>
                            <small>Choose a unique username for the admin account</small>
                        </div>
                        
                        <div class="form-group">
                            <label for="admin_email">Email Address *</label>
                            <input type="email" id="admin_email" name="admin_email" required>
                            <small>This will be used for password recovery</small>
                        </div>
                        
                        <div class="row">
                            <div class="col">
                                <div class="form-group">
                                    <label for="admin_password">Password *</label>
                                    <input type="password" id="admin_password" name="admin_password" required minlength="6">
                                    <small>Minimum 6 characters</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="form-group">
                                    <label for="admin_password_confirm">Confirm Password *</label>
                                    <input type="password" id="admin_password_confirm" name="admin_password_confirm" required>
                                </div>
                            </div>
                        </div>
                        
                        <div style="text-align: right; margin-top: 30px;">
                            <a href="?step=3" class="btn btn-secondary">← Back</a>
                            <button type="submit" class="btn btn-success">Complete Installation ✓</button>
                        </div>
                    </form>
                <?php endif; ?>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>