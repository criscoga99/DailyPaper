from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from datetime import date
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' #Direccion del servidor de BD
app.config['MYSQL_USER'] = 'root' #Usuario del servidor
app.config['MYSQL_PASSWORD'] = '1234' #Contraseña del servidor
app.config['MYSQL_DB'] = 'DailyPaper' #Nombre de la BD
mysql = MySQL(app)
#Ruta raíz
@app.route('/')
def home():
    return render_template('login.html')
#Ruta de registro
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST': #Si el método por el cual se accede a la ruta es POST, quiere decir que el formulario ha sido enviado
        #Extrar los datos del formulario mediante el método form y lo almacena en variables
        user = request.form['user'] 
        passwd = request.form['pass']
        confirm_passwd = request.form['confirmpass']
        type_user = request.form['typeuser']
        cursor = mysql.connection.cursor()
        usuario = cursor.execute(f'select * from usuarios where nombre = "{user}"')
        mysql.connection.commit()
        if passwd != confirm_passwd: #Comprueba si los campos de contraseñas son coincidentes o no
            mensaje = "Usuario no registrado! La contraseña no coincide"
            return render_template ('login.html', mensaje=mensaje)
        elif usuario == True: #Comprueba si el usuario existe o no conforma a lo que haya arrojado la consulta anterior (si arroja True, el usuario existe). En caso de que el usuario exista, arrojará un error
            mensaje = "El usuario ya existe!"
            return render_template ('login.html', mensaje=mensaje)
        elif user == "" or passwd == "": #Comprueba si los datos necesarios tales como el usuario y la contraseña están en blanco o no
            mensaje = "Error debe introducir todos los datos"
            return render_template ('login.html', mensaje=mensaje)
        elif passwd == confirm_passwd: #En caso de que ningunas de las anteriores acciones no se haya llevado a cabo, y los campos de contraseña sean coincidentes, se llevará a cabo la insercción del usuario en la BD mediante un cursor
            cursor1 = mysql.connection.cursor()
            add_user = cursor1.execute('insert into usuarios(nombre, pass, tipo_usuario) values (%s, %s, %s)', (user, passwd, type_user))
            data1 = cursor1.fetchall()
            mysql.connection.commit()
            return render_template ('login.html')
    else: #Si el formulario no ha sido enviado, el método seguirá siendo GET
        return render_template ('login.html')
#Ruta login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST': #En caso de que el formulario se haya enviado
        global user
        user = request.form['user']
        passwd = request.form['pass']
        cursor = mysql.connection.cursor()
        cursor1 = mysql.connection.cursor()
        usuario = cursor.execute('select nombre from usuarios where nombre = %s and pass = %s', (user, passwd))
        editorial = cursor1.execute('select tipo_usuario from usuarios where nombre = %s and pass = %s', (user, passwd))
        data = cursor1.fetchall()
        mysql.connection.commit()
        #Comprobaciones de la existencias de los usuarios mediante un cursor y del tipo de usuario mediante otro cursor
        #Si el usuario es usuario raso o editorial devolverá un index diferente al index de un admin
        if usuario == True and data[0][0] == "Editorial": 
            return redirect(url_for("inicio"))
        elif usuario == True and data[0][0] == "Usuario":
            return redirect(url_for("inicio"))
        elif usuario == True and data[0][0] == "Admin":
            return redirect(url_for("inicio_admin"))
        elif user == "" or passwd == "": #Si los campos están vacios, devolverá error
            mensaje = "Error debe introducir todos los datos"
            return render_template('login.html', mensaje=mensaje)
        else: #Si el usuario no existe o su contraseña esta mal introducida, devolverá error
            mensaje = "Error de autenticación"
            return render_template('login.html', mensaje=mensaje)
    else: 
        return render_template ('login.html')
#Ruta del inicio de los usuarios rasos y las editoriales
@app.route('/inicio')
def inicio():
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    #Se extrae las noticias posteadas por el usuario, para que luego sean mostradas en la plantilla con un for
    noticias = cursor.execute(f'select p.id, p.titular from usuarios u inner join publicaciones p on u.id = p.creador where u.nombre = "{user}"')
    #Se extrae el id del usuario actual, útil para realizar acciones posteriores
    id_usuario = cursor2.execute(f'select id from usuarios where nombre = "{user}"')
    data = cursor.fetchall()
    global id_user
    id_user = cursor2.fetchall()
    return render_template('hecho.html', noticias=data, id_user=id_user, usuario=user)
#Ruta de redacción de posts (usuarios y editoriales)
@app.route('/inicio/redactar', methods=['POST', 'GET'])
def redactar():
    if request.method == 'POST': #En caso de que el formulario haya sido enviado
        titular = request.form['titular']
        cuerpo = request.form['cuerpo']
        tematica = request.form['topic']
        fecha_comentario = date.today() #Extrae la fecha actual y la almacena en una variable para su posterior insercción en la BD
        #Inserta la publicación en la BD
        cursor = mysql.connection.cursor()
        publicaciones = cursor.execute(f'insert into publicaciones(titular, contenido, creador, tematica, Fecha_creacion) values ("{titular}", "{cuerpo}", "{id_user[0][0]}", "{tematica}", "{fecha_comentario}")')
        data = cursor.fetchall()
        mysql.connection.commit()
        return redirect(url_for('inicio'))
    else:
        return render_template('hecho.html')
#Ruta del inicio de los admins
@app.route('/inicio_admin')
def inicio_admin():
    cursor = mysql.connection.cursor()
    evaluar_tipo = cursor.execute(f'select tipo_usuario from usuarios where nombre="{user}"')
    data = cursor.fetchall()
    mysql.connection.commit()
    if data[0][0] == "Admin": #Comprueba si el usuario que está accediendo a la ruta es administrador o no
        #Mostrar los usuarios que no sean admins
        cursor1 = mysql.connection.cursor()
        mostrar_usuarios = cursor1.execute('select * from usuarios where tipo_usuario="Usuario" or tipo_usuario="Editorial"')
        data1 = cursor1.fetchall()
        #Mostrar las publicaciones junto a su creador
        cursor2 = mysql.connection.cursor()
        mostrar_publicaciones = cursor2.execute('select p.id, p.titular, p.Fecha_creacion, u.nombre from usuarios u inner join publicaciones p on u.id = p.creador')
        data2 = cursor2.fetchall()
        cursor3 = mysql.connection.cursor()
        id_usuario = cursor3.execute(f'select id from usuarios where nombre = "{user}"')
        #Se extrae, en una variable global, el id del admin para realizar futuras operaciones
        global id_user
        id_user = cursor3.fetchall()
        mysql.connection.commit()
        return render_template('inicio_admin.html', usuarios=data1, noticias=data2)
    else: #En caso de que se intente acceder a la ruta desde un usuario no admin, saltará un mensaje de error
        return 'Acceso denegado'
#Ruta de redacción de posts (admin)
@app.route('/inicio/redactar_admin', methods=['POST', 'GET'])
def redactar_admin():
    if request.method == 'POST':
        titular = request.form['titular']
        cuerpo = request.form['cuerpo']
        tematica = request.form['topic']
        fecha_comentario = date.today()
        cursor = mysql.connection.cursor()
        publicaciones = cursor.execute(f'insert into publicaciones(titular, contenido, creador, tematica, Fecha_creacion) values ("{titular}", "{cuerpo}", "{id_user[0][0]}", "{tematica}", "{fecha_comentario}")')
        data = cursor.fetchall()
        mysql.connection.commit()
        return redirect(url_for('inicio_admin'))
    else:
        return render_template('index_admin.html')
#Ruta para ordenar usuarios y posts        
@app.route('/inicio_admin/ordenar', methods=['POST', 'GET'])
def ordenar():
    if request.method == 'POST':
        ordenar_users = request.form['orderby'] #Extrae el criterio de ordenación establecido en el formulario
        cursor1 = mysql.connection.cursor()
        cursor2 = mysql.connection.cursor()
        if ordenar_users == 'Alfabéticamente': #Ordena de la A-Z tanto usuarios como publicaciones
            usuarios = cursor1.execute('select * from usuarios where tipo_usuario="Usuario" or tipo_usuario="Editorial" order by nombre asc')
            publicaciones = cursor2.execute('select p.id, p.titular, p.Fecha_creacion, u.nombre from usuarios u inner join publicaciones p on u.id = p.creador order by p.titular asc')
            data1 = cursor1.fetchall()
            data2 = cursor2.fetchall()
            return render_template('inicio_admin.html', usuarios=data1, noticias=data2)
        elif ordenar_users == 'Usuarios con más publicaciones': #Muestra primero los usuarios con más publicaciones 
            usuarios = cursor1.execute('select u.id, u.nombre, count(p.id) cant_publicaciones, u.tipo_usuario  from usuarios u inner join publicaciones p on u.id = p.creador where u.tipo_usuario = "Usuario" or u.tipo_usuario = "Editorial" group by u.id order by cant_publicaciones desc')
            data1 = cursor1.fetchall()
            return render_template('inicio_admin.html', usuarios=data1)
        elif ordenar_users == 'Usuarios con menos publicaciones': #Muestra primero los usuarios con menos publicaciones
            usuarios = cursor1.execute('select u.id, u.nombre, count(p.id) cant_publicaciones, u.tipo_usuario  from usuarios u inner join publicaciones p on u.id=p.creador where u.tipo_usuario="Usuario" or u.tipo_usuario="Editorial" group by u.id order by cant_publicaciones asc')
            data1 = cursor1.fetchall()
            return render_template('inicio_admin.html', usuarios=data1)
        elif ordenar_users == 'Publicaciones más recientes': #Muestra primero las publicaciones más recientes
            publicaciones = cursor2.execute('select p.id, p.titular, p.Fecha_creacion, u.nombre from usuarios u inner join publicaciones p on u.id = p.creador order by p.Fecha_creacion desc')
            data2 = cursor2.fetchall()
            return render_template('inicio_admin.html', noticias=data2)
        elif ordenar_users == 'Publicaciones menos recientes': #Muestra primero las publicaciones menos recientes
            publicaciones = cursor2.execute('select p.id, p.titular, p.Fecha_creacion, u.nombre from usuarios u inner join publicaciones p on u.id = p.creador order by p.Fecha_creacion asc')
            data2 = cursor2.fetchall()
            return render_template('inicio_admin.html', noticias=data2)
        mysql.connection.commit()
    else:
        return render_template('inicio_admin.html')
#Ruta para buscar usuario
@app.route('/inicio_admin/buscar_users', methods=['POST', 'GET'])
def buscar_users():
    if request.method == 'POST':
        buscar_user = request.form['buscar']
        cursor = mysql.connection.cursor()
        if buscar_user != '': #Comprueba si el campo no está vacio
            usuarios = cursor.execute(f'select * from usuarios where nombre like "%{buscar_user}%" and (tipo_usuario="Usuario" or tipo_usuario="Editorial")')
        else: #Si el campo está vacio salta este error
            return 'Error de búsqueda'
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('inicio_admin.html', usuarios=data)
    else:
        return render_template('inicio_admin.html')
#Ruta para buscar por tipo de usuario
@app.route('/inicio_admin/filtrar_tipo', methods=['POST', 'GET'])
def tipo_users():
    if request.method == 'POST':
        tipo = request.form['typeuser']
        cursor = mysql.connection.cursor()
        if tipo == 'Editorial':
            usuarios = cursor.execute('select * from usuarios where tipo_usuario="Editorial"')
        elif tipo == 'Usuario':
            usuarios = cursor.execute('select * from usuarios where tipo_usuario="Usuario"')
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('inicio_admin.html', usuarios=data)
    else:
        return render_template('explorar.html')
#Ruta para buscar posts
@app.route('/inicio_admin/buscar_posts', methods=['POST', 'GET'])
def buscar_post():
    if request.method == 'POST':
        buscar_post = request.form['buscar']
        cursor = mysql.connection.cursor()
        if buscar_post != '':
            publicaciones = cursor.execute(f'select * from publicaciones where titular like "%{buscar_post}%"')
        else:
            return 'Error de búsqueda'
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('inicio_admin.html', noticias=data)
    else:
        return render_template('inicio_admin.html')
#Ruta para buscar posts por mediante el creador
@app.route('/inicio_admin/buscar_posts_user', methods=['POST', 'GET'])
def buscar_post_user():
    if request.method == 'POST':
        buscar_post_user = request.form['buscar']
        cursor = mysql.connection.cursor()
        if buscar_post_user != '':
            publicaciones = cursor.execute(f'select p.id, p.titular, p.Fecha_creacion, u.nombre from usuarios u inner join publicaciones p on u.id = p.creador where u.nombre = "{buscar_post_user}"')
        else:
            return 'Error de búsqueda'
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('inicio_admin.html', noticias=data)
    else:
        return render_template('inicio_admin.html')
#Ruta para buscar posts mediante la fecha
@app.route('/inicio_admin/buscar_posts_fecha', methods=['POST', 'GET'])
def buscar_posts_fecha():
    if request.method == 'POST':
        buscar_posts_fecha = request.form['buscar']
        cursor = mysql.connection.cursor()
        if buscar_posts_fecha != '':
            publicaciones = cursor.execute(f'select * from publicaciones where Fecha_creacion = "{buscar_posts_fecha}"')
        else:
            return 'Error de búsqueda'
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('inicio_admin.html', noticias=data)
    else:
        return render_template('inicio_admin.html')
#Ruta para acceder a una publicación
@app.route('/inicio/noticia/<id>')
def news(id):
    #Se extrae, en una variable global, el id de la publicación en cuestión
    global id_publicacion
    id_publicacion = id
    #Se muestra datos relativos a la publicacion y a su creador
    cursor = mysql.connection.cursor()
    noticia = cursor.execute(f'select u.nombre, p.* from publicaciones p inner join usuarios u on u.id = p.creador where p.id = {id_publicacion}')
    data = cursor.fetchall()
    #Se muestra los comentarios de la publicación en cuestión
    cursor1 = mysql.connection.cursor()
    usuario_comentario = cursor1.execute(f'select u.nombre, c.contenido, c.fecha, u.id from usuarios u inner join comentarios c on u.id = c.usuarios inner join publicaciones p on p.id = c.publicaciones where p.id = {id} order by fecha desc')
    data1 = cursor1.fetchall()
    return render_template('noticia.html', titular=data[0][2], contenido=data[0][3], creador=data[0][0], fecha_publicacion=data[0][6], comentarios=data1)
#Ruta para establecer un comentario
@app.route('/inicio/noticia/comentario', methods=['POST', 'GET'])
def news_comment():
    if request.method == 'POST':
        comentario = request.form['comentario']
        fecha_comentario = date.today()
        cursor = mysql.connection.cursor()
        posteo = cursor.execute(f'insert into comentarios(contenido, fecha, publicaciones, usuarios) values ("{comentario}", "{fecha_comentario}", {id_publicacion}, {id_user[0][0]})')
        data = cursor.fetchall()
        mysql.connection.commit()
        return redirect(url_for('news', id=id_publicacion))
    else:
        return render_template('noticia.html')
#Ruta para editarse el usuario a si mismo (usuarios y editoriales)
@app.route('/inicio/editar_user/<id>', methods=['POST', 'GET'])
def edit_user(id):
    cursor = mysql.connection.cursor()
    usuario = cursor.execute(f'select * from usuarios where id = "{id_user[0][0]}"')
    data = cursor.fetchall()
    print(id_user)
    print(data)
    #Se restringe el acceso a otros usuarios mediante if (solo puede editarse a el mismo)
    if id_user[0][0] == data[0][0] : 
        if request.method == 'POST':
            user1 = request.form['user']
            passwd = request.form['pass']
            confirm_passwd = request.form['confirmpass']
            if passwd == confirm_passwd:
                cursor1 = mysql.connection.cursor()
                update = cursor1.execute('update usuarios set nombre = %s, pass = %s where id = %s', (user1, passwd, id_user))
                data1 = cursor1.fetchall()
                mysql.connection.commit()
                return redirect(url_for("login"))
            else:
                return 'Las contraseñas no coinciden'
        else:
            return render_template('edit_user.html', usuario=data, id=id_user)
    else:
        return 'Acceso denegado'
#Ruta para buscar un usuario y ver sus publicaciones
@app.route('/inicio/buscar_user/<usuario>', methods=['POST', 'GET'])
def buscar_user(usuario):
    if request.method == 'POST':
        barraBuscar = request.form['buscar']
        cursor = mysql.connection.cursor()
        usuario_buscar = cursor.execute(f'select * from usuarios where nombre = "{barraBuscar}"')
        data = cursor.fetchall()
        cursor1 = mysql.connection.cursor()
        publicaciones_usuario = cursor1.execute(f'select p.* from usuarios u inner join publicaciones p on u.id = p.creador where u.nombre = "{barraBuscar}" order by p.Fecha_creacion desc;')
        data1 = cursor1.fetchall()
        mysql.connection.commit()
        if usuario_buscar == True:
            return render_template('buscar_user.html', usuarios=data, publicaciones=data1)
        else:
            return 'El usuario no existe'
    else:
        return redirect(url_for("inicio", usuarios=data))
#Ruta explorar
@app.route('/inicio/explorar', methods=['POST', 'GET'])
def explorar():
    if request.method == 'POST':
        ordenar_por = request.form['orderby']
        cursor = mysql.connection.cursor()
        if ordenar_por == 'Más recientes':
            todas_publicaciones = cursor.execute('select * from publicaciones order by Fecha_creacion desc')
        elif ordenar_por == 'Más antiguos':
            todas_publicaciones = cursor.execute('select * from publicaciones order by Fecha_creacion asc')
        elif ordenar_por == 'Titular':
            todas_publicaciones = cursor.execute('select * from publicaciones order by titular asc')
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('explorar.html', publicaciones=data)
    else:
        return render_template('explorar.html')
#Ruta para buscar post por titular
@app.route('/inicio/explorar/buscar_titular', methods=['POST', 'GET'])
def explorar_titular():
    if request.method == 'POST':
        buscar_post = request.form['buscar']
        cursor = mysql.connection.cursor()
        if buscar_post != '':
            todas_publicaciones = cursor.execute(f'select * from publicaciones where titular like "%{buscar_post}%"')
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('explorar.html', publicaciones=data)
    else:
        return render_template('explorar.html')
#Ruta para buscar post por fecha
@app.route('/inicio/explorar/buscar_fecha', methods=['POST', 'GET'])
def explorar_fecha():
    if request.method == 'POST':
        buscar_fecha = request.form['buscar']
        cursor = mysql.connection.cursor()
        if buscar_fecha != '':
            todas_publicaciones = cursor.execute(f'select * from publicaciones where Fecha_creacion = "{buscar_fecha}"')
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('explorar.html', publicaciones=data)
    else:
        return render_template('explorar.html')
#Ruta para buscar post por temática
@app.route('/inicio/explorar/buscar_tematica', methods=['POST', 'GET'])
def explorar_temarica():
    if request.method == 'POST':
        buscar_tematica = request.form['topic']
        cursor = mysql.connection.cursor()
        if buscar_tematica != '':
            todas_publicaciones = cursor.execute(f'select * from publicaciones where tematica = "{buscar_tematica}"')
        data = cursor.fetchall()
        mysql.connection.commit()
        return render_template('explorar.html', publicaciones=data)
    else:
        return render_template('explorar.html')
#Ruta para borrar usuarios (menos los administradores)
@app.route('/inicio_admin/borrar_user/<id>', methods=['POST', 'GET'])
def borrar_user(id):
    cursor = mysql.connection.cursor()
    admins = cursor.execute(f'select tipo_usuario from usuarios where id = "{id}"')
    data = cursor.fetchall()
    if data[0][0] == 'Admin':
        return 'Error, no se puede eliminar un administrador'
    else:
        cursor1 = mysql.connection.cursor()
        borrar_usuario = cursor1.execute(f'delete from usuarios where id = "{id}"')
        data1 = cursor1.fetchall()
        mysql.connection.commit()
        return redirect(url_for("inicio_admin"))
#Ruta para borrar posts
@app.route('/inicio_admin/borrar_post/<id>', methods=['POST', 'GET'])
def borrar_post(id):
    cursor = mysql.connection.cursor()
    admins = cursor.execute(f'select tipo_usuario from usuarios where id = "{id}"')
    data = cursor.fetchall()
    if data == 'Admin':
        return 'Error, no se puede eliminar un administrador'
    else:
        cursor1 = mysql.connection.cursor()
        borrar_usuario = cursor1.execute(f'delete from publicaciones where id = "{id}"')
        data1 = cursor1.fetchall()
        mysql.connection.commit()
        return redirect(url_for("inicio_admin"))
@app.errorhandler(404)
def page_not_found(error):
    return 'Página no encontrada...', 404              
if __name__ == '__main__':
    app.run(debug=True) #El debug activo, permite ir actualizando y probando el código de la aplicación sin tener que desactivarla
