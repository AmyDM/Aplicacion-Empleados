from flask import Flask, render_template, request, redirect, url_for, flash, Markup
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = False
app.config['MYSQL_DB'] = 'informacion_general'
mysql = MySQL(app)

app.secret_key = "llave"

@app.route('/')
def Index():
    q = mysql.connection.cursor()
    q.execute('SELECT * FROM empleados')
    datos = q.fetchall()

    q.close()
    return render_template('index.html', empleados = datos)

@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        ventas = request.form['ventas']
        q = mysql.connection.cursor()
        q.execute("INSERT INTO empleados (nombre, apellido, ventas) VALUES (%s,%s,%s)", (nombre, apellido, ventas))
        mysql.connection.commit()
        flash('Se ha añadido exitosamente')
        return redirect(url_for('Index'))


@app.route('/grafica')
def grafica():
    q = mysql.connection.cursor()
    q.execute('SELECT nombre FROM empleados')
    datos1 = q.fetchall()
    bar_labels = [row[0] for row in datos1]


    q = mysql.connection.cursor()
    q.execute('SELECT ventas FROM empleados')
    datos2 = q.fetchall()
    bar_values = [row[0] for row in datos2]


    return render_template('grafica.html', title='Ventas por empleado', max=17000, labels=bar_labels, values=bar_values)


if __name__ == "__main__":
    app.run(port=3000, debug=True)