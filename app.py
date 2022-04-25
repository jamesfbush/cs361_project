from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv, find_dotenv
import os 
from models import Clients, Projects, Employees, Tasks, prepopulateDatabase 


# Flask object
app = Flask(__name__)
# # https://flask.palletsprojects.com/en/2.1.x/tutorial/layout/ 
# Based off of this intro 
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

# Configure database 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{passwd}@{host}/{db}' # MySQL

# Other db config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Declare db
db = SQLAlchemy(app)

# Set up dummy data 
prepopulateDatabase()



# CRUD operations 
# def create():
# def retrieve():
# def update(): 
# def delete(): 



# ---------- Home ---------- 
@app.route('/',methods=["GET"])
def home():
    if request.method == "GET": 
            return render_template("main.j2",entity="Home") 


# ---------- Clients ---------- 
@app.route('/clients',methods=["GET"])
def clients():
    return render_template("main.j2", entity="Clients")

@app.route('/clients/retrieve',methods=["GET"])
def clientsRetrieve():
    results = Clients.query.all()
    columns = Clients.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

    return render_template("retrieve.j2", entity="Clients", data=[columns, results]) #data=[columns, results] 

@app.route('/clients/create',methods=["GET", "POST"])
def clientsCreate():
    if request.method == "GET":
        # results = Clients.query.all()
        columns = Clients.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

        return render_template("create.j2", entity="Clients", data=[]) #data=[columns, results] 

    if request.method == "POST":
        formData = list(request.form.values())

        #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
 
        client = Clients(clientOrganizationName=formData[0], 
                clientContactFirstName=formData[1], 
                clientContactLastName=formData[2],
                clientContactEmail=formData[3]
            )
        db.session.add(client)
        db.session.commit()
        
        return render_template("create.j2", entity="Clients", data="success")



# ---------- Projects ---------- 
@app.route('/projects',methods=["GET"])
def projects():
    if request.method == "GET": 
            return render_template("main.j2",entity="Projects")

@app.route('/projects/retrieve',methods=["GET"])
def projectsRetrieve():
    results = Projects.query.all()
    columns = Projects.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax
    print(columns)
    return render_template("retrieve.j2", entity="Projects", data=[columns, results]) #data=[columns, results] 

@app.route('/projects/create',methods=["GET", "POST"])
def projectsCreate():
    if request.method == "GET":
        # results = Projects.query.all()
        columns = Projects.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

        return render_template("create.j2", entity="Projects", data=[]) #data=[columns, results] 

    if request.method == "POST":
        formData = list(request.form.values())

        #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
 
        project = Projects(clientId=formData[0], 
                projectDescription=formData[1], 
                projectBillRate=formData[2]
            )
        db.session.add(project)
        db.session.commit()
        
        return render_template("create.j2", entity="Projects", data="success")



# ---------- Employees ---------- 
@app.route('/employees',methods=["GET"])
def employees():
    if request.method == "GET": 
            return render_template("main.j2", entity="Employees")

@app.route('/employees/retrieve',methods=["GET"])
def employeesRetrieve():
    results = Employees.query.all()
    columns = Employees.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax
    print(columns)
    return render_template("retrieve.j2", entity="Employees", data=[columns, results]) #data=[columns, results] 

@app.route('/employees/create',methods=["GET", "POST"])
def employeesCreate():
    if request.method == "GET":
        # results = Projects.query.all()
        columns = Employees.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

        return render_template("create.j2", entity="Employees", data=[]) #data=[columns, results] 

    if request.method == "POST":
        formData = list(request.form.values())

        #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
 
        ee = Employees(eeFirstName=formData[0], 
                eeLastName=formData[1], 
                eePosition=formData[2],
                eeStatus=bool(formData[3])
            )
        db.session.add(ee)
        db.session.commit()
        
        return render_template("create.j2", entity="Employees", data="success")


# ---------- Tasks ---------- 

@app.route('/tasks',methods=["GET"])
def tasks():
    if request.method == "GET": 
            return render_template("main.j2", entity="Tasks")

@app.route('/tasks/retrieve',methods=["GET"])
def tasksRetrieve():
    results = Tasks.query.all()
    columns = Tasks.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax
    print(columns)
    return render_template("retrieve.j2", entity="Tasks", data=[columns, results]) #data=[columns, results] 


@app.route('/tasks/create',methods=["GET", "POST"])
def tasksCreate():
    if request.method == "GET":
        # results = Projects.query.all()
        columns = Tasks.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

        return render_template("create.j2", entity="Tasks", data=[]) #data=[columns, results] 

    if request.method == "POST":
        formData = list(request.form.values())

        #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
 
        task = Tasks(projectId=formData[0], 
                taskDescription=formData[1], 
                taskTime=formData[2],
                eeId=formData[3]
            )
        db.session.add(task)
        db.session.commit()
        
        return render_template("create.j2", entity="Tasks", data="success")



# ---------- Help ---------- 
@app.route('/help',methods=["GET"])
def appHelp():
    if request.method == "GET": 
            return render_template("help.j2", entity="Help")

# ---------- Help ---------- 
@app.route('/faq',methods=["GET"])
def appFaq():
    if request.method == "GET": 
            return render_template("faq.j2", entity="Help")



@app.route('/confirmation',methods=["GET"])
def confirmation():
    if request.method == "GET": 
            return render_template("confirmation.j2")






if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost.',port=port, debug=True)