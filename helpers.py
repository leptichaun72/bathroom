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
def setup():
    bg = Person(name="BG")
    alan = Person(name="Alan")
    brian = Person(name="Brian")
    db.session.add_all([bg,alan,brian])
    db.session.commit()
