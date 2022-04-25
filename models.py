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
        #return '<User %r>' % self.username
        return f'clientId: {self.clientId}, clientContactFirstName: {self.clientContactFirstName}'


class Projects(db.Model):
    projectId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    clientId = db.Column(db.Integer, db.ForeignKey(Clients.clientId), nullable=False) # https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    projectDescription = db.Column(db.String(120),nullable=False)
    projectBillRate = db.Column(db.Numeric(6,2), nullable=False) # https://stackoverflow.com/a/42428259
    # Returns information about object when called 
    def __repr__(self):

        return f'projectId: {self.projectId}, projectBillRate: {self.projectBillRate}'

class Employees(db.Model):
    eeId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    eeFirstName = db.Column(db.String(35), nullable=False)
    eeLastName = db.Column(db.String(35), nullable=False)
    eePosition = db.Column(db.String(35), nullable=False)
    eeStatus = db.Column(db.Boolean, nullable=False)
    # Returns information about object when called 
    def __repr__(self):

        return f'eeId: {self.eeId}, eeFirstName: {self.eeFirstName}, eeLastName: {self.eeLastName}'

class Tasks(db.Model):
    taskId = db.Column(db.Integer, primary_key=True, nullable=False, unique=True) #Auto increment? 
    projectId = db.Column(db.Integer, db.ForeignKey(Projects.projectId), nullable=False) # https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes
    taskDescription = db.Column(db.String(240), nullable=False)
    taskTime = db.Column(db.Numeric(4,2), nullable=False)
    eeId = db.Column(db.Integer, db.ForeignKey(Employees.eeId), nullable=False)
    # Returns information about object when called 
    def __repr__(self):

        return f'taskId: {self.taskId}, taskDescription: {self.taskDescription}'

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
                    (3, 'Cut the grass every two weeks',39.99),
                    (4, 'Tune double bass',139.99),
                    (5, 'Disposal of large bagged object', 100.99)
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
        ee = Employees(     eeFirstName = i[0],
                            eeLastName = i[1],
                            eePosition = i[2],
                            eeStatus = i[3]
                    )


        db.session.add(ee)
    
    db.session.commit()
    # for i in (Employees.query.all()):
    #     print(i)

    # -------------------------- Populate Tasks table
    TasksLst = [    (1, 'Pulled weeds all damn day', 3.4, 1),
                    (2, 'Trimmed 57 trees.', 2.5, 2)
                    ]

   
    # print("Populating test database.")

    for i in TasksLst: 
        task = Tasks(   projectId= i[0], 
                        taskDescription= i[1], 
                        taskTime= i[2], 
                        eeId = i[3] 
                    )


        db.session.add(task)
    
    db.session.commit()
    # for i in (Tasks.query.all()):
    #     print(i)



if __name__ == "__main__": 

    # Create new schema 
    db.create_all()

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
                    (3, 'Cut the grass every two weeks',39.99),
                    (4, 'Tune double bass',139.99),
                    (5, 'Disposal of large bagged object', 100.99)
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
        ee = Employees(     eeFirstName = i[0],
                            eeLastName = i[1],
                            eePosition = i[2],
                            eeStatus = i[3]
                    )


        db.session.add(ee)
    
    db.session.commit()
    # for i in (Employees.query.all()):
    #     print(i)

    # -------------------------- Populate Tasks table
    TasksLst = [    (1, 'Pulled weeds all damn day', 3.4, 1),
                    (2, 'Trimmed 57 trees.', 2.5, 2)
                    ]

   
    # print("Populating test database.")

    for i in TasksLst: 
        task = Tasks(   projectId= i[0], 
                        taskDescription= i[1], 
                        taskTime= i[2], 
                        eeId = i[3] 
                    )


        db.session.add(task)
    
    db.session.commit()
    # for i in (Tasks.query.all()):
    #     print(i)

    print("**Database populated.\n")