from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

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



@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('Employee.html')

@app.route("/Employees")
def employee():
    return render_template('Employee.html')

@app.route("/Add_employee")
def AddEmployee():
    return render_template('Add_employee.html')

@app.route("/Save", methods=['POST'])
def AddEmpData():
    eid = request.form['eid']
    fname = request.form['fname']
    lname = request.form['lname']
    dept = request.form['dept']
    deg = request.form['deg']
    role = request.files['role']
	gender = request.form['gender']
    blood = request.form['blood']
    nid = request.form['nid']
    contact = request.form['contact']
    dob = request.form['dob']
    joindate = request.files['joindate']
	leavedate = request.form['leavedate']
    username = request.form['username']
    email = request.form['email']
    image_url = request.files['image_url']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if image_url.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (eid, fname, lname, dept, deg, role, gender, blood, nid, contact, dob, joindate, leavedate, username, email))
        db_conn.commit()
		#Set name for listout#
        #emp_name = "" + first_name + " " + last_name 
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
    return render_template('Add_employee.html')

@app.route("/Attendance")
def attendance():
    return render_template('Attendance.html')

@app.route("/Save_Attendance")
def addAttendance():
    return render_template('Save_Attendance.html')


@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
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
    return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)