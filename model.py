from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import os 


app = Flask(__name__)

# --------------------Database Connection--------------------

def mySqlConnection():
    """
    Create mySQL connection with credentials in dotenv in root directory file.
    """
    load_dotenv(find_dotenv())
    host = os.environ.get("DBHOST")
    user = os.environ.get("DBUSER")
    passwd = os.environ.get("DBPW")
    db = os.environ.get("DB")
    # MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{passwd}@{host}/{db}'

def sqlLiteConnection():
    """
    Create SQLite connection with db in root directory. 
    """
    # SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/timeTrack.db'

# Initiate connection, initial config
sqlLiteConnection()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --------------------Database Model--------------------#

class Clients(db.Model):
    clientId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    clientOrganizationName = db.Column(db.String(35),nullable=True)
    clientContactFirstName = db.Column(db.String(35),nullable=False)
    clientContactLastName = db.Column(db.String(35),nullable=False)
    clientContactEmail = db.Column(db.String(70),nullable=False)
    projects = db.relationship('Projects',cascade="all, delete") # Non-data / relationship

    def __repr__(self):
        """
        Return information about object.
        """
        return f'clientId: {self.clientId}, clientContactFirstName: {self.clientContactFirstName}'

    def getData(self):
        """
        Return dict of all columns and values.
        """
        return dict({   'clientId':self.clientId,
                        'clientOrganizationName':self.clientOrganizationName,
                        'clientContactFirstName':self.clientContactFirstName,
                        'clientContactLastName':self.clientContactLastName,
                        'clientContactEmail':self.clientContactEmail
                    })

class Projects(db.Model):
    projectId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) 
    clientId = db.Column(db.Integer, db.ForeignKey(Clients.clientId), nullable=False) # Note [1]
    projectDescription = db.Column(db.String(120),nullable=False)
    projectBillRate = db.Column(db.Numeric(6,2), nullable=False) # Note [2]
    tasks = db.relationship('Tasks',cascade="all, delete") # Non-data / relationship - Note [3]
    
    def __repr__(self):
        """
        Return information about object.
        """
        return f'projectId: {self.projectId}, projectBillRate: {self.projectBillRate}'
    
    def getData(self):
        """
        Return dict of all columns and values.
        """
        return dict({   'projectId':self.projectId,
                        'clientId':self.clientId,
                        'projectDescription':self.projectDescription,
                        'projectBillRate':float(self.projectBillRate)
                    })

class Employees(db.Model):
    employeeId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)  
    employeeFirstName = db.Column(db.String(35), nullable=False)
    employeeLastName = db.Column(db.String(35), nullable=False)
    employeePosition = db.Column(db.String(35), nullable=False)
    employeeStatus = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        """
        Return information about object.
        """
        return f'employeeId: {self.employeeId}, employeeFirstName: {self.employeeFirstName}, employeeLastName: {self.employeeLastName}'
    
    def getData(self):
        """
        Return dict of all columns and values.
        """
        return dict({   'employeeId':self.employeeId,
                        'employeeFirstName':self.employeeFirstName,
                        'employeeLastName':self.employeeLastName,
                        'employeePosition':self.employeePosition,
                        'employeeStatus':self.employeeStatus
                })

class Tasks(db.Model):
    taskId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) 
    projectId = db.Column(db.Integer, db.ForeignKey(Projects.projectId), nullable=False) # Note [1]
    taskDescription = db.Column(db.String(240), nullable=False)
    taskDate = db.Column(db.String(10), nullable=False)# new
    taskTime = db.Column(db.Numeric(4,2), nullable=False)
    employeeId = db.Column(db.Integer, db.ForeignKey(Employees.employeeId), nullable=False)

    def __repr__(self):
        """
        Return information about object.
        """
        return f'taskId: {self.taskId}, taskDescription: {self.taskDescription}'

    def getData(self):
        """
        Return dict of all columns and values.
        """
        return dict({   'taskId':self.taskId,
                        'projectId':self.projectId,
                        'taskDescription':self.taskDescription,
                        'taskDate':self.taskDate,
                        'taskTime':float(self.taskTime),
                        'employeeId':self.employeeId
                    })

#--------------------Additional Functionality--------------------

def getSesssion():
    """
    Return the current database session.
    """
    return db.session

def prepopulateDatabase():
    """
    Prepopulate a sample database for the application.
    """

    # ----- Create new schema -----
    db.drop_all() # drop old tables and data
    db.create_all() # create new tables 

    # ----- Populate Clients table -----
    clientsLst = [  ('ACME', 'Rafiki', 'Adams ', 'ra@example.com'),
                    ('Bat Enterprises', 'Mufasa', 'Ghosh ', 'mg@example.com'),
                    (None, 'Raj', 'Klepper ', 'rk@example.com'),
                    (None, 'Charles', 'Mingus ', 'cm@example.com'),
                    ('Evil Corp', 'Tyrell', 'Wellick', 'tw@evilcorp.com')
                ]
    for i in clientsLst: 
        client = Clients(clientOrganizationName=i[0], 
                        clientContactFirstName=i[1], 
                        clientContactLastName=i[2], 
                        clientContactEmail=i[3]
                    )
        db.session.add(client)
    db.session.commit()

    # ----- Populate Projects table -----
    projectsLst = [ (1, 'Monthly garden maintenence at Adams house.', 55.99),
                    (2, 'Periodic tree trimming at Ghosh house.', 69.99), 
                ]

    for i in projectsLst: 
        project = Projects(clientId=i[0], 
                        projectDescription=i[1], 
                        projectBillRate=i[2]
                    )
        db.session.add(project)
    
    db.session.commit()

    # ----- Populate Employees table -----
    employeesLst = [    ('Brandi','Bingo','Manager',1),
                        ('Shenzi','Filson','Associate',1)
                    ]

    for i in employeesLst: 
        ee = Employees(     employeeFirstName = i[0],
                            employeeLastName = i[1],
                            employeePosition = i[2],
                            employeeStatus = i[3]
                    )
        db.session.add(ee)   
    db.session.commit()

    # ----- Populate Tasks table -----
    # projectId, taskDescription, taskDate, taskTime, employeeId
    tasksLst = [    (1, 'Pulled weeds all damn day', '2020-01-02',3.4, 1),
                    (1, 'Finished pulling weeds', '2020-01-03',2.4, 1),
                    (1, 'Pruned begonias', '2020-01-08',2.1, 1),
                    (1, 'Mulched front flower beds', '2020-01-04',2.1, 1),
                    (1, 'Transplanted very thorny rose bush', '2020-01-05',4.4, 1),
                    (1, 'Pulled more weeds all damn day', '2020-01-20',15.2, 1),
                    (2, 'Trimmed 57 trees.', '2020-01-05',2.5, 2)
                ]

    for i in tasksLst: 
        task = Tasks(   projectId= i[0], 
                        taskDescription= i[1], 
                        taskDate=i[2],
                        taskTime= i[3], 
                        employeeId = i[4] 
                    )
        db.session.add(task)
    db.session.commit()



#--------------------Notes--------------------

#[1] https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
#[2] https://stackoverflow.com/a/42428259
#[3] https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete