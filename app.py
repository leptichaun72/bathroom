### sqlAlchemy HELPERS
def lclass():
    print db.engine.table_names()
def lfield(classname):
    print classname.__table__.columns.keys()
def getall(classname):
    print classname.query.all()
def getdate():
    return datetime.now().strftime("%b %d %Y %X")
def table(tablename):
    prompt = input("Enter 1.Create table \
2.Delete table: ")
    if prompt==1:
        tablename.__table__.create(db.engine)
    elif prompt==2:
        tablename.__table__.drop(db.engine)
    else:
        print "Try Again"

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
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://llzzgrcd:iRMc90xCWyHxUcUhhmXxmt7SRB6WKQ2k@otto.db.elephantsql.com:5432/llzzgrcd"

db = SQLAlchemy(app)

### MODELS
class Person(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),unique=True,nullable=False)
    memo = db.Column(db.String(25))
    uses = db.relationship("Use", backref="person", lazy=True)

    def __repr__(self):
        return "<PERSON %r>" % self.name

class Use(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    start = db.Column(db.DateTime,nullable=False)
    finish = db.Column(db.DateTime)

    @property
    def startime(self):
        return self.start.strftime("%b %-d '%y %-I:%M:%S %p")
        #return self.start.isoformat()

    def __repr__(self):
        return "<USE starts at %r>" % self.start

###ROUTES
@app.route("/")
def index():
    people = Person.query.join(Use).all()
    return render_template("index.html", people=people)

###RUN
app.run(debug=True)
