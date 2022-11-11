import ibm_db

dictionary={}
def printTableData(conn):
    sql = "SELECT * FROM userdetails"
    out = ibm_db.exec_immediate(conn, sql)
    document = ibm_db.fetch_assoc(out)
    while document != False:
        dictionary.update({document['USERNAME']:document['PASSWORD']})
        document = ibm_db.fetch_assoc(out)


def insertTableData(conn,rollno,username,email,password):
    sql="INSERT INTO userdetails(rollno,username,email,password) VALUES ({},'{}','{}','{}')".format(rollno,username,email,password)
    out = ibm_db.exec_immediate(conn,sql)
    print('Number of affected rows : ',ibm_db.num_rows(out),"\n")


def updateTableData(conn,rollno,username,email,password):
    sql = "UPDATE userdetails SET (username,email,password)=('{}','{}','{}') WHERE rollno={}".format(username,email,password,rollno)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")

def deleteTableData(conn,rollno):
    sql = "DELETE FROM userdetails WHERE rollno={}".format(rollno)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")

try:
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=lmf89137;PWD=veOooJR9cKcT0lB3;", "", "")
    print("Db connected")

except:
    print("Error")



from flask import Flask,render_template,request,url_for,session
app=Flask(__name__)

@app.route("/")
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        printTableData(conn)
        username=request.form['username']
        password=request.form['password']
        if dictionary[username] == password:
            return "Logged in successfully"
    return render_template('login.html')

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        profession = request.form['profession']
        insertTableData(conn,email, password, age, profession)
        #printTableData(conn)
        return render_template('login.html')
    return render_template('registration.html')

#deleteTableData(conn,6)
#printTableData(conn)
#print(dictionary)


if __name__=="__main__":
    app.run(debug=True)