#!/usr/bin/env bash
# iconMap one-step setup (macOS / Linux). Run: bash setup.sh
set -e
cd "$(dirname "$0")"
echo "iconMap setup"
command -v node >/dev/null || { echo "Install Node 18 or newer from https://nodejs.org, then run this again."; exit 1; }
echo "  OK node $(node -v)"
command -v ffmpeg >/dev/null || { echo "Install ffmpeg (brew install ffmpeg / apt install ffmpeg), then run this again."; exit 1; }
echo "  OK ffmpeg"
command -v python3 >/dev/null || { echo "Install Python 3.10 or newer, then run this again."; exit 1; }
npm install --silent && npx playwright install chromium
echo "  OK Playwright and Chromium"
python3 -m pip install -q -r requirements.txt
echo "  OK Python packages (voice, timing, imagery, mix)"
node scripts/render.mjs examples/demo-ar.json test-render.mp4 --scale 0.5 --to 3
echo "Done! test-render.mp4 created. The Globe engine (real NASA imagery, 3D) needs a GPU with WebGL: see README."