from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from dotenv import load_dotenv, find_dotenv
import os 
from datetime import datetime as dt
from models import Clients, Projects, Employees, Tasks, prepopulateDatabase, getSesssion
import requests 

import numpy as np
import matplotlib.pyplot as plt 
import io
import base64

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
    # results = retrieve(Clients, "all")
    results = Clients.query.all()
    columns = Clients.__table__.columns.keys() # https://stackoverflow.com/questions/6455560/how-to-get-column-names-from-sqlalchemy-result-declarative-syntax

    return render_template("retrieve.j2", entity="Clients", data=[columns, results]) #data=[columns, results] 

@app.route('/clients/create',methods=["GET", "POST"])
def clientsCreate():
    if request.method == "GET":
        results = Clients.query.all()
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
        print(formData)

        #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
 
        task = Tasks(projectId=formData[0], 
                taskDescription=formData[1], 
                taskDate=str(formData[2]),
                taskTime=formData[3],
                eeId=formData[4]
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
    
    #note there is a difference between request.json and request.json

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
                                taskDate=request.json['taskDate'],
                                taskTime=request.json['taskTime'],
                                eeId=request.json['eeId'] 
                            )
        
    elif entity == "employees":
        newEntity = entityObj(  eeFirstName=request.json['eeFirstName'],
                                eeLastName=request.json['eeLastName'],
                                eePosition=request.json['eePosition'],
                                eeStatus=request.json['eeStatus']

                            )
    # add and commit the change, return a success code 
    session.add(newEntity)
    session.commit()
    return (jsonify({entity:[request.json]}),201)

# ------- retrieve -------

@app.route('/api/<entity>/retrieve',methods=["GET"])
def apiRetrieve(entity, internal=None):

    # map passed entity to db object 
    entityObj = mapEntity(entity) 

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
                    print("**",query)
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

    # map passed entity to db object, extract entityIdKey, entityIdVal
    entityObj = mapEntity(entity) 
    entityIdKey =  str(list(request.args.keys())[0]) 
    entityIdVal = str(request.args[list(request.args.keys())[0]])

    # Extract object attribute from entityObj for the entityIdKey
    attr = getattr(entityObj,entityIdKey)
    session = getSesssion()
    # Pass request.json form directly to query/update
    entityObj.query.filter(attr==entityIdVal).update(request.json)
    # Look up updated record to return in response 
    query = entityObj.query.filter(attr==entityIdVal).first().getData()
    # Commit change 
    session.commit()

    return (jsonify(query),200)
    

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


# ---------- FAQ ---------- 
@app.route('/faq',methods=["GET"])
def appFaq():
    if request.method == "GET": 
            return render_template("faq.j2", entity="Help")


# ---------- Confirmation ---------- 
@app.route('/confirmation',methods=["GET"])
def confirmation():
    if request.method == "GET": 
            return render_template("confirmation.j2")

# ---------- Reports ---------- s

def serve_img(plt):
    """
    Take image plot (matplotlib currently), return HTML img element with in-memory image

    Keyword arguments:
    plt -- the graph object

    Sourced from: 
    https://blog.furas.pl/python-flask-how-to-use-bytesio-in-flask-to-display-matplotlib-image-without-saving-in-file-gb.html
    """
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return f'<img src="data:image/png;base64,{plot_url}">'


@app.route('/reports',methods=["GET"])
def reports():

    # Landing page
    if request.method == "GET" and len(request.args) == 0:
        #tables = db.engine.table_names()
        print("THIS")
        return render_template("reports.j2", entity="reports", reportEntity=None)

    # Specific reports
    # Request format: http://localhost:5000/reports?entity=tasks&projectId=2
    elif request.method == "GET" and len(request.args) >= 1: 

        # Extract entity from URL          
        reportEntity = request.args[str(list(request.args)[0])]

        # intersecting entity ID, e.g., reporting tasks by project, projectId is intersecting
        idKey = str(list(request.args)[1])
        idVal = str(request.args[idKey])
        
        # query db by the intersectId and value to obtain data in json 
        data = requests.get(f'http://localhost:5000/api/{reportEntity}/retrieve?{idKey}={idVal}').json()[reportEntity]
        
        # convert dict to list of dates and times sorted by date
        taskDatesTimes = sorted({task['taskDate']:task['taskTime'] for task in data}.items(), key=lambda item:item[0])
        print(taskDatesTimes)

        # declare x and y arrays, prepare graph  
        x = np.array([i[0] for i in taskDatesTimes])
        y = np.array([i[1] for i in taskDatesTimes])
        plt.bar(x, y, color="#FCB35F")
        plt.xlabel("Date")
        plt.ylabel("Hours")
        # plt.savefig("static/plot.jpeg")

        img = serve_img(plt)


        # graphingPayload = { "graph_type": "line",
        #                     "graph_height": 400, 
        #                     "graph_width": 600, 
        #                     "x_axis": str(list(taskDates)), 
        #                     "y_axis": str(list(taskTimes)),
        #                     "export_type": "jpeg",
        #                     "export_location": "export.jpeg",
        #                     "graph_title": "report",
        #                     "x_axis_label": "Date",
        #                     "y_axis_label": "Amount"
        #                     }

        # payload = json.loads(graphingPayload)
        return render_template("reports.j2", idKey=idKey, data=data, img=serve_img(plt), entity="reports", reportEntity="tasks") #data=[taskDates,taskTimes]

    # Reports Notes
        # consider adding granularity 
        # supports:  
        #   tasks by project: 'http://localhost:5000/reports/tasks?projectId=1'

        # demo'd proof of concept with plotly and dropping jpegs
        # into static directory. 

        # as opposed to creating JPEG each time, can do one in memory
        # and server per https://stackoverflow.com/questions/25140826/generate-image-embed-in-flask-with-a-data-uri 
        # another example: https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser 
        # pull out the intersecting entity id (e.g., tasks by projectId, tasks by eeId) 

# ---------- Reports ---------- 
@app.route('/reports/client',methods=["GET"])
def reportsClient():
    r = requests.get('http://localhost:5000/api/tasks/retrieve?projectId=1')
    print(r.text)
    return r.text




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    host = 'localhost.'
    app.run(host=host,port=port, debug=True)