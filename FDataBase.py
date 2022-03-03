import math
import time
import sqlite3


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

    def add_Post(self, title, text):
        try:
            tm = math.floor(time.time())
            print(tm)
            sql = ''' INSERT INTO posts VALUES (NULL, '{title}', '{text}', '{tmr}') '''.format(title=title, text=text, tmr=tm)
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка {err}'.format(err=e))
            return False
        return True

    def GetPost(self, id_post):
        try:
            sql = f''' SELECT title, text From posts WHERE id = {id_post} LIMIT 1'''
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
            sql = ''' SELECT id, title, text FROM posts ORDER BY time DESC '''
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка выборки статей: {err}'.format(err=e))

        return []