from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import os 

# Based off of this intro 
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

app = Flask(__name__)

# # --------------------Database Connection-------------------------------------#
# # Load our environment variables from the .env file in the root of our project.
# load_dotenv(find_dotenv())

# # Set the variables in our application with those environment variables
# host = os.environ.get("DBHOST")
# user = os.environ.get("DBUSER")
# passwd = os.environ.get("DBPW")
# db = os.environ.get("DB")

# # SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# # MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{passwd}@{host}/{db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------Database Model------------------------------------------#

class Clients(db.Model):
    clientId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    clientOrganizationName = db.Column(db.String(35),nullable=True)
    clientContactFirstName = db.Column(db.String(35),nullable=False)
    clientContactLastName = db.Column(db.String(35),nullable=False)
    clientContactEmail = db.Column(db.String(70),nullable=False)

    # Returns information about object when called 
    def __repr__(self):
        """Return information about object when called"""
        #return '<User %r>' % self.username
        return f'clientId: {self.clientId}, clientContactFirstName: {self.clientContactFirstName}'
    # Return dict of all columns and values

    def getData(self):
        """Return dict of all columns and values"""
        return dict({   'clientId':self.clientId,
                        'clientOrganizationName':self.clientOrganizationName,
                        'clientContactFirstName':self.clientContactFirstName,
                        'clientContactLastName':self.clientContactLastName,
                        'clientContactEmail':self.clientContactEmail
                })
    



class Projects(db.Model):
    projectId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    clientId = db.Column(db.Integer, db.ForeignKey(Clients.clientId), nullable=False) # https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    projectDescription = db.Column(db.String(120),nullable=False)
    projectBillRate = db.Column(db.Numeric(6,2), nullable=False) # https://stackoverflow.com/a/42428259
   
    # Returns information about object when called 
    def __repr__(self):
        """Return information about object when called"""
        return f'projectId: {self.projectId}, projectBillRate: {self.projectBillRate}'
    
    # Return dict of all columns and values
    def getData(self):
        """Return dict of all columns and values"""
        return dict({'projectId':self.projectId,
                'clientId':self.clientId,
                'projectDescription':self.projectDescription,
                'projectBillRate':float(self.projectBillRate)
                })




class Employees(db.Model):
    employeeId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    employeeFirstName = db.Column(db.String(35), nullable=False)
    employeeLastName = db.Column(db.String(35), nullable=False)
    employeePosition = db.Column(db.String(35), nullable=False)
    employeeStatus = db.Column(db.Boolean, nullable=False)

    
    def __repr__(self):
        """Return information about object when called"""
        return f'employeeId: {self.employeeId}, employeeFirstName: {self.employeeFirstName}, employeeLastName: {self.employeeLastName}'

    
    def getData(self):
        """Return dict of all columns and values"""
        return dict({   'employeeId':self.employeeId,
                        'employeeFirstName':self.employeeFirstName,
                        'employeeLastName':self.employeeLastName,
                        'employeePosition':self.employeePosition,
                        'employeeStatus':self.employeeStatus
                })




class Tasks(db.Model):
    taskId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    projectId = db.Column(db.Integer, db.ForeignKey(Projects.projectId), nullable=False) # https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    taskDescription = db.Column(db.String(240), nullable=False)
    taskDate = db.Column(db.String(10), nullable=False)# new
    taskTime = db.Column(db.Numeric(4,2), nullable=False)
    employeeId = db.Column(db.Integer, db.ForeignKey(Employees.employeeId), nullable=False)
    # Returns information about object when called 
    def __repr__(self):
        """Return information about object when called"""
        return f'taskId: {self.taskId}, taskDescription: {self.taskDescription}'

    # Return dict of all columns and values
    def getData(self):
        """Return dict of all columns and values"""
        return dict({'taskId':self.taskId,
                'projectId':self.projectId,
                'taskDescription':self.taskDescription,
                'taskDate':self.taskDate,
                'taskTime':float(self.taskTime),
                'employeeId':self.employeeId
                })

def prepopulateDatabase():
    # Create new schema 
    db.drop_all() # drop old tables and data
    db.create_all() # create new tables 

    # print("**Populating test database.**\n")
    # Populate Clients table 
    # print("Creating test Clients table.\n")
    ClientsLst = [  ('ACME', 'Rafiki', 'Adams ', 'ra@example.com'),
                    ('Bat Enterprises', 'Mufasa', 'Ghosh ', 'mg@example.com'),
                    (None, 'Raj', 'Klepper ', 'rk@example.com'),
                    (None, 'Charles', 'Mingus ', 'cm@example.com'),
                    ('Evil Corp', 'Tyrell', 'Wellick', 'tw@evilcorp.com')
                ]

    for i in ClientsLst: 
        client = Clients(clientOrganizationName=i[0], 
                        clientContactFirstName=i[1], 
                        clientContactLastName=i[2], 
                        clientContactEmail=i[3]
                    )
        db.session.add(client)
    
    db.session.commit()

    # for i in (Clients.query.all()):
    #     print(i)

    # print()

    # -------------------------- Populate Projects table 
    # print("Creating test Projects table.\n")
    ProjectsLst = [ (1, 'Monthly garden maintenence at Adams house.', 55.99),
                    (2, 'Periodic tree trimming at Ghosh house.', 69.99), 
                ]

   
    # print("Populating test database.")

    for i in ProjectsLst: 
        project = Projects(clientId=i[0], 
                        projectDescription=i[1], 
                        projectBillRate=i[2]
                    )
        db.session.add(project)
    
    db.session.commit()
    # for i in (Projects.query.all()):
    #     print(i)


    # -------------------------- Populate Employees table
    EmployeesLst = [    ('Brandi','Bingo','Manager',1),
                        ('Shenzi','Filson','Associate',1)
                    ]

   
    # print("Populating test database.")

    for i in EmployeesLst: 
        ee = Employees(     employeeFirstName = i[0],
                            employeeLastName = i[1],
                            employeePosition = i[2],
                            employeeStatus = i[3]
                    )


        db.session.add(ee)
    
    db.session.commit()
    # for i in (Employees.query.all()):
    #     print(i)

    # -------------------------- Populate Tasks table
    # projectId, taskDescription, taskDate, taskTime, employeeId
    TasksLst = [    (1, 'Pulled weeds all damn day', '2020-01-02',3.4, 1),
                    (1, 'Finished pulling weeds', '2020-01-03',2.4, 1),
                    (1, 'Pruned begonias', '2020-01-08',2.1, 1),
                    (1, 'Mulched front flower beds', '2020-01-04',2.1, 1),
                    (1, 'Transplanted very thorny rose bush', '2020-01-05',4.4, 1),
                    (1, 'Pulled more weeds all damn day', '2020-01-20',15.2, 1),
                    (2, 'Trimmed 57 trees.', '2020-01-05',2.5, 2)
                    ]

   
    # print("Populating test database.")

    for i in TasksLst: 
        task = Tasks(   projectId= i[0], 
                        taskDescription= i[1], 
                        taskDate=i[2],
                        taskTime= i[3], 
                        employeeId = i[4] 
                    )


        db.session.add(task)
    
    db.session.commit()
    # for i in (Tasks.query.all()):
    #     print(i)


def getSesssion():
    """Return the current database session"""
    return db.session



