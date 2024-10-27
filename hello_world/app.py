from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify(message='Hola muchacho, estamos activos')

@app.route('/embergadura')
def embergadura():
    return jsonify(message='Para los baity entendidos')

if __name__ == '__main__':
    app.run()