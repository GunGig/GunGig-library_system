from flask import Flask
import pymysql
import sqlalchemy

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='admin')
print(conn.get_server_info())


@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    app.run()
