from flask import Flask
import requests
from main import sql_take_row

app = Flask(__name__)


def check_status():
    status_1 = requests.request(method='GET', url="http://127.0.0.1:7001/status")
    status_2 = requests.request(method='GET', url="http://127.0.0.1:7002/status")
    status_3 = requests.request(method='GET', url="http://127.0.0.1:7003/status")
    return status_1.text, status_2.text, status_3.text


def run_server(server_index):
    requests.request(method='GET', url=f"http://127.0.0.1:700{server_index}/b{server_index}")
    print('server', server_index, 'is free')


@app.route('/base')
def sql():
    b1_status, b2_status, b3_status = check_status()
    print(f"""
    'b1:' {b1_status}
    'b2:' {b2_status} 
    'b3:' {b3_status}
    """)
    if sql_take_row():
        if b1_status == "not in progress":
            print("server 1 is running")
            run_server(1)
            return 'data processed'
        elif b2_status == "not in progress":
            print("server 2 is running")
            run_server(2)
            return 'data processed'
        elif b3_status == "not in progress":
            print("server 3 is running")
            run_server(3)
            return 'data processed'
        else:
            return 'no free servers'
    else:
        return "base up to date"


if __name__ == "__main__":
    app.run(debug=True, port=7000)
