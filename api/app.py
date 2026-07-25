from flask import Flask

app = Flask(__name__)

@app.route('/prueba')
def test():
    return f"<h1> Mensaje de prueba </h1>"

if __name__ == "__main__":
    app.run(debug=True, port= 5000, host="0.0.0.0")