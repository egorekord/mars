from flask import Flask, render_template, redirect
from data import db_session
from forms.user import RegisterForm, LoginForm, JobForm
from data.users import User
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)


@app.route('/')
@app.route('/index')
def main_page():
    actions = [
        [1, 'Deployment of residential modules 1 and 2', 'Scott Ridley', '15 hours', '2, 3', False],
        [2, 'Exploration of mineral resources', 'Weir Andy', '15 hours', '4, 3', True],
        [3, 'Development of a management system', 'Sanders Teddy', '25 hours', '5', False]
    ]
    return render_template('index.html', title='Заготовка', actions=actions)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template('job.html', title='Adding a job', form=form)


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.run()


if __name__ == '__main__':
    main()