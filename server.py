
from venv import create
from flask import Flask, request, json, send_from_directory, render_template, redirect, render_template_string, abort, Response, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from utils import users


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SECRET_KEY"] = "SawshaIsCute"


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_uuid():
    return users.user_id()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})


    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exists! please choose another one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")






@app.route("/", methods =["GET", "POST"])
def gfg():
    return render_template("home/home.html")


@app.route('/login', methods =["GET", "POST"])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login/login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard/dashboard.html') 

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('gfg'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()


    if form.validate_on_submit():
        user_id = users.user_id()
        
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            raise ValidationError("This username already exists!")
        else:
        
            new_user = User(username=form.username.data, password=hashed_password, user_id=str(user_id))
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('login'))
        

    return render_template('register/register.html', form=form)

    


if __name__ == '__main__':
    app.run(port=5001, debug=True)