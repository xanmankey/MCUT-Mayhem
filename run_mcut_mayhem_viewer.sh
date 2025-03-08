#!/nix/store/m8xqd9hv339yxgiilbv7wvh8figqx135-system-path/bin/bash

cd MCUT-Mayhem-Viewer-WebApp
nix-shell -p "nodejs_23" --run "npm run preview"
