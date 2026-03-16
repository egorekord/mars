from flask import Flask, render_template, redirect, abort, flash, url_for, request
from data import db_session
from forms.user import RegisterForm, LoginForm
from forms.job import JobForm, EditForm
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

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
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    actions = [[job.id, job.job, job.work_size,
                job.collaborators, job.is_finished,
                job.user.name, job.user.surname, job.team_leader] for job in jobs]
    return render_template('index.html', title='Главная', actions=actions)


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
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=current_user.id,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect("/")
    return render_template('job.html', title='Adding a job', form=form)


@app.route('/personal')
@login_required
def personal_page():
    return render_template('personal.html', title='Personal')


@app.route('/delete_job/<int:i>', methods=['GET', 'POST'])
@login_required
def delete_job(i):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == i).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
        flash('Работа успешно удалена', 'success')
    else:
        abort(404)
    return redirect("/")


@app.route('/edit_job/<int:i>', methods=['GET', 'POST'])
@login_required
def edit_job(i):
    form = EditForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == i).first()
    if request.method == 'GET':
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
    if form.validate_on_submit():
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        db_sess.commit()
        flash('Работа успешно изменена', 'success')
        return redirect("/")
    return render_template('edit.html', title='Edit a job', form=form)


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.run()


if __name__ == '__main__':
    main()