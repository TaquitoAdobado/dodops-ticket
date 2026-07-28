from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance import DevelopConfig, ProductionConfig, TestingConfig
from extensions import db
from models import Ticket
from routes import tickets_bp

def create_app (configuration):

    app = Flask(__name__,)
    app.config.from_object(configuration)   # Establecemo configuraciones de desarrollo
    db.init_app(app)                        # Inicializamos la base de datos

    # Rutas
    @app.route('/prueba')
    def test():
        return f"<h1> Mensaje de prueba </h1>"

    # Registramos la blueprint de tickets
    app.register_blueprint(tickets_bp)

    with app.app_context():
        db.create_all()                     # Creamos las tablas al iniciar (solo en desarrollo)

    return app

if __name__ == "__main__":
    app = create_app(DevelopConfig)
    app.run(debug=True, port=5000, host="0.0.0.0")
