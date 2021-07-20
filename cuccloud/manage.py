# -*- encoding=UTF-8 -*-

from cuccloud import app, db
from flask_script import Manager
# from cuccloud.models import Like, User, Image, Comment
import random

manager = Manager(app)



# 初始化数据库 使用命令行


@manager.command
def init():
    db.drop_all()
    db.create_all()

    db.session.commit()


if __name__ == '__main__':
    manager.run()
