from flask import Flask, render_template, request, jsonify, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)


ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7733@localhost/'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ysqhybqlcowgnm:248a0d1a82842826da4cdcff82418db36b34b7ec776d220240123256ea5ebb60@ec2-54-172-175-251.compute-1.amazonaws.com:5432/d4v03hmlietk8t'

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/ajaxlivesearch", methods = ["POST", "GET"])
def ajaxlivesearch():
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == "":
            equations = Equation.query.order_by(Equation.votes.desc()).all()
            return jsonify({'htmlresponse2': render_template('nothing.html')})
        else:
            equations = Equation.query.filter(or_(Equation.mathematics.ilike('%'+ search_word + '%'), Equation.name.ilike('%'+ search_word + '%'))).order_by(Equation.votes.desc()).all()   
            numrows = len(equations)
            return jsonify({'htmlresponse': render_template('response.html', equations=equations, numrows=numrows)})

@app.route("/ajaxvote/<int:id>", methods = ["GET", "POST"])
def ajaxvote(id):
    if request.method == "POST":
            equation = Equation.query.filter_by(id=id).first()
            equation.votes = equation.votes + 1
            
            try:
                db.session.commit()
                return ('', 204)
            except:
                return 'woops'



if __name__ == "__main__":
    app.run(port=8080, debug=True)
