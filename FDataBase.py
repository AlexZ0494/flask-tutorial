import math
import re
import time
import sqlite3
import re
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Error read!')
        return []

    def check_url(self, url):
        sql = " SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}' ".format(url=url)
        self.__cur.execute(sql)
        res = self.__cur.fetchone()
        if res['count'] > 0:
            print('Статья с таким url уже существует')
            return False
        else:
            return True

    def add_Post(self, title, text, url):
        try:
            self.check_url(url)
            tm = math.floor(time.time())
            base = url_for('static', filename='images_html')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>", res['text'])
            sql = ''' INSERT INTO posts VALUES (NULL, '{title}', '{text}', '{url}', '{tmr}') '''.format(title=title, text=text, tmr=tm, url=url)
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка {err}'.format(err=e))
            return False
        return True

    def GetPost(self, alias):
        try:
            sql = f''' SELECT title, text From posts WHERE url LIKE '{alias}' LIMIT 1'''
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            print(res)
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка селекта {err}".format(err=e))

        return (False, False)

    def getPostsAnonce(self):
        try:
            sql = ''' SELECT id, title, text, url FROM posts ORDER BY time DESC '''
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка выборки статей: {err}'.format(err=e))

        return []

    def addUser(self, username, email, passwd):
        try:
            self.__cur.execute(f''' SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}' ''')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует!')
                return False
            tm = math.floor(time.time())
            sql = f''' INSERT INTO users VALUES (NULL, '{username}', '{email}', '{passwd}', NULL, '{tm}') '''
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка добавления в БД: {e}')
            return False

        return True


    def getUser(self, user_id):
        try:
            sql = f''' SELECT * FROM users WHERE id = {user_id} LIMIT 1 '''
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден!')
                return False

            return res

        except sqlite3.Error as e:
            print(f'Ошибка чтения данных: {e}')

        return False


    def getUserByEmail(self, email):
        try:
            sql = f''' SELECT * FROM users WHERE email = '{email}' LIMIT 1 '''
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден в БД')
                return False

            return res

        except sqlite3.Error as e:
            print(f'Ошибка чтения БД: {e}')

        return False

    def updateUserAvatar(self, img, user_id):
        if not img:
            return False
        try:
            binary = sqlite3.Binary(img)
            sql = f''' UPDATE users SET avatar = '{binary}' WHERE id = {user_id} '''
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка записи аватара в БД:{e}')
            return False
        return True