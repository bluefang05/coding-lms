# 🐼 Pandas Gamified LMS - Installation Guide

## Quick Start (Recommended)

The easiest way to install the Pandas Gamified LMS is using the **web-based auto-installer**:

1. **Upload files** to your web server or local development environment
2. **Navigate to** `http://your-domain.com/install.php`
3. **Follow the wizard**:
   - Step 1: Server requirements check
   - Step 2: Database configuration (database will be created automatically if it doesn't exist)
   - Step 3: Table creation (existing data will be preserved)
   - Step 4: Admin account setup
4. **Done!** You'll be redirected to the login page

## Manual Installation

If you prefer manual installation:

### 1. Requirements

- PHP 7.4 or higher
- MySQL 5.7+ or MariaDB 10.3+
- PDO MySQL extension enabled
- Web server (Apache, Nginx, etc.)

### 2. Database Setup

Create a MySQL database and user:

```sql
CREATE DATABASE pandas_lms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pandas_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON pandas_lms.* TO 'pandas_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Configuration

Copy `config.php.example` to `config.php`:

```bash
cp config.php.example config.php
```

Edit `config.php` with your database credentials:

```php
define('DB_HOST', 'localhost');
define('DB_PORT', '3306');
define('DB_NAME', 'pandas_lms');
define('DB_USER', 'pandas_user');
define('DB_PASS', 'your_secure_password');
```

### 4. Run Installation

Access `install.php` in your browser to create tables and set up the admin account.

## Docker Installation

Using Docker Compose:

```bash
docker-compose up -d
```

Then navigate to `http://localhost:8080/install.php`

## Troubleshooting

### "Could not create database"

Make sure your MySQL user has CREATE privileges, or create the database manually before running the installer.

### "Config file not writable"

Ensure the web server has write permissions to the installation directory:

```bash
chmod 755 /path/to/pandas-lms
chown www-data:www-data /path/to/pandas-lms
```

### "PDO MySQL not enabled"

Install the PDO MySQL extension:

**Ubuntu/Debian:**
```bash
sudo apt-get install php-mysql
sudo systemctl restart apache2
```

**CentOS/RHEL:**
```bash
sudo yum install php-mysqlnd
sudo systemctl restart httpd
```

## Post-Installation

1. **Delete the installer** for security:
   ```bash
   rm install.php
   ```

2. **Set DEBUG_MODE to false** in `config.php` for production

3. **Change default admin password** immediately after first login

4. **Set up email configuration** in `config.php` for password recovery features

## Support

For issues or questions, please check the main README.md or open an issue on GitHub.
