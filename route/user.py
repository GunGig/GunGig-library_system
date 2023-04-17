from common.flask_helper import *
from common.message import Message
from model.book import Book
from model.history import History
from model.lease import Lease
from model.user import User
from model.order import Order
from model.recommend import Recommend
from model.comment import Comment
import time
import datetime

blueprint_user = Blueprint('user', __name__)


@blueprint_user.route('/user/<number>')
# 用户主页
def user_main_page(number):
    session['number'] = number
    return render_template('user.html', number=number)


# 图书搜索逻辑实现
@blueprint_user.route('/user/book_search', methods=['GET', 'POST'])
def user_book_search():
    message = Message()
    books = None
    if request.method == 'POST':
        if request.form['item'] == 'name':
            if not request.form['query']:
                message.set_error('请输入书名')
            else:
                books = Book.fuzzy_query_by_name(request.form['query'])
        else:
            if not request.form['query']:
                message.set_error('请输入作者名')
            else:
                books = Book.fuzzy_query_by_author(request.form['query'])
        if not books:
            message.set_error('未找到')
    return render_template('user_book_search.html ', books=books, message=message)


# 图书续借
def user_book_renewal(book_id):
    lease = Lease.query_by_book_id(book_id)
    if lease.renewal_cnt < 3:
        new_expired_date = lease.expired_date + datetime.timedelta(days=30)
        renewal_cnt = lease.renewal_cnt + 1
        lease.set_value(renewal_cnt=renewal_cnt, expired_date=new_expired_date)
        return 0
    else:
        return -1


# 图书借阅记录查询
@blueprint_user.route('/user/<number>/history')
def user_history(number):
    if request.args.get('action') == 'renewal' and request.args.get('bid'):
        result = user_book_renewal(int(request.args.get('bid')))
    histories = History.query_by_user_number(number)
    leases = Lease.query_by_user_number(number)
    orders = Order.query_by_user_number(number)
    return render_template('user_history.html ', histories=histories, leases=leases, orders=orders)

    # 用户信息管理


@blueprint_user.route('/user/<number>/detail', methods=['GET', 'POST'])
def user_detail(number):
    message = Message()
    if request.method == 'POST':
        if not request.form['password']:
            message.set_error('请输入新密码')
        elif not request.form['password2']:
            message.set_error('请确认新密码')
        elif request.form['password'] != request.form['password2']:
            message.set_error('两次密码不一致')

        user = User.query_by_number(number)
        user.set_value(password=request.form['password'])
        message.set_ok('密码修改成功')
    return render_template('user_detail.html', message=message)


# 图书信息
@blueprint_user.route('/user/book/<book_id>', methods=['GET', 'POST'])
def user_book_detail(book_id):
    message = Message()
    book = Book.query_by_id(book_id)
    if request.method == 'POST':
        if request.form.get('action') == 'comment':
            content = request.form.get('comment')
            if content:
                book = Book.query_by_id(book_id)
                Comment.add(book.ISBN, session['number'], content)
                message.set_ok('评论发布成功')
            else:
                message.set_error('评论不能为空')

    if request.args.get('action') == 'order':
        order_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
        expired_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 24 * 60 * 60))
        Order.add(book_id, session['number'], order_date, expired_date)
        message.set_ok('预借成功')

    if Lease.query_by_book_id(book_id):
        book.available = False

    elif Order.query_by_book_id(book_id):
        book.available = False
    comments = Comment.query_by_ISBN(book.ISBN)
    return render_template('user_book_detail.html ', book=book, comments=comments, message=message)


@blueprint_user.route('/user/<number>/recommend', methods=['GET', 'POST'])
def user_book_recommend(number):
    message = Message()
    if request.method == 'POST':
        if not request.form['ISBN']:
            message.set_error('请输入图书ISBN号')
        elif not request.form['name']:
            message.set_error('请输入书名')
        elif not request.form['author']:
            message.set_error('请输入作者')
        elif not request.form['publisher']:
            message.set_error('请输入出版社')
        else:
            if Book.query_by_ISBN(request.form['ISBN']):
                message.set_error('图书已存在库中')
            elif Recommend.query_by_ISBN(request.form['ISBN']):
                message.set_error('图书已存在荐购清单中')
            else:
                Recommend.add(number, request.form['ISBN'], request.form['name'], request.form['author'],
                              request.form['publisher'])
                message.set_ok('已将图书加入荐购清单')
    return render_template('user_book_recommend.html ', message=message)
