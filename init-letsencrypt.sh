#!/bin/bash
# Start web and nginx services
docker compose up -d web nginx

# Run certbot with webroot to generate certificates
docker compose run --rm certbot certonly --webroot -w /var/lib/letsencrypt -d sweets.promo --non-interactive --agree-tos --email memememe@gmail.com

# Restart nginx to load the certificates
docker compose restart nginx

# Start the certbot renewal service
docker compose up -d certbot