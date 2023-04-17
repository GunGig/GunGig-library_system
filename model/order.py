from common.sqlalchemy_helper import *
from common.database import db_session
from model.book import Book


class Order(BaseModel):
    __tablename__ = 'order'

    # 数据库order表的ORM属性
    id = mapped_column(Integer, primary_key=True)
    user_number = mapped_column(String)
    book_id = mapped_column(Integer)
    order_date = mapped_column(Date)
    expired_date = mapped_column(Date)

    book_name = None  # 书名

    # 添加预借信息
    @staticmethod
    def add(book_id, user_number, order_date, expired_date):
        order = Order(book_id=book_id, user_number=user_number, order_date=order_date, expired_date=expired_date)
        db_session.add(order)
        db_session.commit()

    # 根据预借ID删除预借信息
    @staticmethod
    def delete_by_id(order_id):
        db_session.query(Order).filter(Order.id == order_id).delete()

    # 根据图书ID查询预借信息
    @staticmethod
    def query_by_book_id(book_id):
        order = db_session.query(Order).filter(Order.book_id == book_id).first()

        # order表中没有书名信息，需要根据图书ID查询图书信息，以获得书名
        if order:
            book = db_session.query(Book).filter(Book.id == book_id).first()
            order.book_name = book.name
        return order

    # 根据用户学号查询预借信息
    @staticmethod
    def query_by_user_number(user_number):
        orders = db_session.query(Order).filter(Order.user_number == user_number).all()

        # order表中没有书名信息，需要根据图书ID查询图书信息，以获得书名
        if orders:
            for order in orders:
                book = db_session.query(Book).filter(Book.id == order.book_id).first()
                order.book_name = book.name
        return orders



