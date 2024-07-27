#!/bin/bash

# Execute keyword_mapping.py
python keyword_mapping.py

# Start your Flask application with Gunicorn
gunicorn -b 0.0.0.0:4000 app:app
