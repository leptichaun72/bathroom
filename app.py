### PACKAGES
import os

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for

### APP
project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir, "usetoilet.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db = SQLAlchemy(app)

### MODELS
class Person(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable=False)
    memo = db.Column(db.String(25))
    uses = db.relationship("Use", backref="person", lazy=True)

    def __repr__(self):
        return "<PERSON %r>" %self.name

class Use(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    start_time = db.Column(db.DateTime,nullable=False)
    finish_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<USE starts at %r>" %self.start_time

###ROUTES
@app.route("/")
def index():
    return render_template("index.html")

###RUN
app.run(debug=True)
