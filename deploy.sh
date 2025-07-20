#!/bin/bash

echo "Starting deployment and testing..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run tests
echo "Running tests..."
python manage.py test

TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo "All tests passed! Deployment successful."
    exit 0
else
    echo "Tests failed! Deployment aborted."
    exit 1
fi
