from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from models import Usuario, Entrada, Comentario, Categoria
from views import UsuarioView, EntradaView, ComentarioView, CategoriaView
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import secrets
import os

usuario_view = UsuarioView.as_view('usuario_view')
entrada_view = EntradaView.as_view('entrada_view')
comentario_view = ComentarioView.as_view('comentario_view')
categoria_view = CategoriaView.as_view('categoria_view')

from models import Usuario, Entrada, Comentario, Categoria
from schemas import UsuarioSchema, CategoriaSchema, EntradaSchema, ComentarioSchema
from views import UsuarioView, EntradaView, ComentarioView, CategoriaView

# Crear instancias de las clases MethodView
usuario_view = UsuarioView.as_view('usuario_view')
entrada_view = EntradaView.as_view('entrada_view')
comentario_view = ComentarioView.as_view('comentario_view')
categoria_view = CategoriaView.as_view('categoria_view')

# Definir las rutas para acceder a las vistas
app.add_url_rule('/usuarios/', defaults={'user_id': None}, view_func=usuario_view, methods=['GET'])
app.add_url_rule('/usuarios/', view_func=usuario_view, methods=['POST'])
app.add_url_rule('/usuarios/<int:user_id>', view_func=usuario_view, methods=['GET', 'PUT', 'DELETE'])

app.add_url_rule('/entradas/', defaults={'entrada_id': None}, view_func=entrada_view, methods=['GET'])
app.add_url_rule('/entradas/', view_func=entrada_view, methods=['POST'])
app.add_url_rule('/entradas/<int:entrada_id>', view_func=entrada_view, methods=['GET', 'PUT', 'DELETE'])

app.add_url_rule('/comentarios/', defaults={'comentario_id': None}, view_func=comentario_view, methods=['GET'])
app.add_url_rule('/comentarios/', view_func=comentario_view, methods=['POST'])
app.add_url_rule('/comentarios/<int:comentario_id>', view_func=comentario_view, methods=['GET', 'PUT', 'DELETE'])

app.add_url_rule('/categorias/', defaults={'categoria_id': None}, view_func=categoria_view, methods=['GET'])
app.add_url_rule('/categorias/', view_func=categoria_view, methods=['POST'])
app.add_url_rule('/categorias/<int:categoria_id>', view_func=categoria_view, methods=['GET', 'PUT', 'DELETE'])

@app.context_processor
def categorias_disponibles():
    categorias = Categoria.query.all()
    return dict(categorias=categorias)

@app.route('/')
def index():
    print(os.environ)
    return render_template('index.html')

@app.route('/posteos')
def posteos():
    posts = Entrada.query.all()
    return render_template('posteos.html', posts=posts)

@app.route('/categoria/<int:categoria_id>')
def categoria(categoria_id):
    categoria = Categoria.query.get(categoria_id)
    entradas = categoria.entradas  
    return render_template('categoria.html', categoria=categoria, entradas=entradas)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password= request.form['password']
        password_hasheada = generate_password_hash(
            password=password, 
            method="pbkdf2", 
            salt_length=8
            )

        # Verifica si el nombre de usuario ya existe en la base de datos
        usuario_existente = Usuario.query.filter_by(username=username).first()
        if usuario_existente:
            flash('El nombre de usuario ya está en uso. Por favor, elige otro.', 'error')
        else:
            # Crea un nuevo usuario con las credenciales ingresadas
            nuevo_usuario = Usuario(username=username, password=password_hasheada)
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Registro exitoso. Inicia sesión con tus nuevas credenciales.', 'success')
            return redirect(url_for('login'))

    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar si el usuario existe y la contraseña es válida
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and check_password_hash(usuario.password, password):
            # Generar un token de acceso único
            access_token = secrets.token_hex(16)
            # Calcular la fecha y hora de expiración
            expiration_time = datetime.utcnow() + timedelta(minutes=30)
            # Asignar el token y su expiración al usuario en la base de datos
            usuario.access_token = access_token
            usuario.token_expiration = expiration_time
            db.session.commit()
            session['user_id'] = usuario.id
            flash('Inicio de sesión exitoso', 'success')
            # Redirigir a la página de creación de posteos con el token de acceso
            return redirect(url_for('crear_posteo', access_token=access_token))
        else:
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'error')

    return render_template('login.html')

@app.route('/crear_posteo', methods=['GET', 'POST'])
def crear_posteo():
    if 'user_id' not in session:
        # Si el usuario no ha iniciado sesión, redirigir a inicio de sesión
        flash('Inicia sesión para crear un posteo.', 'info')
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        categoria_id = int(request.form['categoria'])

        nueva_entrada = Entrada(
            titulo=titulo,
            contenido=contenido,
            fecha_creacion=datetime.now(),
            autor_id=session['user_id'],
            categoria_id=categoria_id
        )

        db.session.add(nueva_entrada)

        db.session.commit()

        flash('Posteo creado exitosamente.', 'success')
        return redirect(url_for('posteos'))

    categorias = Categoria.query.all()
    return render_template('crear_posteo.html', categorias=categorias)


@app.route('/post/<int:post_id>')
def ver_post(post_id):
    post = Entrada.query.get(post_id)
    print(post)  
    return render_template('ver_post.html', post=post)

@app.route('/post/<int:post_id>/comentar', methods=['POST'])
def comentar(post_id):
    if 'user_id' not in session:
        flash('Inicia sesión para comentar.', 'info')
        return redirect(url_for('login'))

    texto_comentario = request.form['comentario']
    autor_id = session['user_id'] 

    nuevo_comentario = Comentario(texto=texto_comentario, fecha_creacion=datetime.now(),
                                  autor_id=autor_id, entrada_id=post_id)
    db.session.add(nuevo_comentario)
    db.session.commit()
    return redirect(url_for('ver_post', post_id=post_id))

@app.route('/logout')
def logout_view():
    if 'user_id' in session:
        del session['user_id']
        flash('Has cerrado sesión', 'success')
    return redirect(url_for('index'))
