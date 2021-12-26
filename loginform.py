from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(),Length(max=20)])
    password = PasswordField("Password",validators=[InputRequired(),Length(max=40)])
    submit = SubmitField('Login')