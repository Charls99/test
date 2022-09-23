from flask import Flask, render_template, request, url_for
from pymysql import connections
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
def index():
    return render_template('Employee.html')

@app.route("/Employees")
def employee():
    return render_template('Employee.html')

@app.route("/Add_employee", methods=['GET', 'POST'])
def addEmployee():
    if request.method == 'POST':
       fname = request.form['fname']
       lname = request.form['lname']

       insert_sql = "INSERT INTO test VALUES (%s, %s)"
       cursor = db_conn.cursor()

    try:

        cursor.execute(insert_sql, (fname, lname))
        db_conn.commit()

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('Add_employee.html')


@app.route("/AddEmpData", methods=['POST'])
def addEmployeeData():
#add userdata when press submit button#
    fname = request.form['fname']
    lname = request.form['lname']
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

    return fname
    

@app.route("/Attendance")
def attendance():
    return render_template('Attendance.html', name=db_conn)

@app.route("/Save_Attendance")
def addAttendance():
    return render_template('Save_Attendance.html')

# Initiating the application
if __name__ == '__main__':
 # Running the application and leaving the debug mode ON
    app.run(host='0.0.0.0', port=80, debug=True)
