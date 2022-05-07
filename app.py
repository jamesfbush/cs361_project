from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv, find_dotenv
import os 
from datetime import datetime as dt
from models import Clients, Projects, Employees, Tasks, prepopulateDatabase, getSesssion


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



# CRUD operations? 


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
    results = retrieve(Clients, "all")
    # results = Clients.query.all()
    columns = Clients.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

    return render_template("retrieve.j2", entity="Clients", data=[columns, results]) #data=[columns, results] 

@app.route('/clients/create',methods=["GET", "POST"])
def clientsCreate():
    if request.method == "GET":
        # results = Clients.query.all()
        columns = Clients.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

        return render_template("create.j2", entity="Clients", data=[]) #data=[columns, results] 

    if request.method == "POST":
        formData = list(request.json.values())

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
        formData = list(request.json.values())

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
        formData = list(request.json.values())

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
        formData = list(request.json.values())

        #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
 
        task = Tasks(projectId=formData[0], 
                taskDescription=formData[1], 
                taskTime=formData[2],
                eeId=formData[3]
            )
        db.session.add(task)
        db.session.commit()
        
        return render_template("create.j2", entity="Tasks", data="success")


# ---------- API ---------- 
def mapEntity(entity):
    # map passed entity to db object 
    entityDict = {  'tasks':Tasks, 
                    'projects':Projects, 
                    'clients':Clients, 
                    'employees':Employees
                }
    return entityDict[entity]

# ------- timeDelta -------
@app.route('/api/timeDelta',methods=["GET"])
def timeDeltaAPI():

    if request.method == "GET": 
        if len(request.args) > 0:
            # Extract startTime and endTime from API call  
            startTime = dt.fromtimestamp(int(request.args['startTime']))
            endTime = dt.fromtimestamp(int(request.args['endTime'] ))

            # Calculate the timeDelta down to total seconds 
            totalSeconds = int((endTime - startTime).total_seconds()) 

            # Calculate days, hours, minutes, seconds for dict
            timeDelta = {"timeDelta": { "days": totalSeconds // (60*60*24),
                                        "hours": (totalSeconds - (totalSeconds // (60*60*24))*60*60*24) // (60*60),
                                        "minutes": (totalSeconds % 3600) // 60,
                                        "seconds": totalSeconds % 60
                                    }
                        }
            # Return JSON 
            return jsonify(timeDelta)
        else:
            return ("Call API in following format:<br><br>\
                '.../api/timeDelta?startTime=1577865600&endTime=1641121445'<br><br>\
                    where startTime and endTime values are Unix timestamps.",404)

# ------- create -------
@app.route('/api/<entity>/create',methods=["POST"])
def apiCreate(entity):
    print(request.json) #note there is a difference between request.json and request.json
    # # Map passed entity to entityObj
    entityObj = mapEntity(entity)

    # # Get db session 
    session = getSesssion()

    # # # Declare the new entity to add 
    if entity == "clients":
        newEntity =  entityObj(clientOrganizationName=request.json['clientOrganizationName'], 
                            clientContactFirstName=request.json['clientContactFirstName'], 
                            clientContactLastName=request.json['clientContactLastName'], 
                            clientContactEmail=request.json['clientContactEmail']
                        )
    elif entity == "projects":
        newEntity = entityObj(  clientId=request.json['clientId'],
                                projectDescription=request.json['projectDescription'],
                                projectBillRate=request.json['projectBillRate']
                        )
    elif entity == "tasks":
        newEntity = entityObj(  projectId=request.json['projectId'],
                                taskDescription=request.json['taskDescription'],
                                taskTime=request.json['taskTime'],
                                eeId=request.json['eeId'] 
                            )
      
        
    elif entity == "employees":
        newEntity = entityObj(  )
        pass

    session.add(newEntity)
    session.commit()
    return str(request.json)

# ------- retrieve -------

@app.route('/api/<entity>/retrieve',methods=["GET"])
def apiRetrieve(entity):

    # map passed entity to db object 
    # entityDict = {  'tasks':Tasks, 
    #                 'projects':Projects, 
    #                 'clients':Clients, 
    #                 'employees':Employees
    #             }
    entityObj = mapEntity(entity) 

    if request.method == "GET": 

        # URL request to retrieveAll 
        if 'retrieveAll' in request.args.keys() and len(request.args.keys()) == 1:
            query = entityObj.query.all()
            results = {entity:[i.getData() for i in query]}

            return (jsonify(results),200)

        # Retrieve based on URL-specified filter 
        elif len(request.args.keys()) >= 1:

            # Set relevant entity columns 
            cols = entityObj.__table__.columns.keys()

            # Extract attributes passed in URL to set filter cols 
            filters = [col for col in request.args.keys() if col in cols]
            if len(filters) > 0:
                # Declare results 
                results = {entity:[]}
                
                # Query db based on attributes/values in URL
                for i in filters:
                    # Attribute passed in URL 
                    attr = getattr(entityObj,i) 
                    #  Value passed in URL 
                    val = request.args[i] 
                    # Numeric values require exact match
                    if val.isnumeric():
                        query = entityObj.query.filter(attr==val).all()
                    # Non-numeric values allow like match
                    elif val.isnumeric() is False:
                        query = entityObj.query.filter(attr.like(f'%{val}%')).all()
                    # Add each unique query result to results dict
                    for result in query:
                        if result not in results[entity] and i is not None:
                            results[entity].append(result.getData())
                # No results, return 204 Not Found 
                if len(results[entity]) == 0:
                    return (jsonify(results),204)
                # Results found, return 200
                return (jsonify(results),200)

            # Else, return error 
            return ("ERROR: malformed request",404)


# ------- update -------
@app.route('/api/<entity>/update',methods=["PUT"])
def apiUpdate(entity):
    pass

# ------- delete -------
@app.route('/api/<entity>/delete',methods=["DELETE"])
def apiDelete(entity):
    # Map passed entity to a db entity 
    entityObj = mapEntity(entity)

    entityIdKey = list(request.args.keys())[0]

    attr = getattr(entityObj,list(request.args.keys())[0])

    entityIdVal = request.args[entityIdKey]

    query = entityObj.query.filter(attr==1).first() #entityIdKey==int(entityIdVal)
    
    print("Deleting:",entityIdKey, entityIdVal)

    # Delete
    session = getSesssion()
    session.delete(query)
    session.commit()

    return (jsonify("deleted"),200)


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


# ---------- Confirmation ---------- 
@app.route('/confirmation',methods=["GET"])
def confirmation():
    if request.method == "GET": 
            return render_template("confirmation.j2")






if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost.',port=port, debug=True)