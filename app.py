from flask import Flask
from flask import render_template

from route.login import blueprint_login
from route.manager import blueprint_manager
from route.user import blueprint_user

app = Flask(__name__)

app.register_blueprint(blueprint_login)
app.register_blueprint(blueprint_manager)
app.register_blueprint(blueprint_user)

app.config['ADMIN_NAME'] = 'admin'
app.config['ADMIN_PWD'] = 'admin'
app.config['SECRET_KEY'] = 'abcdefgh'


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=80, debug=True)
