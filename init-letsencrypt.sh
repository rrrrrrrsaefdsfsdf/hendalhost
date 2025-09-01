#!/bin/bash
docker compose down
docker compose run --rm certbot certonly --standalone -d sweets.promo --non-interactive --agree-tos --email memememe@gmail.com
docker compose up -d