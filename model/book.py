from common.sqlalchemy_helper import *
from common.database import db_session


class Book(BaseModel):
    __tablename__ = 'book'

    # 定义类成员，并与数据库user表的列建立对应关系
    id = mapped_column(Integer, primary_key=True)
    ISBN = mapped_column(String)
    author = mapped_column(String)
    publisher = mapped_column(String)
    name = mapped_column(String)

    # 用于表示图书是否可用的属性，图书详情页需要根据该属性决定显示内容
    # 例如可用时显示在库，不可用时显示借出
    available = True

    # 查询所有图书
    @staticmethod
    def query_all():
        return db_session.query(Book).all()

    # 添加图书
    @staticmethod
    def add(ISBN, name, author, publisher):
        new_book = Book()
        new_book.ISBN = ISBN
        new_book.name = name
        new_book.author = author
        new_book.publisher = publisher
        db_session.add(new_book)
        db_session.commit()
        return 0

    # 根据作者查询图书
    @staticmethod
    def query_by_author(author):
        return db_session.query(Book).filter(Book.author == author).all()

    # 根据书名查询图书
    @staticmethod
    def query_by_name(name):
        return db_session.query(Book).filter(Book.name == name).all()

    # 根据ID查询图书
    @staticmethod
    def query_by_id(book_id):
        return db_session.query(Book).filter(Book.id == book_id).first()

    # 根据ISBN查询图书
    @staticmethod
    def query_by_ISBN(book_ISBN):
        return db_session.query(Book).filter(Book.ISBN == book_ISBN).first()

    # 根据书名模糊查询
    @staticmethod
    def fuzzy_query_by_author(author):
        return db_session.query(Book).filter(Book.author.like(f'%{author}%')).all()

    # 根据作者模糊查询
    @staticmethod
    def fuzzy_query_by_name(name):
        return db_session.query(Book).filter(Book.name.like(f'%{name}%')).all()

    # 删除图书
    @staticmethod
    def delete(book):
        db_session.delete(book)
        db_session.commit()

    # 赋值函数，调用该函数可以修改数据库中的值，传参方式为key=value，例如
    # book.set_value(name="Python编程")
    def set_value(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        db_session.commit()
