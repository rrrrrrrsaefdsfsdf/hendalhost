#!/bin/bash
docker-compose up -d web
docker-compose run --rm certbot certonly --standalone -d sweets.promo --non-interactive --agree-tos --email memememe@gmail.com
docker-compose down
docker-compose up -d