from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quiz(db.Model):
    __tablename__ = 'Quiz'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # Define the relationship with Question and Attempt and use cascade delete
    questions = db.relationship('Question', backref='quiz', cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', backref='quiz', cascade='all, delete-orphan')

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)

    # Define the relationship with Attempt and use cascade delete
    attempts = db.relationship('Attempt', backref='user', cascade='all, delete-orphan')

class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    content = db.Column(db.Text, nullable=False)

    # Define the relationship with MCQOption and use cascade delete
    options = db.relationship('MCQOption', backref='question', cascade='all, delete-orphan')

class MCQOption(db.Model):
    __tablename__ = 'MCQ_Option'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    option_label = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.String(255))

    __table_args__ = (
        db.UniqueConstraint('question_id', 'option_label'),
    )

class Attempt(db.Model):
    __tablename__ = 'Attempt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    attemptDate = db.Column(db.DateTime)

    # Define the relationship with Response and use cascade delete
    responses = db.relationship('Response', backref='attempt', cascade='all, delete-orphan')

class Response(db.Model):
    __tablename__ = 'Response'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('Attempt.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('MCQ_Option.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    content = db.Column(db.String(255))

    # Define relationships without cascade delete, as these are covered by parent delete
    option = db.relationship('MCQOption', backref=db.backref('responses', lazy=True))
    question = db.relationship('Question', backref=db.backref('responses', lazy=True))
