from flask import jsonify
from app import app, ma, db, Usuario, Entrada, Comentario, Categoria
from marshmallow import Schema, fields, post_load

class UsuarioSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()

    @post_load
    def make_usuario(self, data, **kwargs):
        return Usuario(**data)
    
class CategoriaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()

    @post_load
    def make_categoria(self, data, **kwargs):
        return Categoria(**data)

class EntradaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    titulo = fields.String()
    contenido = fields.String()
    fecha_creacion = fields.DateTime()
    # Agrega el campo autor_id a tus datos serializados
    autor_id = fields.Integer()
    # Define un campo "autor" personalizado que serialice al autor
    autor = fields.String(attribute="autor.username", dump_only=True)
    categoria = fields.Nested(CategoriaSchema)

    @post_load
    def make_entrada(self, data, **kwargs):
        return Entrada(**data)

class ComentarioSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    texto = fields.String()
    fecha_creacion = fields.DateTime()
    autor = fields.Nested(UsuarioSchema)
    entrada = fields.Nested(EntradaSchema)

    @post_load
    def make_comentario(self, data, **kwargs):
        return Comentario(**data)

@app.route('/usuarios_json')
def usuarios_json():
    usuarios = Usuario.query.all()
    usuarios_schema = UsuarioSchema(many=True).dump(usuarios)
    return jsonify(usuarios_schema)

@app.route('/categorias_json')
def categorias_json():
    categorias = Categoria.query.all()
    categorias_schema = CategoriaSchema(many=True).dump(categorias)
    return jsonify(categorias_schema)

@app.route('/entradas_json')
def entradas_json():
    entradas = Entrada.query.all()
    entradas_schema = EntradaSchema(many=True).dump(entradas)
    return jsonify(entradas_schema)

@app.route('/comentarios_json')
def comentarios_json():
    comentarios = Comentario.query.all()
    comentarios_schema = ComentarioSchema(many=True).dump(comentarios)
    return jsonify(comentarios_schema)
