#!/bin/bash

# Pandas Gamified LMS - Installation Script
# This script sets up the complete learning environment

set -e

echo "🚀 Installing Pandas Gamified LMS..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 is not installed. Please install pip3 first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python and pip found${NC}"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn jupyter notebook nbgrader pytest pandera sqlalchemy

# Create necessary directories
echo -e "${YELLOW}Creating directory structure...${NC}"
mkdir -p data/datasets
mkdir -p notebooks
mkdir -p uploads
mkdir -p exports

# Set permissions
chmod 755 data/datasets
chmod 755 notebooks
chmod 755 uploads
chmod 755 exports

# Copy sample datasets
echo -e "${YELLOW}Setting up sample datasets...${NC}"
cp backend/sample_datasets/* data/datasets/ 2>/dev/null || echo "Sample datasets will be downloaded on first use"

# Initialize database
echo -e "${YELLOW}Initializing database...${NC}"
python3 backend/init_database.py

# Create config file
if [ ! -f config.php ]; then
    echo -e "${YELLOW}Creating configuration file...${NC}"
    cp config.php.example config.php
    echo -e "${GREEN}✓ Configuration file created. Please edit config.php with your database credentials.${NC}"
fi

# Generate Jupyter config
echo -e "${YELLOW}Generating Jupyter configuration...${NC}"
jupyter notebook --generate-config -y

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 Installation Complete!                            ║${NC}"
echo -e "${GREEN}╠════════════════════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║  Next steps:                                           ║${NC}"
echo -e "${GREEN}║  1. Edit config.php with your database credentials    ║${NC}"
echo -e "${GREEN}║  2. Run: source venv/bin/activate                     ║${NC}"
echo -e "${GREEN}║  3. Start Jupyter: jupyter notebook                   ║${NC}"
echo -e "${GREEN}║  4. Access the LMS at: http://localhost:8888          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
