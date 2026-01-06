#!/bin/bash
set -e

echo "Waiting for database to be ready..."
python << END
import sys
import os
import time
import psycopg2
from psycopg2 import OperationalError

max_retries = 30
retry_delay = 2

db_name = os.environ.get('DATABASE_NAME', 'postgres')
db_user = os.environ.get('DATABASE_USER', 'postgres')
db_password = os.environ.get('DATABASE_PASSWORD', 'dz-fit')
db_host = os.environ.get('DATABASE_HOST', 'db')
db_port = os.environ.get('DATABASE_PORT', '5432')

for i in range(max_retries):
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.close()
        print("Database is ready!")
        sys.exit(0)
    except OperationalError:
        if i < max_retries - 1:
            print(f"Database not ready, waiting... ({i+1}/{max_retries})")
            time.sleep(retry_delay)
        else:
            print("Database connection failed after max retries")
            sys.exit(1)
END

echo "Running migrations..."
python back/manage.py migrate --noinput

echo "Starting application..."
exec "$@"