from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from webfall.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Tên đăng nhập đã tồn tại')


    username = StringField(label='Tên đăng nhập:', validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='Mật khẩu:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Xác nhận mật khẩu:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Tạo tài khoản')


class LoginForm(FlaskForm):
    username = StringField(label='Tên đăng nhập:', validators=[DataRequired()])
    password = PasswordField(label='Mật khẩu:', validators=[DataRequired()])
    submit = SubmitField(label='Đăng nhập')