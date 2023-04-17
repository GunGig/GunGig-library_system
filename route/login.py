from common.flask_helper import *

from common.message import Message
from model.user import User


blueprint_login = Blueprint('login', __name__)


# 管理员登录
@blueprint_login.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    message = Message()
    if request.method == 'POST':
        if request.form.get('username') == app.config['ADMIN_NAME'] and \
                request.form.get('password') == app.config['ADMIN_PWD']:
            session['username'] = app.config['ADMIN_NAME']  # 将用户名保存到session，用于在页面中显示当前用户
            return redirect(url_for('manager.manager_main_page'))
        else:
            message.set_error('账号或密码错误')
    return render_template('manager_login.html', message=message)


# 登出
@blueprint_login.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 用户登录
@blueprint_login.route('/user_login', methods=['GET', 'POST'])
def user_login():
    message = Message()
    if request.method == 'POST':
        number = request.form.get('number')
        password = request.form['password']
        result = User.login(number, password)
        if result == -1:
            message.set_error('账号或密码错误')
        else:
            session['number'] = number
            return redirect(url_for('user.user_main_page', number=number))
    elif request.method == 'GET' and session.get('number'):
        return redirect(url_for('user.user_main_page', number=session.get('number')))
    return render_template('user_login.html', message=message)


# 用户注册
@blueprint_login.route('/register', methods=['GET', 'POST'])
def register():
    message = Message()
    if request.method == 'POST':
        if not request.form['number']:
            message.set_error('请输入学号')
        elif not request.form['password']:
            message.set_error('请输入密码')
        elif request.form['password'] != request.form['password2']:
            message.set_error('两次密码不同')
        else:
            ret = User.register(number=request.form['number'], username=request.form['username'],
                                password=request.form['password'], school=request.form['school'],)
            if ret == 0:
                message.set_ok('注册成功')
            else:
                message.set_ok('用户已存在')
    return render_template('register.html', message=message)
