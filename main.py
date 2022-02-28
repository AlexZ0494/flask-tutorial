from flask import Flask, render_template, request, flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dshfsdgjdsghodasgbdsigsd'

menu = [
        {'name': 'Установка', 'url': 'inst_flask'},
        {'name': 'Приложение', 'url': 'app'},
        {'name': 'О сайте', 'url': 'about'},
        {'name': 'Обратная связь', 'url': 'contact'}
       ]


@app.route('/')
def index():
    return render_template('start.html', H1='Это главная страница', menu=menu)


@app.route('/about')
def about():
    return render_template('start.html', title='О сайте', H1='О сайте')


@app.route('/profile/<username>')
def profile(username):
    return f'Пользователь: {username}'


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка!')
        print(request.form)
    return render_template('contact.html', title = 'Обратная связь', H1='Обратная связь', menu=menu)


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('err_page.html', title='Страница не найдена', menu=menu), 404


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=3000)
