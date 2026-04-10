# 🐼 Pandas Gamified LMS - Complete Installation Package

A comprehensive, installable Learning Management System for learning Python Pandas through gamification and hands-on projects.

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

```bash
# Clone or navigate to the project directory
cd /workspace

# Run the installation script
chmod +x install/install.sh
./install/install.sh
```

### Option 2: Manual Installation

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python backend/init_database.py

# 4. Generate sample datasets
python backend/sample_datasets/generate_datasets.py

# 5. Configure your environment
cp config.php.example config.php
# Edit config.php with your database credentials

# 6. Start Jupyter Notebook for interactive lessons
jupyter notebook
```

## 📦 What's Included

### Core Components
- **10 Progressive Modules** (0-9) covering basics to advanced topics
- **Gamification System** with XP, badges, streaks, and leaderboards
- **Interactive Jupyter Notebooks** for hands-on practice
- **Automated Assessment** using nbgrader and pytest
- **Sample Datasets** for all mini-projects
- **SQLite Database** for tracking progress

### Directory Structure

```
/workspace
├── install/                    # Installation scripts
│   └── install.sh             # Main installer
├── backend/                   # Backend services
│   ├── init_database.py       # Database initialization
│   ├── auto_insert_curriculum.py
│   └── sample_datasets/       # Dataset generator
│       └── generate_datasets.py
├── data/                      # Data storage
│   ├── pandas_lms.db          # SQLite database
│   └── datasets/              # CSV datasets for exercises
├── notebooks/                 # Jupyter notebooks for each module
├── includes/                  # PHP includes
│   ├── gamification.php       # Gamification logic
│   └── functions.php          # Helper functions
├── admin/                     # Admin panel
├── lessons/                   # Lesson viewer
├── exercises/                 # Exercise runner
├── assets/                    # CSS, JS, images
├── requirements.txt           # Python dependencies
└── config.php.example         # Configuration template
```

## 🎮 Gamification Features

### Progression System
- **Levels**: Novato → Analista → Ingeniero → Arquitecto
- **XP Points**: Earned from exercises, projects, and challenges
- **Technical Badges**: 
  - 🌱 Explorador del Entorno
  - 🕵️ Detective de Datos
  - 🔗 Misión: Conexiones
  - Maestro del Groupby
  - Vectorizador
  - 🛡️ Código de Acero
  - And more!

### Engagement Mechanics
- **Daily Streaks**: XP multipliers for consecutive days
- **Leaderboards**: Ranked by XP, accuracy, and efficiency
- **Boss Fights**: Challenging end-of-module projects
- **Peer Review**: Collaborative learning system

## 📚 Curriculum Overview

### Phase 1: Foundations (Modules 0-3)
- **Module 0**: Environment Setup & First Steps
- **Module 1**: Series, DataFrames & Indexing
- **Module 2**: Data Ingestion & Cleaning
- **Module 3**: Transformation & Reshaping

### Phase 2: Analysis (Modules 4-6)
- **Module 4**: GroupBy & Aggregations
- **Module 5**: Merging & Joining Data
- **Module 6**: Time Series & Categories

### Phase 3: Mastery (Modules 7-9)
- **Module 7**: Optimization & Best Practices
- **Module 8**: Ecosystem Integration (Viz, ML)
- **Module 9**: Final Capstone Project

## 🛠️ Technical Requirements

### Minimum Requirements
- Python 3.8+
- pip3
- 2GB RAM
- 500MB disk space

### Recommended
- Python 3.10+
- 4GB+ RAM
- Modern web browser
- Git (for version control features)

### Dependencies
All Python dependencies are listed in `requirements.txt`:
- pandas, numpy, matplotlib, seaborn
- jupyter, notebook, nbgrader
- pytest, pandera (for validation)
- sqlalchemy (database ORM)

## 🎯 Usage Guide

### For Students

1. **Register/Login** at the main dashboard
2. **Start with Module 0** to set up your environment
3. **Complete lessons** in order (theory → exercises → mini-project)
4. **Earn XP and badges** as you progress
5. **Build your portfolio** with completed projects
6. **Compete on leaderboards** with other students

### For Instructors

1. **Access admin panel** at `/admin/`
2. **Monitor student progress** via dashboard
3. **Review submissions** and provide feedback
4. **Customize curriculum** by adding/editing exercises
5. **Export analytics** for reporting

### Running Jupyter Notebooks

```bash
# Activate virtual environment
source venv/bin/activate

# Start Jupyter
jupyter notebook --notebook-dir=notebooks

# Or use JupyterHub for multi-user setup
jupyterhub
```

## 📊 Database Schema

The system uses SQLite with the following main tables:
- `users` - Student accounts and progress
- `modules` - Course modules
- `lessons` - Individual lessons
- `exercises` - Coding exercises
- `mini_projects` - Capstone projects per module
- `badges` - Available achievements
- `user_badges` - Earned badges
- `submissions` - Student code submissions
- `streaks` - Daily activity tracking

## 🔧 Configuration

Edit `config.php` to customize:
- Database connection settings
- JupyterHub integration
- Email notifications
- Gamification parameters
- Export settings (LinkedIn, GitHub)

## 🚀 Deployment Options

### Local Development
Use the included installation script for quick setup.

### Docker Deployment
```bash
docker build -t pandas-lms .
docker run -p 8888:8888 -p 80:80 pandas-lms
```

### Cloud Platforms
- **Render/Railway**: Deploy as a PaaS
- **Kubernetes**: Use provided Helm charts for scaling
- **Google Colab**: Integration available via API

## 📈 Analytics & Metrics

Track these key metrics:
- Module completion rates
- Average time per exercise
- Common error patterns
- Badge distribution
- Leaderboard standings
- Streak statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new exercises or datasets
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support

- **Documentation**: Check the `/docs` folder
- **Issues**: Report bugs on GitHub
- **Community**: Join our discussion forum

---

**Ready to start?** Run `./install/install.sh` and begin your Pandas journey! 🎉
