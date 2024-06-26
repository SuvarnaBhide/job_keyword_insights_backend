#!/bin/bash

# Install SpaCy model if not already installed
python -m spacy download en_core_web_sm

# Run the preliminary script
python keyword_mapping.py

# Run the Flask app
python app.py