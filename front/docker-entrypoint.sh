#!/bin/sh
set -e

cd /app

echo "Checking dependencies..."

# Vérifier si vite existe et est exécutable dans le volume nommé
if [ ! -f "node_modules/.bin/vite" ] || [ ! -x "node_modules/.bin/vite" ]; then
  echo "vite not found or not executable, installing dependencies..."
  npm install --legacy-peer-deps
  echo "Dependencies installed successfully"
else
  echo "Dependencies already installed"
fi

# Vérifier une dernière fois que vite est disponible
if [ ! -f "node_modules/.bin/vite" ]; then
  echo "ERROR: vite still not found after installation"
  exit 1
fi

echo "Dependencies ready. Starting application..."

# Exécuter la commande passée en argument
exec "$@"

