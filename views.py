from app import *
from models import Database

# instancia la base de datos
db = Database()
# redirecciona hacia el login
@app.route('/')
def index():
    return redirect(url_for('login'))
# controlador de login http://localhost:5000/pythonlogin/
@app.route('/login', methods=['GET', 'POST'])
def login():
    # controlador de los mensajes de error
    msg = ''
    # valida que haya un POST, usuario y clave
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # crea variables de uso rapido
        email = request.form['email']
        password = str(b64encode(request.form['password'].encode('utf-8')), 'utf-8')
        credenciales = (email, password)
        print(password)
        # valida la cuenta contra la base de datos
        account = db.validar_usuario(credenciales)
        # cursor.execute('SELECT * FROM usuarios\
        #                 WHERE email = %s AND clave = %s',
        #                 (email, password))
        # captura el query en la variable account
        #account = cursor.fetchone()
        # valida si la cuenta existe
        if account:
            # crea la data de registro para ser usado por otros modulos
            session['loggedin'] = True
            session['id'] = account[0]
            session['dni'] = account[1]
            session['nombre'] = account[2]
            session['apellido'] = account[3]
            session['email'] = account[5]
            session['telefono'] = account[6]
            session['direccion'] = account[7]
            session['ciudad'] = account[8]
            # redirecciona a la pagina de inicio
            return redirect(url_for('home'))
        else:
            # la cuenta o la clave estan erroneas
            msg = 'Usuario o clave incorrecto.'
    # muestra el formulario de inicio si hay algun mensaje
    return render_template('index.html', msg=msg)

# controla la pagina de logout http://localhost:5000/pythonlogin/logout
@app.route('/logout')
def logout():
    # elimina los datos que se registraron de la session
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre', None)
    session.pop('apellido', None)
    session.pop('dni', None)
    session.pop('telf', None)
    session.pop('email', None)
    session.pop('direccion', None)
    session.pop('ciudad', None)
    # redirecciona a la pagina de login
    return redirect(url_for('login'))

# controla la pagina de registro http://localhost:5000/pythonlogin/register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # muestra cualquier error en el mensaje de la pantalla
    msg = ''
    ciudades = db.consultar_ciudades()
    # chequea si los campos username, password e email existen cuando se hace el POST
    if request.method == 'POST' and\
    'nombre' in request.form and\
    'apellido' in request.form and\
    'dni' in request.form and\
    'password' in request.form and\
    'email' in request.form:
        # crea una tupla con los datos del usuario
        datos_usuario = (
            request.form['dni'],
            request.form['nombre'],
            request.form['apellido'],
            request.form['email'],
            request.form['telf'],
            b64encode(request.form['password'].encode('utf-8')),
            request.form['direccion'],
            request.form['ciudad']
        )
        
        # chequea la cuenta contra la base de datos
        account = db.consultar_usuario_por_email(datos_usuario[3])
        # valida la cuenta y sus campos
        if account:
            msg = 'La cuenta ya existe.'
            flash(msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', datos_usuario[3]):
            msg = 'Dirección de email inválida.'
            flash(msg)
        elif not re.match(r'^[0-9]{7,8}', datos_usuario[0]):
            msg = 'Utiliza solo numeros, sin puntos ni espacios para el DNI'
            flash(msg)
        elif not datos_usuario[0] or not\
        datos_usuario[1] or not datos_usuario[2] or not\
        datos_usuario[3] or not datos_usuario[4]:
            msg = 'Llena todos los campos antes de continuar.'
            flash(msg)
        else:
            # se procede a guardar la informacion en la base de datos si no hay problemas
            db.crear_usuario(datos_usuario)
            flash('Te registraste con éxito.')
            msg = ''
    elif request.method == 'POST':
        # chequea si el formulario esta vacio
        msg = 'Falta información, recuerda completar todos los campos.'
        flash(msg)
    # muestra los mensaje en el formulario de registro, en el caso que haya alguno
    return render_template('register.html', msg=msg, ciudades=ciudades)

# maneja el home http://localhost:5000/pythonlogin/home
@app.route('/home')
def home():
    # verifica si el usuario esta logueado
    if 'loggedin' in session:
        historico_compras = db.consultar_compras(session['email'])
        # redirecciona al home, si se registra correctamente
        return render_template('home.html', username=session['nombre'], compras=historico_compras)
    # redirecciona a la pagina de login, si no esta registrado
    return redirect(url_for('login'))

# define la ruta y funciones del perfil http://localhost:5000/pythonlogin/profile
@app.route('/profile')
def profile():
    # verifica si el usuario esta registrado
    if 'loggedin' in session:
        # muestra toda la info del usuario desde la base de datos
        cuenta = db.consultar_usuario_por_email(session['email'])
        # muestra los datos en la pagina de profile
        return render_template('profile.html', account=cuenta)
    # redirecciona a la pantalla de login si no esta registrado
    return redirect(url_for('login'))

# define la ruta y funciones para el catalogo http://localhost:5000/pythonlogin/catalogo
@app.route('/catalogo', method=['GET', 'POST'])
def catalogo():
    # chequea si hay un usuario registrado
    if 'loggedin' in session:
        if request.method == 'POST':
            compras = request.args.getlist('compra')
            print(compras)
        else:
            catalogo = db.consultar_lista_productos()
            return render_template('catalogo.html', productos=catalogo)
    # redirecciona a la pagina de login, si no esta registrado
    return redirect(url_for('login'))

# define la ruta y funciones del carrito de compras http://localhost:5000/pythonlogin/carrito
@app.route('/carrito')
def carrito():
    if 'loggedin' in session:
        if request.method == 'POST':
            pass
