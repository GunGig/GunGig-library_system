from common.sqlalchemy_helper import *
from common.database import db_session

from model.book import Book


class History(BaseModel):
    __tablename__ = 'history'

    # 数据库表属性
    id = mapped_column(Integer, primary_key=True)
    user_number = mapped_column(Integer)
    book_id = mapped_column(Integer)
    borrow_date = mapped_column(Date)
    return_date = mapped_column(Date)

    # 其他属性
    book_name = None  # 书名

    # 根据学号查询历史信息
    @staticmethod
    def query_by_user_number(number):
        # 根据学号查询历史信息
        histories = db_session.query(History).filter(History.user_number == number).all()
        # 由于history表中没有书名项，因此需要遍历每条历史信息，根据该条历史信息的图书ID
        # 从book表中查询书名
        for history in histories:
            if history:
                book = Book.query_by_id(history.book_id)
                if book:
                    history.book_name = book.name

        return histories

    # 添加历史信息
    @staticmethod
    def add(book_id, user_number, borrow_date, return_date):
        new_history = History(book_id=book_id, user_number=user_number, borrow_date=borrow_date, return_date=return_date)
        db_session.add(new_history)
        db_session.commit()

