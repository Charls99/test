from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import boto3
from config import *

# Flask constructor#
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__,template_folder="templates", static_folder="static")

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
def index():
    return render_template('Employee.html')

@app.route("/Employees")
def employee():
    search_sql = "SELECT * FROM employee"
    cursor = db_conn.cursor()

    cursor.execute(search_sql)
    allemp = cursor.fetchall()
    return render_template('Employee.html', allemp = allemp)

@app.route("/Add_employee", methods=['GET', 'POST'])
def addEmployee():
    if request.method == 'POST':
       #add userdata when press submit button#
       fname = request.form['fname']
       lname = request.form['lname']
       eid = request.form['eid']
       dept = request.form['dept']
       deg = request.form['deg']
       role = request.form['role']
       gender = request.form['gender']
       blood = request.form['blood']
       nid = request.form['nid']
       contact = request.form['contact']
       dob = request.form['dob']
       joindate = request.form['joindate']
       leavedate = request.form['leavedate']
       username = request.form['username']
       email = request.form['email']
       image_url = request.files['image_url']
    
       insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
       cursor = db_conn.cursor()

       try:

        cursor.execute(insert_sql, (fname, lname, eid, dept, deg, role, gender, blood, nid, contact, dob, joindate, leavedate, username, email))
        db_conn.commit()
        #Set name for listout#
        emp_name = "" + fname + " " + lname
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(eid) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=image_url)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

       finally:
        cursor.close()

       print("all modification done...")
       #after store data return back#
    return render_template('Add_employee.html')

@app.route("/Single_Employee/<eid>")
def singleEmployee(eid):
    #Using %s to Prevent SQL Injection#
    search_sql = "SELECT * FROM employee where eid = %s"
    cursor = db_conn.cursor()

    cursor.execute(search_sql, (eid))
    single_emp = cursor.fetchone()
    return render_template('Single_Employee.html', single_emp = single_emp)

@app.route("/Delete_Employee/<eid>")
def deleteEmployee(eid):
    #Using %s to Prevent SQL Injection#
    delete_sql = "Delete FROM employee where eid = %s"
    cursor = db_conn.cursor()

    cursor.execute(delete_sql, (eid))
    db_conn.commit()
    cursor.close()
    return employee()
    

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
