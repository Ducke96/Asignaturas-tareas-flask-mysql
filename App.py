from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcrud'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"


# routes
@app.route('/')
def Index():



    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM asignaturas')
    data = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tarea')
    dataTarea = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tarea WHERE Fecha_limite BETWEEN NOW() AND NOW() + INTERVAL 4 DAY')
    pendientes = cur.fetchall()
    cur.close()


    return render_template('index.html', contacts = data , tarea = dataTarea , pendientes = pendientes)



@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        Descripcion = request.form['Descripcion']
        horario = request.form['horario']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO asignaturas (fullname, Descripcion, Horario) VALUES (%s,%s,%s)", (fullname, Descripcion, horario))
        mysql.connection.commit()
        flash('Contact Added successfully')

        return redirect(url_for('Index'))



@app.route('/add_tarea', methods=['POST'])
def add_tarea():
    if request.method == 'POST':
        id_asignatura = request.form['id_asignatura']
        fullname = request.form['fullname']
        Fecha_limite = request.form['Fecha_limite']
        Descripcion = request.form['Descripcion']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tarea (id_asignatura,fullname, Fecha_limite, Descripcion) VALUES (%s,%s,%s,%s)", (id_asignatura,fullname, Fecha_limite, Descripcion))
        mysql.connection.commit()
        flash('Contact Added successfully')

        return redirect(url_for('Index'))        

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM asignaturas WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    
    return render_template('edit-contact.html', contact = data[0])



@app.route('/editTarea/<id>', methods = ['POST', 'GET'])
def get_tarea(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tarea WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0][1])
    
    id_asignatura = data[0][1]
    print(id_asignatura)
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM asignaturas')
    dataCombo = cur.fetchall()
    cur.close()


    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM asignaturas WHERE id = {0}'.format(id_asignatura))
    dataComboPre = cur.fetchall()
    cur.close()

    return render_template('edit-tarea.html', contact = data[0] , asignaturas = dataCombo , dataComboPref = dataComboPre[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        Descripcion = request.form['Descripcion']
        horario = request.form['horario']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE asignaturas
            SET fullname = %s,
                Descripcion = %s,
                Horario = %s
            WHERE id = %s
        """, (fullname, Descripcion, horario, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))



@app.route('/updatetarea/<id>', methods=['POST'])
def update_tarea(id):
    if request.method == 'POST':
        id_asignatura = request.form['id_asignatura']
        fullname = request.form['fullname']
        Fecha_limite = request.form['Fecha_limite']
        Descripcion = request.form['Descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE tarea
            SET id_asignatura = %s,
                fullname = %s,
                Fecha_limite = %s,
                Descripcion = %s
            WHERE id = %s
        """, (id_asignatura, fullname, Fecha_limite,Descripcion, id))
        flash('tarea Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM asignaturas WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


@app.route('/deleteTarea/<string:id>', methods = ['POST','GET'])
def delete_tarea(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tarea WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
