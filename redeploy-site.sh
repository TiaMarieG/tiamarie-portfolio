#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

cd /root/tiamarie-portfolio

# Fetches latest code from GitHub
git fetch && git reset origin/main --hard

# Activates virtual environment
source python3-virtualenv/bin/activate

# Installs dependencies
pip install -r requirements.txt

# Restarts systemd service
sudo systemctl daemon-reload
sudo systemctl restart myportfolio