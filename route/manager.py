from common.flask_helper import *
from common.database import db_session
from model.book import Book
from model.lease import Lease
from model.order import Order
from model.user import User
from model.history import History
from model.recommend import Recommend
from model.comment import Comment

from common.message import Message

import time

blueprint_manager = Blueprint('manager', __name__)


# 管理员主页
@blueprint_manager.route('/manager')
def manager_main_page():
    return render_template('manager.html')


# ---------------------------图书管理---------------------------
# 图书列表
@blueprint_manager.route('/manager/books', methods=['GET', 'POST'])
def manager_books():
    if request.args.get('action') == 'delete':
        book = Book.query_by_id(int(request.args.get('book_id')))
        Book.delete(book)
    books = Book.query_all()
    return render_template('manager_books.html', books=books)


# 添加图书
@blueprint_manager.route('/manager/books/add', methods=['GET', 'POST'])
def manager_books_add():
    message = Message()
    if request.method == 'POST':
        a = request.form['shul']
        if not request.form['ISBN']:
            message.set_error('请输入图书ISBN号')
        elif not request.form['name']:
            message.set_error('请输入书名')
        elif not request.form['author']:
            message.set_error('请输入作者')
        elif not request.form['publisher']:
            message.set_error('请输入出版社')
        elif not request.form['shul']:
            message.set_error('请输入数量')
        else:
            for i in range(eval(a)):
                Book.add(request.form['ISBN'], request.form['name'],
                         request.form['author'], request.form['publisher'])
            message.set_ok('添加成功')

    return render_template('manager_books_add.html', message=message)


# 删除图书
@blueprint_manager.route('/manager/books/delete', methods=['GET', 'POST'])
def manager_books_delete():
    message = Message()
    if request.method == 'POST':
        if not request.form['book_id']:
            message.set_error('请输入图书编号')
        else:
            book = Book.query_by_id(int(request.form['book_id']))
            lease = Lease.query_by_book_id(int(request.form['book_id']))
            if book is None:
                message.set_error('图书不存在')
            elif lease is not None:
                message.set_error('该图书未归还')
            else:
                Book.delete(book)
                message.set_ok(f'图书编号：{request.form["book_id"]}删除成功')
    return render_template('manager_books_delete.html', message=message)


# 单本图书管理
@blueprint_manager.route('/manager/book/<book_id>')
def manager_book(book_id):
    message = Message
    if request.args.get('action') is not None:
        message=manager_books_action()
    book = Book.query_by_id(book_id)
    lease = Lease.query_by_book_id(book_id)
    comments = Comment.query_by_ISBN(book.ISBN)
    return render_template('manager_book.html', book=book, lease=lease, comments=comments, message=message)


# 单本图书修改页
@blueprint_manager.route('/manager/book/<book_id>/detail', methods=['GET', 'POST'])
def manager_book_modify(book_id):
    book=Book.query_by_id(book_id)
    message=Message()
    if request.method=='POST':
        if not request.form['ISBN']:
            message.set_error('ISBN不能为空')
        elif not request.form['name']:
            message.set_error('书名不能为空')
        elif not request.form['author']:
            message.set_error('作者不能为空')
        elif not request.form['publisher']:
            message.set_error('出版社不能为空')
        if message.type != Message.ERROR:
            book.set_value(ISBN=request.form['ISBN'], name=request.form['name'],
                           author=request.form['author'], publisher=request.form['publisher'])
            return redirect(url_for('manager.manager_book', book_id=book_id))
    return render_template('manager_book_detail.html', book=book, message=message)


# 书评管理
@blueprint_manager.route('/manager/books/recommend')
def manager_book_recommend():
    message = Message()
    if request.args.get('action') =='delete':
        if request.args.get('rid'):
            Recommend.delete(int(request.args.get('rid')))
            message.set_ok('荐购信息删除成功')
    recommend_list =Recommend.query_all()
    return render_template('manager_book_recommend.html', recommend_list=recommend_list)


# ---------------------------借阅管理---------------------------
# 租约管理
@blueprint_manager.route('/manager/lease/<book_id>', methods=['GET', 'POST'])
def manager_lease(book_id):
    message = Message()
    book = Book.query_by_id(book_id)
    lease = Lease.query_by_book_id(book_id)
    order = Order.query_by_book_id(book_id)
    if request.method == 'POST':
        if request.form.get('lend'):
            if not request.form['number']:
                message.set_error('借阅人学号不能为空')
            user = User.query_by_number(request.form['number'])
            if not user:
                message.set_error('借阅人不存在')
            if message.type != Message.ERROR:
                borrow_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                expired_date = time.strftime('%Y-%m-%d',time.localtime(time.time() - 30 * 24 * 60 * 60))
                Lease.add(book_id,user.number,borrow_date,expired_date)
                lease = Lease.query_by_book_id(book_id)
                if not lease:
                    message.set_error('借阅失败，请重试')
        elif request.form.get('return'):
            if lease:
                user = User.query_by_number(lease.user_number)
                return_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                History.add(book_id, user.number, lease.borrow_date,return_date)
                Lease.delete(lease)
                lease = None
        elif request.form['order_accept']:
            if order:
                borrow_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                expired_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 30 * 24 * 60 * 60))
                Lease.add(book_id, order.user_number, borrow_date, expired_date)
                lease = Lease.query_by_book_id(book_id)
                if not lease:
                    message.set_error('借阅失败，请重试')
                else:
                    Order.delete_by_id(order.id)
                    order = None
        elif request.form['order_accept']:
            if order:
                Order.delete_by_id(order.id)
                order = None
    return render_template('manager_lease.html',book=book,lease=lease,order=order,message=message)



# 超期管理
@blueprint_manager.route('/manage/lease/expired')
def manager_lease_expired():
    today = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
    leases = Lease.query_by_date_before(today)
    return render_template('manager_lease_expired.html ', leases=leases)



# ---------------------------用户管理---------------------------
# 用户列表
@blueprint_manager.route('/manager/users')
def manager_users():
    users = User.query_all()
    return render_template('manager_users.html', users=users)


@blueprint_manager.route('/manager/user/<number>', methods=['GET', 'POST'])
def manager_user(number):
    message = Message()
    user = User.query_by_number(number)
    leases = Lease.query_by_user_number(number)
    if request.args.get('action') == 'delete':
        if len(leases) != 0:
            message.set_error(f'用户{number}有未还书籍,无法删除该用户')
        else:
            User.delete(user)
            return redirect(url_for('manager.manager_users'))
    results = []
    for lease in leases:
        book = Book.query_by_id(lease.book_id)
        results.append((lease.borrow_date, lease.expired_cate, book.name))
    return render_template('manager_user.html', user=user, results=results, me1=message)


@blueprint_manager.route('/manager/user/<number>/detail', methods=['GET', 'POST'])
def manager_user_detail(number):
    message = Message()
    user = User.query_by_number(number)
    if request.method == 'POST':
        if not request.form['username']:
            message.set_error('姓名不能为空')
        elif not request.form['school']:
            message.set_error('学院不能为空')
        if message.type !=Message.ERROR:
            user.set_value(school=request.form['school'],
                           username=request.form['username'])
            if request.form['password']:
                user.set_value(password=request.form['password'])
            message.set_ok('修改成功')
    return render_template('manager_user_detail.html', user=user, message=message)




# -------------------------------------功能函数------------------------------------- #
# 评论删除
def manager_books_action():
    abort(503)
