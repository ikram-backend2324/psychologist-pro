#!/usr/bin/env bash
# Render build script. Free instances have no pre-deploy command or shell,
# so migrations, roles, the admin account and demo content are set up here. Safe to re-run.
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
python manage.py compile_translations
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py setup_roles

if [ "${SEED_DEMO:-false}" = "true" ]; then
  python manage.py seed_demo
fi
