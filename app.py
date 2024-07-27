import csv
import os
# import db
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from keyword_mapping import keyword_counts, load_keyword_data, keyword_output_dir
from models import db, Quiz, User, Question, MCQOption, Attempt, Response
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize SQLAlchemy with Flask app
db.init_app(app)

def initialize_database():
    with app.app_context():
        db.create_all()

# Manually call initialization function
initialize_database()

# GET API for returning quizzes
@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = Quiz.query.all()
    results = [{'id': quiz.id, 'name': quiz.name, 'description': quiz.description} for quiz in quizzes]
    return jsonify(results)

# GET API for returning questions
@app.route('/api/<int:quiz_id>/questions', methods=['GET'])
def get_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    results = []
    
    for question in questions:
        options = [{'id': opt.id, 'label': opt.option_label, 'is_correct': opt.is_correct, 'content': opt.content, 'explanation': opt.explanation} for opt in question.options]
        
        # Find the index of the correct option using a simple loop
        correct_option_index = -1
        for i, opt in enumerate(question.options):
            if opt.is_correct:
                correct_option_index = i
                break
        
        results.append({
            'id': question.id,
            'quiz_id': question.quiz_id,
            'content': question.content,
            'options': options,
            'correctOptionIndex': correct_option_index
        })

    return jsonify(results)

# POST API for submitting an attempt
@app.route('/api/attempts', methods=['POST'])
def submit_attempt():
    data = request.json
    user_id = data['user_id']
    quiz_id = data['quiz_id']
    
    # Get the current date and time
    attempt_date = datetime.now().strftime('%d %B %Y, %I:%M %p')
    
    # Create a new attempt in the database
    attempt = Attempt(user_id=user_id, quiz_id=quiz_id, attemptDate=datetime.now())
    db.session.add(attempt)
    db.session.commit()
    
    # Add responses to the database from the request data (data['details'])
    for detail in data['details']:
        response = Response(
            attempt_id=attempt.id,
            question_id=detail['question_id'],
            option_id=detail['option_id'],
            content=','.join(map(str, detail['order']))
        )
        db.session.add(response)
    
    db.session.commit()
    return jsonify({'message': 'Attempt submitted successfully', 'attemptDate': attempt_date}), 201

# GET API for returning attempts
@app.route('/api/attempts/<int:user_id>', methods=['GET'])
def get_attempts(user_id):
    
    # Fetch attempts sorted by attemptDate in descending order
    attempts = Attempt.query.filter_by(user_id=user_id).order_by(Attempt.attemptDate.desc()).all()
    results = []

    # Fetch responses for each attempt
    for attempt in attempts:
        responses = Response.query.filter_by(attempt_id=attempt.id).all()
        response_results = []

        for response in responses:
            option_order = response.content.split(',') if response.content else []
            response_results.append({
                'question_id': response.question_id,
                'option_id': response.option_id,
                'content': response.content,
                'option_order': option_order  # Include the shuffled order
            })
        
        # Calculate quizScore
        total_questions = len(attempt.quiz.questions)
        correct_answers = 0
        for response in responses:
            option = MCQOption.query.get(response.option_id)
            if option.is_correct:
                correct_answers += 1
        quiz_score = f"{correct_answers}/{total_questions}" if total_questions > 0 else 0
        
        results.append({
            'id': attempt.id,
            'quiz_id': attempt.quiz_id,
            'quizName': attempt.quiz.name,
            'quizScore': quiz_score,
            'attemptDate': attempt.attemptDate.strftime('%d %B %Y, %I:%M %p'),  # Format the date
            'responses': response_results
        })

    return jsonify(results)

# Route for the home page
@app.route('/')
def flask_mongodb_atlas():
    return "This is a Python Flask application!"

# Route for returning keyword counts
@app.route('/api/keyword_counts', methods=['GET'])
def get_keyword_counts():
    return jsonify(keyword_counts)

@app.route('/api/keyword/<keyword>', methods=['GET'])
def get_keyword_data(keyword):
    # Load keyword data from CSV file
    keyword_data = load_keyword_data(keyword, keyword_output_dir)
    return jsonify(keyword_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)



