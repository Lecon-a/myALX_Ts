from email.policy import default
import os
from tkinter import CASCADE
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
import secret as s
from flask_migrate import Migrate

database_path = "postgresql://{0}@{1}/{2}".format(
    s.credentials,
    s.address,
    s.database_name
)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db


'''
User, Question, Category

'''


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'score': self.score
        }

    def uid(self):
        return {'id':self.id}  


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(Integer, ForeignKey('categories.id'))
    difficulty = Column(Integer)
    rating = Column(Integer)

    def __init__(self, question, answer, category, difficulty, rating):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty,
            'rating': self.rating
        }


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = db.relationship(Question, backref=(
        'categories'), cascade='all, delete', lazy=True)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }

    def ctype(self):
        return self.type

    def cid(self):
        return self.id
