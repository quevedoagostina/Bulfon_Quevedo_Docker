from app import app
from app.database import db
from models import Usuario, Entrada, Comentario, Categoria

db.init_app(app)
