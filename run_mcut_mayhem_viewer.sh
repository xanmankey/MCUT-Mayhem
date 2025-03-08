#!/nix/store/m8xqd9hv339yxgiilbv7wvh8figqx135-system-path/bin/bash

cd MCUT-Mayhem-Viewer-WebApp
nix-shell -p nodejs_23 nodePackages.serve --run "serve -s dist -l 10092"
