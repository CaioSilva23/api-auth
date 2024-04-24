#!/bin/bash

# Aplica as migrações do banco de dados
python manage.py migrate

# Inicia o servidor Django
python manage.py runserver 0.0.0.0:8000
