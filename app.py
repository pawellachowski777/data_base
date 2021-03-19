from control import sql_control
from flask import Flask
import requests

app = Flask(__name__)


@app.route('/base')
def sql():
    sql_control()
    requests.request(method='GET', url="http://127.0.0.1:7001/b1")

    return str(sql_control())


if __name__ == "__main__":
    app.run(debug=True, port=7000)
