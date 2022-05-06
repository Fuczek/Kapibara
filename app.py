from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7733@localhost/'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dwwbeuabioltay:325b35fadbe4c8543523180ec68c640b0c426ae0ed37b805a285d096d0827385@ec2-52-3-200-138.compute-1.amazonaws.com:5432/d9ugl6a69dmrs1'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    subjects = db.relationship('Subject', backref='faculty')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    equations = db.relationship('Equation', backref='subject')

class Equation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    mathematics = db.Column(db.String(200), nullable=False)
    votes = db.Column(db.Integer, default = 0, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    components = db.relationship('Component', backref='equation')

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    constant = db.Column(db.String(10), nullable=False)
    equation_id = db.Column(db.Integer, db.ForeignKey('equation.id'))