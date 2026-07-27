from flask_sqlalchemy import SQLAlchemy

# Creamos una instancia de SQLAlchemy. Para inicializarla, la importamos en app.py y usamos "db.init_app(app)"
db = SQLAlchemy()