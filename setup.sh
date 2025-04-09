#!/bin/bash

set -e  # exit on error

echo "🔐 Setting permissions for current user and group..."
chmod -R ug+rwX data meltano/output

echo "📦 Installing Meltano plugins (if needed)..."
docker-compose run --rm meltano meltano install

echo "✅ Done! Your project is ready to use."
