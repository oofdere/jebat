from flask_wtf import FlaskForm
from flask_wtf.file import FileField, ValidationError
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from models import User

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("remember me")
    submit = SubmitField("login")

class SignupForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password2 = PasswordField("repeat", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("signup")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already in use.")

class UploadForm(FlaskForm):
    file = FileField("file", validators=[DataRequired()])
    caption = StringField("caption", validators=[DataRequired()])
    submit = SubmitField("submit")