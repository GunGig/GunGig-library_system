from common.sqlalchemy_helper import *
from common.database import db_session

from sqlalchemy import Text


class Comment(BaseModel):
    __tablename__ = 'comment'

    # 与数据库comment表的列建立对应关系
    id = mapped_column(Integer, primary_key=True)
    user_number = mapped_column(Integer)
    book_ISBN = mapped_column(String)
    content = mapped_column(Text)

    # 新增书评
    @staticmethod
    def add(book_ISBN, user_number, content):
        new_comment = Comment()
        new_comment.book_ISBN = book_ISBN
        new_comment.user_number = user_number
        new_comment.content = content
        db_session.add(new_comment)
        db_session.commit()

    # 删除书评
    @staticmethod
    def delete(comment_id):
        db_session.query(Comment).filter(Comment.id == comment_id).delete()
        db_session.commit()

    # 根据ISBN查询书评
    @staticmethod
    def query_by_ISBN(ISBN):
        comments = db_session.query(Comment).filter(Comment.book_ISBN == ISBN).all()
        return comments
