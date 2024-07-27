import os
import csv
import random
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from config import Config
from models import db, Quiz, Question, MCQOption

# Load environment variables from the .env file
load_dotenv()

database_uri = Config.SQLALCHEMY_DATABASE_URI

# Create an SQLAlchemy engine and session
engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)
session = Session()

# Define the CSV file path
csv_file_path = 'quiz_csvs/Thermodynamics.csv'

# Extract quiz name from the CSV file name
quiz_name = os.path.splitext(os.path.basename(csv_file_path))[0]

# Function to get the next available ID for a table
def get_next_id(table):
    max_id = session.query(func.max(table.id)).scalar()
    return (max_id or 0) + 1

# Insert a new quiz
new_quiz = Quiz(name=quiz_name, description=f'A quiz about {quiz_name}')
session.add(new_quiz)
session.commit()

quiz_id = new_quiz.id

# Read the CSV file and generate the SQL for inserting questions and options
with open(csv_file_path, 'r', newline='') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        question_content = row['Question']

        # Assign options to a dictionary, correct answer is appended as the last option
        options = [row['Option1'], row['Option2'], row['Option 3'], row['CorrectAnswer']]
        
        # Define the option labels
        option_labels = ['A', 'B', 'C', 'D']

        # Insert the question
        new_question = Question(quiz_id=quiz_id, content=question_content)
        session.add(new_question)
        session.commit()

        question_id = new_question.id

        # Insert the options
        for label, option_content in zip(option_labels, options):
            if option_content:  # Only add options if the content is not empty
                is_correct = (label == 'D')
                new_option = MCQOption(
                    question_id=question_id,
                    option_label=label,
                    is_correct=is_correct,
                    content=option_content
                )
                session.add(new_option)
        session.commit()

# Close the session
session.close()
