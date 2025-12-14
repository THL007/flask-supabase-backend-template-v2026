#!/bin/bash
# Setup script for the Flask Supabase Backend

set -e

echo "🚀 Setting up Flask Supabase Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11 or higher is required. Found: $python_version"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "⚠️  Please update .env with your configuration"
    else
        echo "⚠️  .env.example not found. Please create .env manually"
    fi
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p content/blog
mkdir -p logs
mkdir -p migrations/versions

# Initialize Alembic if not already done
if [ ! -f "migrations/versions/.gitkeep" ]; then
    echo "🗄️  Initializing Alembic migrations..."
    alembic init migrations || echo "Alembic already initialized"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your Supabase credentials"
echo "2. Run 'alembic upgrade head' to apply database migrations"
echo "3. Run 'python run.py' to start the development server"
echo "4. Run 'celery -A celery_worker.celery worker --loglevel=info' to start Celery worker"

