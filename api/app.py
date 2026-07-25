from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance import DevelopConfig, ProductionConfig, TestingConfig

app = Flask(__name__)
app.config.from_object(DevelopConfig)   # Establecemo configuraciones de desarrollo

db = SQLAlchemy(app)    # Establecemos la base de datos

@app.route('/prueba')
def test():
    return f"<h1> Mensaje de prueba </h1>"

if __name__ == "__main__":
    app.run(debug=True, port= 5000, host="0.0.0.0")