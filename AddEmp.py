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

@app.route("/AddEmp.py", methods=['POST'])
def addEmployeeData():
#add userdata when press submit button#
    if request.method == 'POST':
       eid = request.form['eid']
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

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
    