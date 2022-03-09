from flask import Flask, render_template, make_response, url_for, request, session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c433f5709159453e08ae730a6e481cbf5142a862589db7f9153c5d5089f3'


@app.route('/')
def index():
    print(session)
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return f'<H1>Main page</H1><p>Колличестов просмотров: {session["visits"]}</p>'


if __name__ == '__main__':
    app.run(debug=True)