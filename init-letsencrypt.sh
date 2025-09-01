#!/bin/bash
# Stop all services to free up port 80
docker compose down

# Run certbot to generate certificates
docker compose run --rm certbot certonly --standalone -d sweets.promo --non-interactive --agree-tos --email memememe@gmail.com

# Start all services
docker compose up -d