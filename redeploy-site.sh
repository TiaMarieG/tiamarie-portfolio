#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Enter project directory
cd /root/tiamarie-portfolio
echo "Changed directory to /root/tiamarie-portfolio"

# Step 2: Fetch and reset to latest main branch from GitHub
echo "Fetching and resetting to origin/main"
git fetch
git reset origin/main --hard

# Step 3: Spin down existing containers to free memory
echo "Stopping existing containers"
docker compose -f docker-compose.prod.yml down

# Step 4: Build and start containers in detached mode
echo "Building and starting Docker containers"
docker compose -f docker-compose.prod.yml up -d --build

echo "✅ Deployment complete."
