#!/nix/store/m8xqd9hv339yxgiilbv7wvh8figqx135-system-path/bin/bash

cd MCUT-Mayhem-Backend
source venv/bin/activate
nix-shell ../shell.nix --run "python app.py"
