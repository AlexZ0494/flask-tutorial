import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogined import UserLogin
from forms import LoginForm, RegisterForm

# Configs
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = 'c433f5709159453e08ae730a6e481cbf5142a862589db7f9153c5d5089f3'
MAX_CONTENT_LENGTH = 1024*1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


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


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def index():
    return render_template('start.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route('/addPost', methods=['POST', 'GET'])
def addPost(dbbase=None):
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbbase.add_Post(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка записи статьи на сайт!', category='error')
            else:
                flash('Статья успешно загружена!', category='succes')
        else:
            flash('Малое колличество символов в статье!', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавление статьи')


@app.route('/post/<alias>')
@login_required
def showPost(alias):
    title, post = dbase.GetPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['password'], form.pas.data):
            userlog = UserLogin().create(user)
            rm = form.rememer.data
            login_user(userlog, remember=rm)
            return redirect(request.args.get('next') or url_for('profile'))

        flash('Не верная пара логин/пароль', 'error')

    return render_template('login.html', menu=dbase.getMenu(), title='Авторизация', form=form)
    # if request.method == 'POST':
    #     user = dbase.getUserByEmail(request.form['email'])
    #     if user and check_password_hash(user['password'], request.form['passwd']):
    #         userlog = UserLogin().create(user)
    #         rm = True if request.form.get('remaine') else False
    #         login_user(userlog, remember=rm)
    #         return redirect(request.args.get('next') or url_for('profile'))
    #
    #     flash('Не верная пара логин/пароль', 'error')
    #
    # return render_template('login.html', menu=dbase.getMenu(), title='Авторизация' )


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_pass = generate_password_hash(form.pas.data)
        res = dbase.addUser(form.name.data, form.email.data, hash_pass)
        if res:
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Не верно заполнены поля', 'error')

    return render_template('register.html', menu=dbase.getMenu(), title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ВЫ вышли из профиля', 'success')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', menu=dbase.getMenu(), title=f'Профиль пользователя')


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if img:
        h = make_response(img)
        h.headers['Content-Type'] = 'image/png'
        return h
    else:
        return ''


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка загрузки аватара', 'error')
                    return redirect(url_for('profile'))
                flash('Аватар успешно загружен', 'success')
            except FileExistsError as e:
                flash(f'Ошибка чтения файла:{e}', 'error')

        else:
            flash('Обновление прошло неудачно', 'error')

    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(debug=True)
