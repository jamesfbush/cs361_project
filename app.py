from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy 
from model import Clients, Projects, Employees, Tasks, prepopulateDatabase, getSesssion
from upload import allowed_file, load_csv
from datetime import datetime as dt
import os
import csv
import requests 
import subprocess # Call to chart_ms
import json 
import time as tm

###############################
# ---------- CONFIG ----------
###############################

# Flask object
app = Flask(__name__)

# Configure, delcare, and prepopulate SQLite database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/timeTrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
prepopulateDatabase()

# Declare host name and port
host = 'localhost'
port = 5000

# For uploads, configure folder, allowed filetype, and max size
ALLOWED_EXTENSIONS = {'csv'} 
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 # i.e., max size is 16 kb

###############################
# ---------- HELPERS ----------
###############################

def mapStringToEntity(entity):
    """For CRUD workflow.
    Map passed entity to an object in db model.

    Keyword arguments:
    entity -- string representing entity in database
    """
    entityDict = {  'tasks':Tasks, 
                    'projects':Projects, 
                    'clients':Clients, 
                    'employees':Employees
                }
    return entityDict[entity]


def mapAttributesToString(entity,column=None):
    """For CRUD workflow. 
    Map entity and column strings to UI-friendly column descriptions. 

    Keyword arguments: 
    entity -- string representation of db object, e.g., "clients", "projects"
    column -- optional - will return a single column description 
    """

    stringDict = {  "clients":  {   'clientOrganizationName': 'Organization', 
                                    'clientContactFirstName': 'First name' ,
                                    'clientContactLastName': 'Last name',
                                    'clientContactEmail': 'Email'
                                },
                    "projects": {   'clientId': 'Client ID',
                                    'projectDescription': 'Description',
                                    'projectBillRate':'Bill rate'
                                },
                    "tasks":    {   'projectId': 'Project ID',
                                    'taskDescription': 'Description',
                                    'taskDate':'Date',
                                    'taskTime':'Time',
                                    'employeeId':'Employee ID'    
                                },
                    "employees":{   'employeeFirstName':'First name',
                                    'employeeLastName':'Last name',
                                    'employeePosition':'Position',
                                    'employeeStatus':'Status (current/former)'
                                }
                }
    if column is not None:
        return stringDict[entity][column]
    return stringDict[entity]


def allowed_file(filename):
	"""For CSV upload workflow. 
    Return True if file within allowed extensions, False if not.
	"""
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getChartFromMS(graphingPayload):
    """For reports/graphing workflow. 
    Create graphingPayload from passed dict, save to json, obtain
    jpeg image from chart_ms microservice, return link to image 
    to serve in report 

    Keyword arguments: 
    graphingPayload -- a dict with parameters to pass to chart_ms as json
    """

    # Save graphingPayload to json to microservice directory  
    with open('static/chart.json', 'w') as outfile:
        json.dump(graphingPayload, outfile)

    # Declare new graphFileName
    graphFileName = f"{graphingPayload['export_location']}.{graphingPayload['export_type']}"

    # Declare string of new html img element with src path for image 
    img = f'<img src="{graphFileName}">'

    sourcePath = f"{graphFileName}"

    # Call the graphing microservice as a separate subprocess 
    print('\n\033[2;1;32m **Calling chart_ms as separate subprocess, chart_ms.py...** \033[0;0m\n')
    subprocess.run("python3 chart_ms.py",shell=True)
    print('\033[2;1;32m **Call to chart_ms complete...** \033[0;0m\n')

    return img

###############################
# ---------- ROUTES -----------
###############################

# ---------- UI - Main ---------- 
@app.route('/',methods=["GET"])
def home():
    """Render home page.
    """
    if request.method == "GET": 
            return render_template("main.j2",entity="Home") 


# ---------- UI - Entity landing ---------- 
@app.route('/<entity>',methods=["GET"])
def entityLanding(entity):
    """Render individual entity landing pages.

    Keyword arguments: 
    entity -- string, passed through URL, e.g., "Clients", "Tasks", etc.
    """
    return render_template("main.j2", entity=entity.title())


# ----------- UI/API - Retrieve ----------
@app.route('/api/<entity>/retrieve',methods=["GET"])
@app.route('/<entity>/retrieve',methods=["GET"])
def retrieveEntity(entity):
    """Perform retrieval for UI or API based on search parameters or 'retrieve all'.
    
    Keyword arguments: 
    entity -- string, passed through URL, e.g., "Clients", "Tasks", etc.
    """

    # map passed entity to db object 
    entityObj = mapStringToEntity(entity) 
    entityStr = entity
    columns = entityObj.__table__.columns.keys()
    colStrs = mapAttributesToString(entity) #dict - keys are col names and vals are col descriptions
    
    # UI - Landing page 
    if len(request.args) == 0 and "/api/" not in str(request.url_rule):  
        return (render_template("retrieve.j2", entity=entityStr, data=[columns], colStrs=colStrs),200)

    # UI / API - URL request to retrieveAll 
    elif 'retrieveAll' in request.args.keys() and len(request.args.keys()) == 1:
        query = entityObj.query.all()

        # API
        if "/api/" in str(request.url_rule):
            results = {entity:[i.getData() for i in query]}
            return (jsonify(results),200)
        # UI
        else: 
            results = query 
            return (render_template("retrieve.j2", entity=entityStr, data=[columns, results],colStrs=colStrs),200)

    # Retrieve based on URL-specified filter 
    elif "retrieveAll" not in request.args and len(request.args.keys()) >= 1:

        # Extract attributes passed in URL to set filter columns 
        filters = [col for col in request.args.keys() if col in columns and request.args[col] != ""]
        if len(filters) > 0:
            # Declare results - a bit different than above
            results = {entity:[]}
            # Query db based on attributes/values in URL
            for i in filters:
                # Attribute passed in URL 
                attr = getattr(entityObj,i) 
                val = request.args[i] 
                # Numeric values require exact match
                if val.isnumeric():
                    query = entityObj.query.filter(attr==val).all()
                # Non-numeric values allow like match
                elif val.isnumeric() is False:
                    query = entityObj.query.filter(attr.like(f'%{val}%')).all()
                # Add each unique query result to results dict
                # BUG is returning duplicates, e.g., query id=2 and org=Bat
                for result in query:
                    if result not in results[entity] and i is not None:
                        results[entity].append(result.getData())

            # No results 
            if len(results[entity]) == 0:
                # API - return 204 Not Found
                if "/api/" in str(request.url_rule):
                    return (jsonify(results),204)
                # UI
                else: 
                    results = results[entity]
                    return (render_template("retrieve.j2", entity=entityStr, data=results)) # Had to remove 204
                    
            # API - results found, return 200 Found
            if "/api/" in str(request.url_rule):
                return (jsonify(results),200)
            # UI 
            else:
                results = results[entity]
                return (render_template("retrieve.j2", entity=entityStr, data=[columns, results],colStrs=colStrs),200)

        # Else, for UI/API return 404 error 
        return ("ERROR: malformed request",404)


# ------- UI / API create -------
@app.route('/api/<entity>/create',methods=["POST"])
@app.route('/<entity>/create',methods=["GET", "POST"])
def createEntity(entity):
    """Create an instance of a database entity. 

    Keyword arguments: 
    entity -- string, passed through URL, e.g., "Clients", "Tasks", etc.
    """

    # Map passed entity to entityObj
    entityStr = entity
    entityObj = mapStringToEntity(entity)
    colStrs = mapAttributesToString(entity)

    # UI - landing page 
    if request.method == "GET":
        columns = Tasks.__table__.columns.keys() 
        return render_template("create.j2", entity=entity.title(), data=[]) #data=[columns, results] 

    # UI/API - create entity 
    elif request.method == "POST":
        # Get db session 
        session = getSesssion()

        # UI / API - extract form (UI) or json (API) data 
        if "/api/" in str(request.url_rule):
            formData = request.json
        else:
            formData = request.form 

        # Declare the new entityObj to add 
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
        if entity == "clients":
            newEntity =  entityObj( clientOrganizationName=formData['clientOrganizationName'], 
                                    clientContactFirstName=formData['clientContactFirstName'], 
                                    clientContactLastName=formData['clientContactLastName'], 
                                    clientContactEmail=formData['clientContactEmail']
                                )
        elif entity == "projects":
            newEntity = entityObj(  clientId=formData['clientId'],
                                    projectDescription=formData['projectDescription'],
                                    projectBillRate=formData['projectBillRate']
                                )
        elif entity == "tasks":
            newEntity = entityObj(  projectId=formData['projectId'],
                                    taskDescription=formData['taskDescription'],
                                    taskDate=formData['taskDate'],
                                    taskTime=formData['taskTime'],
                                    employeeId=formData['employeeId'] 
                                )
        elif entity == "employees":
            # Convert form data (string) to Python boolean 
            if formData['employeeStatus'].lower() == "true":
                employeeStatus = True
            elif formData['employeeStatus'].lower() == "false":
                employeeStatus = False
            newEntity = entityObj(  employeeFirstName=formData['employeeFirstName'],
                                    employeeLastName=formData['employeeLastName'],
                                    employeePosition=formData['employeePosition'],
                                    employeeStatus=employeeStatus
                                )
        # add and commit the change, return a success code 
        session.add(newEntity)
        session.commit()

        # API 
        if "/api/" in str(request.url_rule):
            return (jsonify({entity:[request.json]}),201)
        # UI 
        else:
            return render_template("create.j2", entity=entityStr, data="success", formData=formData, colStrs=colStrs)


# ------- update -------
@app.route('/api/<entity>/update',methods=["PUT"])
@app.route('/<entity>/update',methods=["GET", "POST"])
def updateEntity(entity):
    """Update an instance of a database entity. 

    Keyword arguments: 
    entity -- string, passed through URL, e.g., "Clients", "Tasks", etc.
    """

    # get entity db object and session
    entityObj = mapStringToEntity(entity) 
    session = getSesssion()

    # -------UI--------------
    if request.method == "GET":
        entityIdKey =  str(list(request.args.keys())[0]) 
        entityIdVal = str(request.args[list(request.args.keys())[0]])

        # Extract object attribute from entityObj for the entityIdKey
        attr = getattr(entityObj,entityIdKey)

        colStrs = mapAttributesToString(entity)
        query = entityObj.query.filter(attr==entityIdVal).first().getData()
        return render_template("update.j2",entity=entity, colStrs=colStrs, data=query, entityIdKey=entityIdKey, entityIdVal=entityIdVal)

    # -------UI--------------
    if request.method == "POST":
        entityIdKey = f'{entity[:-1]}Id'
        entityIdVal = request.form[entityIdKey]
        updateRecord = dict(request.form)
        
    # -------API--------------
    if request.method == "PUT":
        entityIdKey =  str(list(request.args.keys())[0]) 
        entityIdVal = str(request.args[list(request.args.keys())[0]])
        updateRecord = request.json

    # Extract object attribute from entityObj for the entityIdKey
    attr = getattr(entityObj,entityIdKey)
    # Pass request.json form directly to query/update
    entityObj.query.filter(attr==entityIdVal).update(updateRecord)
    # Look up updated record to return in response 
    query = entityObj.query.filter(attr==entityIdVal).first().getData()
    # Commit change 
    session.commit()

    if request.method == "POST":
        return render_template("update.j2",entity=entity, updated=True, updateRecord=updateRecord)
    return (jsonify(query),200)
        

# ------- delete -------
@app.route('/<entity>/delete',methods=["GET","POST"])
@app.route('/api/<entity>/delete',methods=["DELETE"])
def deleteEntity(entity):
    """Delete an instance of a database entity. 

    Keyword arguments: 
    entity -- string, passed through URL, e.g., "Clients", "Tasks", etc.
    """

    # UI - generate landing page with confirmation prompt 
    if request.method == "GET":
        render_template("delete.j2", entity=entity)

    # UI/API - Declare key, val, and map passed entity to a db entity 
    entityObj = mapStringToEntity(entity)
    entityIdKey = list(request.args.keys())[0]
    attr = getattr(entityObj,list(request.args.keys())[0])
    entityIdVal = request.args[entityIdKey]

    # Query the entity, copy the deleted record for UI display, and delete it
    query = entityObj.query.filter(attr==entityIdVal).first() #entityIdKey==int(entityIdVal)
    deleteRecord = str(query)
    session = getSesssion()
    session.delete(query)
    session.commit()

    # API
    if "/api/" in str(request.url_rule):
        return (jsonify("deleted"),200)
    # UI
    else:
        return render_template("delete.j2",entity=entity, deleteRecord=deleteRecord)


# ---------- UI - Help ---------- 
@app.route('/help',methods=["GET"])
def appHelp():
    """Render help section page."""
    if request.method == "GET": 
            return render_template("help.j2", entity="Help")


# ---------- UI - FAQ ---------- 
@app.route('/faq',methods=["GET"])
def appFaq():
    """Render FAQ section page."""
    if request.method == "GET": 
            return render_template("faq.j2", entity="Help")


# ---------- UI - Reports ----------
@app.route('/reports',methods=["GET"])
def reports():
    """Generate report, calling graphing microservice. 
    Supports:  

    tasks by project: 'http://localhost:5000/reports?reportEntity=tasks&projectId=2'
    """

    # Landing page
    if request.method == "GET" and len(request.args) == 0:
        return render_template("reports.j2", entity="reports", reportEntity=None)

    # Specific reports
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

        # declare x and y arrays, prepare graph  
        x = [i[0] for i in taskDatesTimes]
        y = [i[1] for i in taskDatesTimes]

        # Specs according to 
        graphingPayload = { "graph_type": "bar",
                            "graph_height": 400, 
                            "graph_width": 600, 
                            "x_axis": x, 
                            "y_axis": y,
                            "export_type": "jpeg",
                            "export_location": "static/report",
                            "graph_title": "report",
                            "x_axis_label": "Date",
                            "y_axis_label": "Hours",
                            }

        # see getChartFromMS
        img = getChartFromMS(graphingPayload)

        return render_template("reports.j2", idKey=idKey, data=data, img=img, entity="reports", reportEntity="tasks") #data=[taskDates,taskTimes]


# ------- API - timeDelta -------
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

# ---------- Upload --------------
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file(entity="upload"):
    """
    Render landing page with upload button for GET.
    Once file submitted with POST, check file validity;
    return error message if invalid file.
    Save valid file and return success message, if success. 
    """
    entity = "upload"
    # Landing page
    if request.method == 'GET':
        return render_template('upload.j2', entity=entity)
    elif request.method == 'POST':
        # Check post request has the file part
        if 'file' not in request.files:
            error = "no file part"
            return render_template("upload.j2", entity=entity, error=error) 
        file = request.files['file']
        # No file submitted 
        if file.filename == '':
            error = 'No selected file'
            return render_template("upload.j2", entity=entity, error=error)
        # Impermissible format 
        if not allowed_file(file.filename):
            error ="Error: not a .csv file."
            return render_template("upload.j2", entity=entity, error=error) 
        # Format OK, save, render upload success
        if file and allowed_file(file.filename):
            # Ensure secure file name used
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
            #Load csv
            csv = load_csv(filename)
            if csv is not False:

                # Attempt process 
                for i in csv['tasks']:
                    requests.post(f'http://{host}:{port}/api/tasks/create?', json=i)

                return render_template("upload.j2", entity=entity, success=True, filename=csv)
            else:
                error = "CSV not in correct format"
                return render_template("upload.j2", entity=entity, error=error) 

# ---------- Set Theme --------------
@app.route("/set")
@app.route("/set/<theme>")
def set_theme(theme="light"):
    """Upon request, set CSS to requested theme.
    # Adapted from: https://replit.com/@BD103/Dark-Mode-Flask
    """

    res = make_response(redirect("/")) 
    res.set_cookie("theme", theme)
    return res

if __name__ == "__main__":
    port = int(os.environ.get('PORT', port))
    app.run(host=host,port=port, debug=True)