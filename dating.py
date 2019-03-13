<<<<<<< HEAD
<<<<<<< HEAD:app.py
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
=======
from flask import Flask, render_template, url_for
from app.models import User, example_data
>>>>>>> 94bcc77cd2fb9873de0c851c6a86296bd2524d5c:dating.py
=======
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
>>>>>>> y-berhane56-master

app = Flask(__name__)

app.config['SECRET_KEY'] = '7ba88159506e7b84bff4420080f75a92'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    username = db.Column(db.String(20), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post('{self.username}', '{self.age}')"


cards = [
{ 'name': 'Selina Mangaroo', 'age': '20'},
{ 'name': 'Alexandra Baybay', 'age': '21'},
{ 'name': 'Yohannes Berhane', 'age': '21'}
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', cards=cards)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
