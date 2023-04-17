from common.sqlalchemy_helper import *
from common.database import db_session

from model.book import Book
from model.user import User

from datetime import date


class Lease(BaseModel):
    __tablename__ = 'lease'

    # 数据库lease表的ORM属性
    id = mapped_column(Integer, primary_key=True)
    user_number = mapped_column(Integer)
    book_id = mapped_column(Integer)
    borrow_date = mapped_column(Date)
    expired_date = mapped_column(Date)
    renewal_cnt = mapped_column(Integer)

    # 其他属性
    book_name = None  # 书名
    book_ISBN = None  # 图书ISBN
    user_name = None  # 借书者姓名
    expired = False  # 是否超期

    # 根据学号查询租约
    @staticmethod
    def query_by_user_number(number):
        # 根据学号查询所有租约
        leases = db_session.query(Lease).filter(Lease.user_number == number).all()
        # 由于lease表中没有书名信息，因此需要根据租约中的图书ID来查book表，获取书名信息
        for lease in leases:
            book = Book.query_by_id(lease.book_id)
            lease.book_name = book.name
            lease.expired = date.today() > lease.expired_date

        return leases

    # 根据图书编号查询租约
    @staticmethod
    def query_by_book_id(book_id):
        return db_session.query(Lease).filter(Lease.book_id == book_id).first()

    # 查询所有租约
    @staticmethod
    def query_all():
        return db_session.query(Lease).all()

    # 查询应还日期在给定日期之前的租约（即超期未还租约）
    @staticmethod
    def query_by_date_before(date):
        leases = db_session.query(Lease).filter(Lease.expired_date < date).all()

        for lease in leases:
            # 由于lease表中没有书名信息，因此需要根据租约中的图书ID来查book表，获取书名信息
            book = Book.query_by_id(lease.book_id)
            # # 由于lease表中没有借书人名信息，因此需要根据租约中的学号来查user表，获取人名信息
            user = User.query_by_number(lease.user_number)
            lease.book_name = book.name
            lease.book_ISBN = book.ISBN
            lease.user_name = user.username

        return leases

    # 添加图书
    @staticmethod
    def add(book_id, user_number, borrow_date, expired_date):
        new_lease = Lease(book_id=book_id, user_number=user_number,borrow_date=borrow_date, expired_date=expired_date)
        new_lease.renewal_cnt = 0
        db_session.add(new_lease)
        db_session.commit()

    # 删除图书
    @staticmethod
    def delete(lease):
        db_session.delete(lease)
        db_session.commit()

    # 设置图书属性值
    # **kwargs为可变参数语法
    def set_value(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        db_session.commit()
