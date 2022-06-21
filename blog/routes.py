from flask import render_template, flash, redirect, session, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from blog import app, db
from blog.forms import LoginForm, RegistrationForm, CommentForm, SortPosts
from blog.models import User, Post, Comment, Reviews
from sqlalchemy import desc, asc

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    posts = Post.query.all()
    sort = SortPosts()
    if sort.order.data == 'date_desc':
        posts = Post.query.order_by(desc(Post.timestamp)).all()
    else:
        posts = Post.query.order_by(asc(Post.timestamp)).all()
    return render_template('index.html', title='Home', user=User, posts=posts, sort=sort)


@app.route("/post/<int:post_id>", methods = ['GET', 'POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    data = Comment.query.filter_by(post_id=post_id).all()
    
    Cform = CommentForm()
    post1s = Reviews.query.filter_by(post_id = post_id).with_entities(Reviews.stars).all()
    if len(post1s) > 0: 
        for i in post1s:
            x = [dict(i) for i in post1s]
        values_s =  [d['stars'] for d in x]
        total_rev = sum(values_s)
        n_rev = len(values_s)
        average_post = total_rev/n_rev
    else:
        average_post = 0

    return render_template('post.html',title=post.id,post=post, form=Cform, average_post=average_post, data=data)


@app.route("/comment/<int:post_id>", methods=['POST'])
def comment_form(post_id):
    Cform  = CommentForm()
    if Cform.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(body = Cform.body.data, author_id = current_user.id, post_id = post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment submitted")
    return redirect(url_for('post', post_id=post_id))

@app.route("/stars", methods=['GET', 'POST'])
def receive_stars():
    if request.method == 'POST':
        if current_user.is_authenticated:
            ratings_data = request.get_json()
            rating_value = list(ratings_data.values())
            num_stars = rating_value[0]
            page = rating_value[1]
            rating = Reviews(stars = num_stars, author_id = current_user.id, post_id = page)
            has_posted = Reviews.query.filter_by(post_id = page).with_entities(Reviews.stars).all()
            # test if user has already submitted a rating
            if len(has_posted) == 0:
                db.session.add(rating)
                db.session.commit()
            # if user has already submitted rating
            else:
                flash("You have already submitted a rating")
    return redirect(url_for('post', post_id=page))




@app.route('/about')   
def about():
    return render_template('about.html')


# (Lines 89-90 and 92-95) Login, logout and register directly from Grinberg, 2017. Adapted from and avaialble at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('error_page'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

# Adapted from Grinberg, 2017 at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms/page/6
# Adapted from Cardiff Uni Flask Labs, 2021 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/error_page')
def error_page():
    return render_template('error_page.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')