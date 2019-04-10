import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from dating import app, db, bcrypt
from dating.forms import RegistrationForm, LoginForm, EditProfileForm, InterestForm
from dating.models import *
from flask_login import login_user, current_user, logout_user, login_required
from dating.queries import *

@app.route("/", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/home")
@login_required
def home():
    users_stack = User.query.all()
    return render_template('home.html', users_stack=users_stack)

@app.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilepics', picture_fn)

    output_size = (568, 528)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                firstname=form.firstname.data, lastname=form.lastname.data, date_of_birth=form.date_of_birth.data,
                city=form.city.data, phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  #checks if user is logged in
        return redirect(url_for('home'))    #redirect to the home page
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  #The result of filter_by() is a query that only includes the objects that have a matching username. complete query by calling first(), returns the user object if it exists,None if it does not.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
#Allows a user to view their account profile only if they are logged in
def account():
    return render_template('account.html', title='Account')

@app.route("/profile/<user>", methods=['GET', 'POST'])
@login_required
#Allows a user to view other user's profile page
def profile(user):
    selected_user=User.query.filter_by(username=user).first()
    user = selected_user.username
    return render_template('profile.html', selected_user=selected_user, user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.profilepic.data:
            picture_file = save_picture(form.profilepic.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.city = form.city.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.city.data = current_user.city
        form.phone.data = current_user.phone
        flash('Your photo has been uploaded! It is now your profile pic', 'success')
    image_file = url_for('static', filename='profilepics/' + current_user.image_file)
    return render_template('profileform.html', title='Edit Profile', form=form, image_file=image_file)

@app.route('/add_interests', methods=['GET', 'POST'])
@login_required
def add_interests():
    #form = InterestForm()
    all_interests = [all_book_genres(), all_movie_genres(),all_music_genres(),all_fav_cuisines(),all_hobbies(),
    all_religions(),all_outdoors()]

    book_genre_id = request.form.get('Preferred book genre')
    movie_genre_id = request.form.get('Preferred movie genre')
    music_genre_id = request.form.get('Preferred music genre')
    fav_cuisine_id = request.form.get('Preferred cuisine type')
    hobby_id = request.form.get('Favorite hobby')
    outdoor_id = request.form.get('Favorite Outdoor activity')
    religion_id = request.form.get('Religious ideology')

    #if form.validate_on_submit():
          #update user interests for the specific user
    interest = Interest(
        user_id=current_user.id,
        book_genre_id=book_genre_id,
        movie_genre_id=movie_genre_id,
        music_genre_id=music_genre_id,
        fav_cuisine_id=fav_cuisine_id,
        hobby_id=hobby_id,
        outdoor_id=outdoor_id,
        religion_id=religion_id
    )

    db.session.add(interest)
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('account'))

    return render_template('interestform.html', title='Add Interests', all_interests=all_interests)
