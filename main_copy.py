from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from base64 import b64encode, b64decode
import MySQLdb.cursors
import os
import re

app = Flask(__name__)

# Llave secreta
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ecommerce'

mysql = MySQL(app)

# controlador de login http://localhost:5000/pythonlogin/
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # controlador de los mensajes de error
    msg = ''
    # valida que haya un POST, usuario y clave
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # crea variables de uso rapido
        email = request.form['email']
        password = str(b64encode(request.form['password'].encode('utf-8')), 'utf-8')
        print(password)
        # valida la cuenta contra la base de datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios\
                        WHERE email = %s AND clave = %s',
                        (email, password))
        # captura el query en la variable account
        account = cursor.fetchone()
        print(account)
        # valida si la cuenta existe
        if account:
            # crea la data de registro para ser usado por otros modulos
            session['loggedin'] = True
            session['id'] =account['usuario_id']
            session['nombre'] = account['nombre']
            session['apellido'] = account['apellido']
            session['dni'] = account['dni']
            session['telefono'] = account['telefono']
            session['email'] = account['email']
            # redirecciona a la pagina de inicio
            return redirect(url_for('home'))
        else:
            # la cuenta o la clave estan erroneas
            msg = 'Usuario o clave incorrecto.'
    # muestra el formulario de inicio si hay algun mensaje
    return render_template('index.html', msg=msg)

# controla la pagina de logout http://localhost:5000/pythonlogin/logout
@app.route('/pyhonlogin/logout')
def logout():
    # elimina los datos que se registraron de la session
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre', None)
    session.pop('apellido', None)
    session.pop('dni', None)
    session.pop('telf', None)
    session.pop('email', None)
    # redirecciona a la pagina de login
    return redirect(url_for('login'))

# controla la pagina de registro http://localhost:5000/pythonlogin/register
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # muestra cualquier error en el mensaje de la pantalla
    msg = ''
    # chequea si los campos username, password e email existen cuando se hace el POST
    if request.method == 'POST' and\
    'nombre' in request.form and\
    'apellido' in request.form and\
    'telf' in request.form and\
    'password' in request.form and\
    'email' in request.form:
        # crea las variables de cada uno
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        password = b64encode(request.form['password'].encode('utf-8'))
        email = request.form['email']
        telf = request.form['telf']
        # chequea la cuenta contra la base de datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE dni = %s', (dni,))
        account = cursor.fetchone()
        # valida la cuenta y sus campos
        if account:
            msg = 'La cuenta ya existe.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Dirección de email inválida.'
        elif not re.match(r'^[0-9]{7,9}', dni):
            msg = 'Utiliza solo numeros, sin puntos ni espacios para el DNI'
        elif not nombre or not apellido or not password or not email or not telf:
            msg = 'Llena todos los campos antes de aceptar'
        else:
            # se procede a guardar la informacion en la base de datos si no hay problemas
            cursor.execute('INSERT INTO usuarios (dni, nombre, apellido, clave, email, telefono)\
                            VALUES (%s, %s, %s, %s, %s, %s)', (dni, nombre, apellido, password, email, telf))
            mysql.connection.commit()
            msg = 'Te registraste con éxito.'
    elif request.method == 'POST':
        # chequea si el formulario esta vacio
        msg = 'Falta información, recuerda completar todos los campos.'
    # muestra los mensaje en el formulario de registro, en el caso que haya alguno
    return render_template('register.html', msg=msg)

# maneja el home http://localhost:5000/pythonlogin/home
@app.route('/pythonlogin/home')
def home():
    # verifica si el usuario esta logueado
    if 'loggedin' in session:
        # redirecciona al home, si se registra correctamente
        return render_template('home.html', username=session['nombre'])
    # redirecciona a la pagina de login, si no esta registrado
    return redirect(url_for('login'))

# este codigo maneja la seccion de profile http://localhost:5000/pythonlogin/profile
@app.route('/pythonlogin/profile')
def profile():
    # verifica si el usuario esta registrado
    if 'loggedin' in session:
        # muestra toda la info del usuario desde la base de datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT\
                            direcciones.direccion,\
                            direcciones.altura,\
                            direcciones.codigo_postal,\
                            ciudades.nombre,\
                            provincias.nombre,\
                            paises.nombre\
                        FROM usuarios\
                        INNER JOIN direcciones ON direcciones.id = usuarios.direccion_id\
                        INNER JOIN ciudades ON ciudades.ciudad_id = direcciones.ciudad_id\
                        INNER JOIN provincias ON provincias.provincia_id = ciudades.provincia_id\
                        INNER JOIN paises ON paises.pais_id = provincias.pais_id\
                        WHERE usuarios.usuario_id = %s', [session['id']])
        account = cursor.fetchone()
        # muestra los datos en la pagina de profile
        return render_template('profile.html', account=account)
    # redirecciona a la pantalla de login si no esta registrado
    return redirect(url_for('login'))