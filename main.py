import datetime
import flask
from flask import Flask, render_template, redirect, jsonify, make_response, send_file, current_app, send_from_directory
from flask_restful import abort, Api, Resource
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired
from data import db_session
from flask_login import LoginManager, login_user, login_manager, login_required, logout_user
from data.users import User
from data.workers import Workers
from forms.register import RegisterForm
from forms.carta import CartaForm
from forms.game import GameForm
from forms.game_create import DownloadForm
from data.games import Games
from data import games_api
from forms.user import UserForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbdir/test.db'
app.register_blueprint(games_api.blueprint)
UPLOAD_FOLDER = '/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
db_session.global_init("db/main_info.db")
login_manager = LoginManager()
login_manager.init_app(app)


def abort_if_news_not_found(game_name):
    session = db_session.create_session()
    games = session.query(Games).get(game_name)
    if not games:
        abort(404, message=f"Игра {game_name} не найденна")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    print(form.position.data == 'Разработчик')
    if form.validate_on_submit():
        print(form.position.data, 123)
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()

        print(form.email.data)
        if db_sess.query(User).filter(User.email == form.email.data).first() and \
            db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        print(form.position.data)
        if db_sess.query(User).filter(form.position.data == 'Разработчик'):
            user = User(
                surname=form.surname.data,
                name=form.name.data,
                email=form.email.data,
                age=form.age.data,
                position=form.position.data,
                hashed_password=form.password.data,
                nickname=form.nickname.data)
            db_sess.add(user)
            db_sess.commit()
            db_sess = db_session.create_session()
            worker = Workers(orm_user=user,
                             company_name=form.nickname.data,
                             worker_name=form.name.data,
                             worker_surname=form.surname.data,
                             worker_age=form.age.data
            )
            user.set_password(form.password.data)

            db_sess.add(worker)
            db_sess.commit()
            login_user(user)
            return redirect("/")
        modified_date = datetime.datetime.now()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            hashed_password=form.password.data,
            modified_date=modified_date,
            nickname=form.nickname.data,
            )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')




class GamesResource(Resource):
    def get(self, game_name):
        abort_if_news_not_found(game_name)
        session = db_session.create_session()
        game = session.query(Games).get(game_name)
        return jsonify({'Games': game.to_dict(
            only=('game_name', 'genre', 'cost', 'picture_url', 'description', 'company',
                  'size_GB', 'version', 'created_date', 'buyers', 'status', 'multiplayer'))})

    def delete(self, game_name):
        abort_if_news_not_found(game_name)
        session = db_session.create_session()
        game = session.query(Games).get(game_name)
        session.delete(game)
        session.commit()
        return jsonify({'success': 'OK'})


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/', methods=['GET', 'POST'])
def main_window():
    return render_template('main_window.html', title='Меню')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/user/<user_name>',  methods=['GET', 'POST'])
def user_profile(user_name):
    form = UserForm()
    print(form.submit(), form.submit)
    if form.submit():
        print(123, form.new_url.data)
        if form.new_url.data:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.name == user_name).first()
            user.avatar = form.new_url.data
            db_sess.commit()
            return redirect(f'/user/{user_name}')
    print(form)
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.name == user_name).first()
    print('ggg')
    print(users.name)
    user = users
    print(1)
    name = user.name
    nickname = user.nickname
    avatar = user.avatar
    games = user.games
    age = user.age
    position = user.position
    print(2)
    print(games, 123)
    if not games:
        games = 'Нету у тебя игр'
    return render_template('profile.html', name=name, nickname=nickname, avatar=avatar, games=games,
                           position=position, age=age, form=form)


@app.route('/games', methods=['GET', 'POST'])
def get_games():
    form = GameForm()
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    print(games)
    print(form.game_name, form.validate_on_submit())
    if form.submit():
        print(form.validate_on_submit())
        game = db_sess.query(Games).filter(Games.game_name == form.game_name.data).first()
        print(game)
        if game:
            return redirect(f'/games/{form.game_name.data}')
    print(games)
    return render_template('katalog.html', games=[item.to_dict(only=('game_name', 'genre', 'cost',
                                                                     'picture_url', 'description')) for item in games],
                           form=form)

@app.route('/user/<user_name>/games', methods=['GET', 'POST'])
def my_games(user_name):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.name == user_name).first()
    user = users
    if users.games:
        games = users.games.split()
    else:
        games = []
    games1 = []
    for i in games:
        if db_sess.query(Games).filter(Games.game_name == i).first():
            games1.append(db_sess.query(Games).filter(Games.game_name == i).first())
    return render_template('my_games.html', games=games1)


@app.route('/games/<game_name>')
def get_game(game_name):
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    f = open(f'{game_name}.txt', encoding='utf-8')
    shuget = f.read()
    return render_template('game_revie.html', shuget=shuget, games=[item.to_dict(only=('game_name', 'genre', 'cost',
                                                                        'picture_url', 'description', 'company',
                                                                        'size_GB', 'version', 'created_date',
                                                                        'multiplayer',
                                                                        ))for item in games if item.game_name == game_name])


@app.route('/<user_name>/games/<game_name>/buying', methods=['GET', 'POST'])
@login_required
def buy_game(user_name, game_name):
    db_sess = db_session.create_session()
    games = db_sess.query(Games).all()
    form = CartaForm()
    if form.submit():
        print(123)
        print(form.cvv.data, form.month.data, form.year.data, form.numb.data)
        if form.cvv.data and form.month.data and form.year.data and form.numb.data:
            user = db_sess.query(User).filter(User.name == user_name).first()
            if user.games:
                user.games = user.games + f' {game_name}'
            else:
                user.games = game_name
            db_sess.commit()
            return redirect('/')

    return render_template('buy_game.html', game=[item.to_dict(only=('game_name', 'cost'))
                                                     for item in games if item.game_name == game_name][0], form=form)

@app.route('/kotolog')
def kotolog():
    koti = ['https://s1.best-wallpaper.net/wallpaper/m/2109/Cute-little-kitten-cat-look-green-background_m.jpg',
            'https://hotwalls.ru/thumbnails/lg/malenkiy_seryy_kotenok.jpg',
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5EYftpWRcKQ4EgngyVqGzUVljIOi_33VR7Q&usqp=CAU',
            'https://avatars.mds.yandex.net/i?id=7b90f79a9467c7eb23567388f76531114c0d6397-7457232-images-thumbs&n=13',
            'https://static.mk.ru/upload/entities/2019/09/06/19/articles/detailPicture/d6/56/06/79/f537792f75f8e9821f59b7f21319b010.jpg',
            'https://avatars.mds.yandex.net/i?id=f6357aae6bd8b78419b020cb076c9b2052d5a274-8428027-images-thumbs&n=13',
            'https://sun9-69.userapi.com/impf/c840621/v840621533/35170/bNY8G7ft3jI.jpg?size=450x360&quality=96&sign=6520fcbd892868647891fbf7f964a83c&type=album',]
    return render_template('kotolog.html', koti=koti)

@app.route('/<user_nick>/download-game-on-site', methods=['GET', "POST"])
def download_game_on_site(user_nick):
    form = DownloadForm()
    db_sess = db_session.create_session()
    if form.submit():
        if form.game_name.data:
            f = flask.request.files['file']
            print(app.config['UPLOAD_FOLDER'], form.game_name.data)
            print(os.path.abspath("files.txt"))
            f.save(os.path.abspath(f"{form.game_name.data}.txt"))
            if form.game_name.data and form.genre.data and form.picture_url.data and form.cost.data and form.version.data:
                if form.multiplayer.data == 'Да':
                    print(321)
                    multiplayer = True
                else:
                    multiplayer = False
                newgame = Games(
                        game_name=form.game_name.data,
                        company=user_nick,
                        genre=form.genre.data,
                        size_GB=form.size_GB.data,
                        version=form.version.data,
                        created_date=datetime.datetime.now(),
                        cost=form.cost.data,
                        multiplayer=multiplayer,
                        description=form.description.data,
                        picture_url=form.picture_url.data
                    )
                db_sess.add(newgame)
                db_sess.commit()
                return redirect('/')
                print(newgame)

    return render_template('download_game.html', form=form)

def main():
    app.run(port=8081, host='127.0.0.1')


if __name__ == '__main__':
    main()
