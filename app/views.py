from flask.views import MethodView
from flask import request, jsonify
from models import Usuario, Entrada, Comentario, Categoria
from schemas import EntradaSchema, UsuarioSchema, ComentarioSchema, CategoriaSchema
from app import app, db

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
entrada_schema = EntradaSchema()
entradas_schema = EntradaSchema(many=True)
comentario_schema = ComentarioSchema()
comentarios_schema = ComentarioSchema(many=True)
categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)

class UsuarioView(MethodView):
    def get(self, user_id):
        if user_id:
            user = Usuario.query.get(user_id)
            if user:
                return usuario_schema.jsonify(user)
            return jsonify({"message": "Usuario no encontrado"}), 404
        usuarios = Usuario.query.all()
        return usuarios_schema.jsonify(usuarios)

    def post(self):
        data = request.get_json()
        new_user = usuario_schema.load(data)
        db.session.add(new_user)
        db.session.commit()
        return usuario_schema.jsonify(new_user), 201

    def put(self, user_id):
        user = Usuario.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        data = request.get_json()
        user.username = data['username']
        db.session.commit()
        return usuario_schema.jsonify(user)

    def delete(self, user_id):
        user = Usuario.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado"}), 301

class EntradaView(MethodView):
    def get(self, entrada_id):
        if entrada_id:
            entrada = Entrada.query.get(entrada_id)
            if entrada:
                return entrada_schema.jsonify(entrada)
            return jsonify({"message": "Entrada no encontrada"}), 404
        entradas = Entrada.query.all()
        return entradas_schema.jsonify(entradas)

    def post(self):
        data = request.get_json()
        nueva_entrada = entrada_schema.load(data)
        db.session.add(nueva_entrada)
        db.session.commit()
        return entrada_schema.jsonify(nueva_entrada), 201

    def put(self, entrada_id):
        entrada = Entrada.query.get(entrada_id)
        if not entrada:
            return jsonify({"message": "Entrada no encontrada"}), 404

        data = request.get_json()
        entrada.titulo = data['titulo']
        entrada.contenido = data['contenido']
        db.session.commit()
        return entrada_schema.jsonify(entrada)

    def delete(self, entrada_id):
        entrada = Entrada.query.get(entrada_id)
        if not entrada:
            return jsonify({"message": "Entrada no encontrada"}), 404

        db.session.delete(entrada)
        db.session.commit()
        return jsonify({"message": "Entrada eliminada"})

class ComentarioView(MethodView):
    def get(self, comentario_id):
        if comentario_id:
            comentario = Comentario.query.get(comentario_id)
            if comentario:
                return comentario_schema.jsonify(comentario)
            return jsonify({"message": "Comentario no encontrado"}), 404
        else:
            comentarios = Comentario.query.all()
            return comentarios_schema.jsonify(comentarios)

    def post(self):
        data = request.get_json()
        nuevo_comentario = comentario_schema.load(data)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return comentario_schema.jsonify(nuevo_comentario), 201

    def put(self, comentario_id):
        comentario = Comentario.query.get(comentario_id)
        if not comentario:
            return jsonify({"message": "Comentario no encontrado"}), 404

        data = request.get_json()
        comentario.texto = data['texto']
        db.session.commit()
        return comentario_schema.jsonify(comentario)

    def delete(self, comentario_id):
        comentario = Comentario.query.get(comentario_id)
        if not comentario: 
            return jsonify({"message": "Comentario no encontrado"}), 404

        db.session.delete(comentario)
        db.session.commit()
        return jsonify({"message": "Comentario eliminado"})

class CategoriaView(MethodView):
    def get(self, categoria_id):
        if categoria_id:
            categoria = Categoria.query.get(categoria_id)
            if categoria:
                return categoria_schema.jsonify(categoria)
            return jsonify({"message": "Categoría no encontrada"}), 404
        else:
            categorias = Categoria.query.all()
            return categorias_schema.jsonify(categorias)

    def post(self):
        data = request.get_json()
        nueva_categoria = categoria_schema.load(data)
        db.session.add(nueva_categoria)
        db.session.commit()
        return categoria_schema.jsonify(nueva_categoria), 201

    def put(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify({"message": "Categoría no encontrada"}), 404

        data = request.get_json()
        categoria.nombre = data['nombre']
        db.session.commit()
        return categoria_schema.jsonify(categoria)

    def delete(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify({"message": "Categoría no encontrada"}), 404

        db.session.delete(categoria)
        db.session.commit()
        return jsonify({"message": "Categoría eliminada"})
