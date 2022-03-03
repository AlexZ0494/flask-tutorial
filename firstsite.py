import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort
from FDataBase import FDataBase

# Configs
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = 'dshfsdgjdsghodasgbdsigsd'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    db = get_db()
    # menu = get_mainmenu(db)
    dbase = FDataBase(db)
    return render_template('start.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    db = get_db()
    dbbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbbase.add_Post(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка записи статьи на сайт!', category='error')
            else:
                flash('Статья успешно загружена!', category='succes')
        else:
            flash('Малое колличество символов в статье!', category='error')
    return render_template('add_post.html', menu=dbbase.getMenu(), title='Добавление статьи')


@app.route('/post/<int:id_post>')
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.GetPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


if __name__ == '__main__':
    app.run(debug=True)
