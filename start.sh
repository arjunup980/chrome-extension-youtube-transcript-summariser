#!/bin/bash

# Start the Django application
gunicorn src.transcript.wsgi:application --bind=0.0.0.0:8000 --workers=4 --settings transcript.settings.production