### PACKAGES
import os

from datetime import datetime
from pytz import timezone
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for

### APP
# define eastern timezone
eastern = timezone('US/Eastern')

project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir, "usetoilet.db"))

elephantdb = "postgres://llzzgrcd:iRMc90xCWyHxUcUhhmXxmt7SRB6WKQ2k@otto.db.elephantsql.com:5432/llzzgrcd"
herokudb = "postgres://nyujdikmxeclmz:eca2da8f584812b64eea2fee888196c41ec538442d04709a9dcbdf80299a4bd1@ec2-54-161-58-21.compute-1.amazonaws.com:5432/df3nii1veq5dub"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = herokudb
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
    start = db.Column(db.DateTime(timezone=True),nullable=False,default=datetime.utcnow())
    finish = db.Column(db.DateTime(timezone=True),)

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
        db.create_all()
        people = Person.query.all()
    except:
        return "<h1>There was an issue loading landing page</h1>"
    return render_template("index.jade", people=people)
@app.route("/create/<int:personid>/<int:mode>")
def create(personid, mode):
    if(mode == 1):
        use = Use(person_id=personid,start=datetime.now(eastern))  
        db.session.add(use)
    else:
        lastentry = Person.query.filter_by(id=personid).first().uses[-1]
        if(bool(lastentry.finish) == False):
            lastentry.finish = datetime.now(eastern)

    db.session.commit()
    return redirect('/')
@app.route("/tehe")
def tehe():
    people = Person.query.join(Use).all()
    return render_template("tehe.html", people=people)

###RUN
if __name__ == "__main__":
    app.run(debug=True)
