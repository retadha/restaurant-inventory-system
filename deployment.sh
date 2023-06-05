#!/bin/bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
