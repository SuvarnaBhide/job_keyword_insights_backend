import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:cycle123@localhost:3306/QUIZ_SCHEMA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False