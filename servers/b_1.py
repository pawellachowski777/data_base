from flask import Flask

app = Flask(__name__)


@app.route('/b1')
def sql():

    return 'ok'


if __name__ == "__main__":
    app.run(debug=True, port=7001)
