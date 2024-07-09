import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB URI from environment variables
mysql_uri = os.getenv('MYSQL_URI')

class Config:
    SQLALCHEMY_DATABASE_URI = mysql_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False