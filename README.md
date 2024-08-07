# Django Friend Request API

This project implements a friend request feature using Django and Django REST Framework.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/StrikerCode08/accuknox
cd accuknox
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On Unix or MacOS acitvate venv

source venv/bin/activate

# Install Dependencies and run migrations
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

