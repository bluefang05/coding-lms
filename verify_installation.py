#!/usr/bin/env python3
"""
Quick verification script for Pandas Gamified LMS installation
Checks if all components are properly installed and configured
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = ['pandas', 'numpy', 'matplotlib', 'seaborn']
    optional = ['jupyter', 'nbgrader', 'pytest', 'pandera', 'sqlalchemy']
    
    missing_required = []
    missing_optional = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"❌ {package} (required)")
    
    for package in optional:
        try:
            __import__(package)
            print(f"✅ {package} (optional)")
        except ImportError:
            missing_optional.append(package)
            print(f"⚠️  {package} (optional, not installed)")
    
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def check_database():
    """Check if database exists and is initialized"""
    db_path = Path(__file__).parent / 'data' / 'pandas_lms.db'
    if db_path.exists():
        print(f"✅ Database found at {db_path}")
        
        # Check tables
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        expected_tables = ['users', 'modules', 'lessons', 'exercises', 
                          'mini_projects', 'badges', 'user_badges', 
                          'submissions', 'streaks']
        
        for table in expected_tables:
            if table in tables:
                print(f"   ✅ Table: {table}")
            else:
                print(f"   ❌ Table: {table} (missing)")
        
        return True
    else:
        print(f"❌ Database not found at {db_path}")
        print("   Run: python backend/init_database.py")
        return False

def check_datasets():
    """Check if sample datasets exist"""
    datasets_dir = Path(__file__).parent / 'data' / 'datasets'
    expected_datasets = [
        'video_games_catalog.csv',
        'dirty_sales_data.csv',
        'survey_data_wide.csv',
        'sales_transactions.csv',
        'customers.csv',
        'products.csv',
        'time_series_data.csv',
        'server_logs.csv'
    ]
    
    if not datasets_dir.exists():
        print(f"❌ Datasets directory not found")
        return False
    
    print(f"✅ Datasets directory found")
    
    missing = []
    for dataset in expected_datasets:
        dataset_path = datasets_dir / dataset
        if dataset_path.exists():
            size = dataset_path.stat().st_size
            print(f"   ✅ {dataset} ({size:,} bytes)")
        else:
            missing.append(dataset)
            print(f"   ❌ {dataset} (missing)")
    
    if missing:
        print(f"\n   Run: python backend/sample_datasets/generate_datasets.py")
        return len(missing) < 3  # Allow some missing
    
    return True

def check_directory_structure():
    """Check if required directories exist"""
    required_dirs = [
        'install',
        'backend',
        'data',
        'data/datasets',
        'notebooks',
        'includes',
        'admin',
        'lessons',
        'exercises',
        'assets'
    ]
    
    all_good = True
    for dir_path in required_dirs:
        full_path = Path(__file__).parent / dir_path
        if full_path.exists() and full_path.is_dir():
            print(f"✅ /{dir_path}")
        else:
            print(f"❌ /{dir_path} (missing)")
            all_good = False
    
    return all_good

def check_config():
    """Check if configuration file exists"""
    config_path = Path(__file__).parent / 'config.php'
    config_example = Path(__file__).parent / 'config.php.example'
    
    if config_path.exists():
        print(f"✅ config.php found")
        return True
    elif config_example.exists():
        print(f"⚠️  config.php not found, but config.php.example exists")
        print(f"   Run: cp config.php.example config.php")
        return False
    else:
        print(f"⚠️  No configuration file found")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("🐼 Pandas Gamified LMS - Installation Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Datasets", check_datasets),
        ("Directory Structure", check_directory_structure),
        ("Configuration", check_config)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 40)
        result = check_func()
        results.append((name, result))
        print()
    
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    if passed == total:
        print("🎉 All checks passed! Your installation is ready.")
        print()
        print("Next steps:")
        print("  1. Configure config.php with your database settings")
        print("  2. Start Jupyter: jupyter notebook")
        print("  3. Access the LMS at http://localhost:8888")
        return 0
    else:
        print(f"⚠️  {total - passed} check(s) failed. Please review the errors above.")
        print()
        print("To fix issues:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Initialize database: python backend/init_database.py")
        print("  3. Generate datasets: python backend/sample_datasets/generate_datasets.py")
        return 1

if __name__ == '__main__':
    sys.exit(main())
