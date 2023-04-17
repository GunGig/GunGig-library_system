from common.sqlalchemy_helper import *
from common.database import db_session


class Recommend(BaseModel):
    __tablename__ = 'recommend'

    id = mapped_column(Integer, primary_key=True)
    user_number = mapped_column(Integer)
    book_ISBN = mapped_column(String)
    book_author = mapped_column(String)
    book_publisher = mapped_column(String)
    book_name = mapped_column(String)

    available = True

    @staticmethod
    def query_all():
        return db_session.query(Recommend).all()

    @staticmethod
    def add(user_number, book_ISBN, book_name, book_author, book_publisher):
        new_recommend = Recommend()
        new_recommend.user_number = int(user_number)
        new_recommend.book_ISBN = book_ISBN
        new_recommend.book_name = book_name
        new_recommend.book_author = book_author
        new_recommend.book_publisher = book_publisher
        db_session.add(new_recommend)
        db_session.commit()


    @staticmethod
    def delete(recomment_id):
        db_session.query(Recommend).filter(Recommend.id == recomment_id).delete()


    @staticmethod
    def query_by_ISBN(ISBN):
        return db_session.query(Recommend).filter(Recommend.book_ISBN == ISBN).all()

