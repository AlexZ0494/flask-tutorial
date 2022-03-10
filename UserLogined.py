import sqlite3

from flask import url_for
from flask_login import UserMixin

class UserLogin():


    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self


    def create(self, user):
        self.__user = user
        return self


    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return str(self.__user['id'])


    def getName(self):
        return self.__user['username'] if self.__user else 'Безымянный'


    def getEmail(self):
        return self.__user['email'] if self.__user else 'Нет почты'

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), 'rb') as f:
                    img = f.read()
            except FileExistsError as e:
                print(f'Отсутсвует аватар по умолчанию:{e}')
        else:
            img = self.__user['avatar']

        return img


    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == 'jpg' or ext == 'png':
            return True
        return False