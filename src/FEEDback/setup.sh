#!/bin/bash
virtualenv -p `which python3` venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

# Uncomment the line below to add example data to the database
# echo 'import generate_data' | python manage.py shell