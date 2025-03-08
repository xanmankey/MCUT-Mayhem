#!/nix/store/m8xqd9hv339yxgiilbv7wvh8figqx135-system-path/bin/bash

nix-shell -p "nodejs_23" --run "
cd MCUT-Mayhem-Streamer-WebApp
npm i
npm run build
cd ..
cd MCUT-Mayhem-Viewer-WebApp
npm i
npm run build
cd ..
echo 'All done!'
"
