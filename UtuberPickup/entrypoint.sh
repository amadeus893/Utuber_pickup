#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#cron setting
busybox crond -b -L /dev/stderr

#python manage.py flush --no-input
#python manage.py migrate --fake myrestapi zero
#python manage.py makemigrations
#python manage.py migrate --fake-initial
python manage.py migrate

exec "$@"


