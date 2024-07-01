from flask_pymongo import pymongo
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB URI from environment variables
mongo_uri = os.getenv('MONGODB_URI')

client = pymongo.MongoClient(mongo_uri)

db = client.get_database('job_insights')

user_collection = pymongo.collection.Collection(db, 'job_keywords')