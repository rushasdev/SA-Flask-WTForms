from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
                SubmitField
from wtforms.validators import ValidationError, DataRequired, \
                Email, EqualTo, Length

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY']='LongAndRandomSecretKey'


class CreateUserForm(FlaskForm):
    username = StringField(label=('Username'), validators=[DataRequired(), Length(max=64)])
    email = StringField(label=('Email'), validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(label=('Password'), validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
        label=('Confirm Password'), validators=[DataRequired(message='*Required'),
                                        EqualTo('password', message='Both password fields must be equal!')])

    receive_emails = BooleanField(label=('Receive merketting emails.'))

    submit = SubmitField(label=('Submit'))

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(f"Character {char} is not allowed in username.")


class GreetUserForm(FlaskForm):
    username = StringField(label=('Enter Your Name:'),validators=[DataRequired(), Length(min=5, max=64, message='Name length must be between %(min)d and %(max)dcharacters') ])
    submit = SubmitField(label=('Submit'))


@app.route('/', methods=('GET', 'POST'))
def index():
    form = CreateUserForm()
    if form.validate_on_submit():
        return f"""<h1> Welcome {form.username.data} </h1>"""
    return render_template('index.html', form=form)





