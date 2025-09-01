#!/bin/bash
docker-compose up -d
docker-compose run --rm certbot certonly --webroot --webroot-path=/var/lib/letsencrypt -d sweets.promo
docker-compose down
docker-compose up -d