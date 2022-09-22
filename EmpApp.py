from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

# Flask constructor#
app = Flask(__name__,static_folder="templates/assets")

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


# Creating a route that has both GET and POST request methods
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('Employee.html')

@app.route("/Employees")
def employee():
    return render_template('Employee.html')

@app.route("/Add_employee")
def addEmployee():
    return render_template('Add_employee.html')
    

@app.route("/Attendance")
def attendance():
    return render_template('Attendance.html')

@app.route("/Save_Attendance")
def addAttendance():
    return render_template('Save_Attendance.html')

# Initiating the application
if __name__ == '__main__':
 # Running the application and leaving the debug mode ON
    app.run(host='0.0.0.0', port=80, debug=True)
