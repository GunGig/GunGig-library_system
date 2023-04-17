from common.sqlalchemy_helper import *
from common.database import db_session


class User(BaseModel):
    __tablename__ = 'user'

    # 定义类成员，并与数据库user表的列建立对应关系
    number = mapped_column(Integer, primary_key=True)
    username = mapped_column(String)
    password = mapped_column(String)
    school = mapped_column(String)

    # 赋值函数，调用该函数可以修改数据库中的值，传参方式为key=value，例如
    # user.set_value(number=1, username=zhangsan)
    def set_value(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        db_session.commit()

    # 用户注册接口
    @staticmethod
    def register(number, username, password, school):
        # 构造User类实例，并初始化各成员的值
        new_user = User(number=int(number), username=username, password=password, school=school)
        # 查询数据库中是否存在相同学号的记录
        result = db_session.query(User).filter(User.number == new_user.number).first()
        if result is not None:  # 如果查询结果不为空则表明用户已存在
            return -1

        # 向数据库中添加新用户
        db_session.add(new_user)
        db_session.commit()
        return 0

    # 用户登录接口
    @staticmethod
    def login(number, password):
        # 根据传入的学号、密码查询数据库中是否存在对应记录
        result = db_session.query(User).filter(User.number == int(number), User.password == password).count()
        if result == 0:  # 如果查不到则登录失败
            return -1
        else:  # 查到则登录成功
            return 0

    # 查询所有用户
    @staticmethod
    def query_all():
        return db_session.query(User).all()

    # 根据学号查询用户
    @staticmethod
    def query_by_number(number):
        user = db_session.query(User).filter(User.number == number).first()
        return user

    # 删除用户
    @staticmethod
    def delete(user):
        db_session.delete(user)

