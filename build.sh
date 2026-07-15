#!/bin/bash
set -e
npm install
npm run build:css
python manage.py collectstatic --noinput
python manage.py migrate --noinput