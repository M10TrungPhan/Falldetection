from webfall import app
from flask import render_template, redirect, url_for, flash, request
from webfall.models import History, User
from webfall.forms import RegisterForm, LoginForm
from webfall import db
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/history')
@login_required
def history_page():
    history = History.query.order_by(desc(History.id)).all()
    index = len(history)
    return render_template('history.html', history=history, index = index)



@app.route('/status')
@login_required
def status_page():
    
    # image = "fall/"+ status.image + '.jpg'
    with open('G:/DHBK/Thesis/Project_thesis/webfall/static/last_fall/time.txt', mode='r') as f:
        time = f.read()
    return render_template('status.html', time=time)
    
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Tài khoản đã được tạo thành công. Bạn đang đăng nhập với tài khoản {user_to_create.username}", category='success')
        return redirect(url_for('history_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f' Đã có lỗi trong lúc tạo tài khoản: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Bạn đã đăng nhập thành công với tài khoản {attempted_user.username}', category='success')
            return redirect(url_for('history_page'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không hợp lệ !', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Bạn đã đăng suất khỏi tài khoản.", category='info')
    return redirect(url_for("home_page"))


@app.route('/view')
def view_page():
    print('Nhan duoc tham so',request.args.get('photo', default = ""))
    photo = request.args.get('photo', default = "")
    return render_template('view.html',photo=photo)






