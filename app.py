### sqlAlchemy HELPERS
def lclass():
    print db.engine.table_names()
def lfield(classname):
    print classname.__table__.columns.keys()
def getall(classname):
    print classname.query.all()
def getdate():
    return datetime.now().strftime("%b %d %Y %X")
def modtable(tablename):
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

elephantdb = "postgres://llzzgrcd:iRMc90xCWyHxUcUhhmXxmt7SRB6WKQ2k@otto.db.elephantsql.com:5432/llzzgrcd"
herokudb = "postgres://nyujdikmxeclmz:eca2da8f584812b64eea2fee888196c41ec538442d04709a9dcbdf80299a4bd1@ec2-54-161-58-21.compute-1.amazonaws.com:5432/df3nii1veq5dub"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = elephantdb
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

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
    start = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    finish = db.Column(db.DateTime,)

    @property
    def _start_datetime(self):
        return self.start.strftime("%b %-d '%y %-I:%M:%S %p")
        #return self.start.isoformat()

    @property
    def _start_date(self):
        return self.start.strftime("%b %-d '%y")
    @property
    def _start_time(self):
        return self.start.strftime("%-I:%M:%S %p")
    @property
    def _finish_date(self):
        return self.finish.strftime("%b %-d '%y")
    @property
    def _finish_time(self):
        return self.finish.strftime("%-I:%M:%S %p")

    def __repr__(self):
        return "<USE starts at %r>" % self.start

###ROUTES
@app.route("/")
def index():
    try:
        people = Person.query.all()
    except:
        return "<h1>There was an issue loading landing page</h1>"
    return render_template("index.jade", people=people)
@app.route("/create/<int:personid>/<int:mode>")
def create(personid, mode):
    if(mode == 1):
        use = Use(person_id=personid)  
        db.session.add(use)
    else:
        lastentry = Person.query.filter_by(id=personid).first().uses[-1]
        if(bool(lastentry.finish) == False):
            lastentry.finish = datetime.utcnow()

    db.session.commit()
    return redirect('/')
@app.route("/tehe")
def tehe():
    people = Person.query.join(Use).all()
    return render_template("tehe.html", people=people)

###RUN
app.run(debug=True)
