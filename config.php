<?php
/**
 * Pandas Gamified LMS - Configuration File
 * 
 * Copy this file to config.php and edit with your settings
 */

// Database Configuration (SQLite)
define('DB_TYPE', 'sqlite');
define('DB_PATH', __DIR__ . '/data/pandas_lms.db');

// MySQL Configuration (optional, uncomment to use)
// define('DB_TYPE', 'mysql');
// define('DB_HOST', 'localhost');
// define('DB_NAME', 'pandas_lms');
// define('DB_USER', 'root');
// define('DB_PASS', '');

// Jupyter Configuration
define('JUPYTER_URL', 'http://localhost:8888');
define('JUPYTER_TOKEN', 'pandas123');

// Gamification Settings
define('XP_PER_EXERCISE', 30);
define('XP_PER_LESSON', 20);
define('XP_PER_PROJECT', 200);
define('STREAK_MULTIPLIER', 1.5);

// Level Thresholds
$GLOBALS['LEVEL_THRESHOLDS'] = [
    'Novato' => 0,
    'Analista Junior' => 500,
    'Analista Senior' => 1500,
    'Ingeniero' => 3000,
    'Ingeniero Senior' => 5000,
    'Arquitecto' => 8000
];

// Application Settings
define('APP_NAME', 'Pandas Gamified LMS');
define('APP_URL', 'http://localhost');
define('TIMEZONE', 'UTC');

// Upload Settings
define('UPLOAD_DIR', __DIR__ . '/uploads');
define('MAX_UPLOAD_SIZE', 10 * 1024 * 1024); // 10MB

// Export Settings
define('EXPORT_DIR', __DIR__ . '/exports');

// Session Settings
define('SESSION_LIFETIME', 3600 * 24); // 24 hours

// Email Settings (optional)
define('SMTP_HOST', '');
define('SMTP_PORT', 587);
define('SMTP_USER', '');
define('SMTP_PASS', '');
define('EMAIL_FROM', 'noreply@pandas-lms.local');

// Debug Mode
define('DEBUG', true);

// Date Format
define('DATE_FORMAT', 'Y-m-d H:i:s');
