from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'gradesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Grades Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, grades=result)


@app.route('/view/<int:grades_id>', methods=['GET'])
def record_view(grades_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE id=%s', grades_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', grades=result[0])

@app.route('/edit/<int:grades_id>', methods=['GET'])
def form_edit_get(grades_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM grades WHERE id=%s', grades_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', grades=result[0])

@app.route('/edit/<int:grades_id>', methods=['POST'])
def form_update_post(grades_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Lname'), request.form.get('Fname'), request.form.get('ssn'),
                 request.form.get('Test1'), request.form.get('Test2'),
                 request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'),
                 request.form.get('Grade'), grades_id)
    sql_update_query = """UPDATE grades t SET t.Last_name = %s, t.First_name = %s, t.SSN = %s, t.Test1 = 
        %s, t.Test2 = %s, t.Test3 = %s, t.Test4 = %s,t.Final= %s,t.Grade = %s  WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/grades/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Grades Form')

@app.route('/grades/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (
    request.form.get('Lname'), request.form.get('Fname'), request.form.get('ssn'), request.form.get('Test1'),
    request.form.get('Test2'), request.form.get('Test3'), request.form.get('Test4'), request.form.get('Final'),
    request.form.get('Grade'))
    sql_insert_query = """INSERT INTO grades (Last_name,First_name,SSN,Test1,Test2,Test3,Test4,Final,Grade) VALUES (%s, %s,%s, %s,%s, %s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:grades_id>', methods=['POST'])
def form_delete_post(grades_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM grades WHERE id = %s """
    cursor.execute(sql_delete_query, grades_id)
    mysql.get_db().commit()
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
