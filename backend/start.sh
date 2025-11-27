#!/usr/bin/env bash
# Start script for Render (or other hosts) to run the Flask app via Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:$PORT app:app
