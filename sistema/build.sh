#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Entrar na pasta do manage.py se estiver em subpasta (ex: cd sistema)
cd sistema

python manage.py collectstatic --no-input
python manage.py migrate