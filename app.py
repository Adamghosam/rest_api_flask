# library import
from flask import Flask, jsonify, request,session
from flask_mysqldb import MySQL,MySQLdb
from werkzeug.security import generate_password_hash,check_password_hash
from flask_cors import CORS
from datetime import timedelta
import mysql.connector

# koneksi 
app = Flask(__name__)

app.config['SECRET_KEY']= 'adamghosam-gmail.com'
app.config['PERMANENT_SESSION_LIFETIME']= timedelta(minutes=1)
CORS(app)



# bats koneksi db

app.config['MYSQL_HOST']='192.168.200.222'
app.config['MYSQL_USER']='gho'
app.config['MYSQL_PASSWORD']='ghosam'
app.config['MYSQL_DB']='glory'
app.config['MYSQL_CURSORCLASS']='DictCursor'


# bats koneksi db


mysql =MySQL(app)



@app.route('/')
def home():
    # paswd =generate_password_hash('admin123')
    # print(paswd)
    # return "message for ghosam"
    if 'pid' in session:
        pid =  session['pid']
        return jsonify({'message':' you already loggen in ','pid' : pid})
    else:
        resp =jsonify({'message':'Unautorizei'})
        resp.status_code =401
        return resp


# prosedur 

@app.route('/absen',methods=['POST'])
def absen():
# prosedure
   
    _json =request.json   
    _pid = _json['pid']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result_exse=cursor.callproc('masuk',[_pid])
    mysql.connection.commit()
    return jsonify({'message':'you are Absen in sucessfuly!'})
    

    
# batas prosedure

@app.route('/login', methods=['POST'])
def login():
    _json = request.json
    _pid = _json['pid']
    _pswd = _json['pswd']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM personal WHERE pid=%s"
    sql_where =(_pid,)
    cursor.execute(sql,sql_where)
    row =cursor.fetchone()
    # file
    pid = row['pid']
    nama =row['nama']
  
    data={
        'pid':pid,
        'nama':nama,
    }
    # check password
    if _pswd == pid :
        session['pid']= pid
        cursor.close()
        return jsonify({'message':'you are loggin in sucessfuly!', 'data' : data})

    else:
        resp =jsonify({'message':'Bad Request-invalid Password'})
        resp.status_code =400
        return resp




@app.route('/logout' ,methods=['GET'])
def logout():
    if 'username' in session:   
        session.pop('username', None)
    return jsonify({'message':'kamu berhasil keluar'})








if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='172.16.32.10', port=5000)
