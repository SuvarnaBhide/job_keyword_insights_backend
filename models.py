from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Quiz(db.Model):
    __tablename__ = 'Quiz'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)

class Question(db.Model):
    __tablename__ = 'Question'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    content = db.Column(db.Text, nullable=False)
    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))

class MCQOption(db.Model):
    __tablename__ = 'MCQ_Option'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    option_label = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.String(255))
    question = db.relationship('Question', backref=db.backref('options', lazy=True))
    __table_args__ = (
        db.UniqueConstraint('question_id', 'option_label'),
    )

class Attempt(db.Model):
    __tablename__ = 'Attempt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    attemptDate = db.Column(db.DateTime)
    user = db.relationship('User', backref=db.backref('attempts', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('attempts', lazy=True))

class Response(db.Model):
    __tablename__ = 'Response'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('Attempt.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('MCQ_Option.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('Question.id'))
    content = db.Column(db.String(255))
    attempt = db.relationship('Attempt', backref=db.backref('responses', lazy=True))
    option = db.relationship('MCQOption')
    question = db.relationship('Question', backref=db.backref('responses', lazy=True))