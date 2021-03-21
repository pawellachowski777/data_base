from flask import Flask, request
from main import sql_operation

app = Flask(__name__)
in_progress = False


@app.route('/status')
def status():
    global in_progress
    if in_progress:
        return "in progress"
    else:
        return "not in progress"


@app.route('/b2')
def sql():
    if request.method == 'GET':
        global in_progress
        in_progress = True
        sql_operation()
        in_progress = False
        return 'base operation'


if __name__ == "__main__":
    app.run(debug=True, port=7002)
