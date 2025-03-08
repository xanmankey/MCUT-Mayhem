#!/nix/store/m8xqd9hv339yxgiilbv7wvh8figqx135-system-path/bin/bash

cd site
source venv/bin/activate
nix-shell ../shell.nix --run "PYTHONUNBUFFERED=1 gunicorn --config gunicorn_config.py --capture-output app:app | tee logs/website/$(date +"%Y-%m-%d_%H-%M-%S").txt"
