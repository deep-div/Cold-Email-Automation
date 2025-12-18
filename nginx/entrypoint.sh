#!/bin/sh
set -e

if [ "$ENV" = "prod" ]; then
  cp /etc/nginx/templates/prod.conf /etc/nginx/conf.d/default.conf
else
  cp /etc/nginx/templates/dev.conf /etc/nginx/conf.d/default.conf
fi

exec "$@"