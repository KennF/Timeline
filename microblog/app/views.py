from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, PostForm
from models import User, ROLE_USER, ROLE_ADMIN, Post
from config import POSTS_PER_PAGE

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('You gave a post!')
        return redirect(url_for('index'))
    # posts = [
    #     {
    #         'author' : { 'nickname' : 'John' },
    #         'body' : 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author' : { 'nickname' : 'Susan' },
    #         'body' : 'The Avergers movie was so cool!'
    #     }
    # ]
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)

    return render_template("index.html", title = "Home", form=form, posts = posts)

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen=datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = "Sign In",
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split("@")[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
        # make self as followed
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next')) or url_for('index')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash("User {0} doesn't exist!" % nickname)
        return redirect(url_for('index'))
    # posts = [
    # {'auther': user, 'body' : 'Test post #1' },
    # {'auther': user, 'body' : 'Test post #2' }
    # ]
    posts = user.followed_posts().all()
    return render_template('user.html', user=user, posts = posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    # if g.user is None or not g.user.is_authenticated():
    #     return redirect(url_for('index'))
    form = EditForm(nickname = g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.email = form.email.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash("You changes have been saved")
        return redirect(url_for('user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname 
        form.email.data = g.user.email
        form.about_me.data = g.user.about_me

    return render_template('edit.html', form = form)

@app.route('/follow/<nickname>')
def follow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User {0} not found'.format(user))
        return redirect(url_for('index')) 
    if user == g.user:
        flash('You cannot follow yourself')
        return redirect(url_for('user', nickname = user.nickname)) 
    u = g.user.follow(user)
    if u == None:
        flash('You cannot follow {0}'.format(nickname))
        return redirect(url_for('user', nickname = user.nickname)) 
    db.session.add(u)
    db.session.commit()
    flash('You are following {0}'.format(nickname))
    redirect(url_for('user', nickname=u.nickname))

@app.route('/unfollow/<nickname>')
def unfollow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User {0} not found'.format(user))
        return redirect(url_for('index')) 
    if user == g.user:
        flash('You cannot unfollow yourself')
        return redirect(url_for('user', nickname = user.nickname)) 
    u = g.user.unfollow(user)
    if u == None:
        flash('You cannot unfollow {0}'.format(nickname))
        return redirect(url_for('user', nickname = user.nickname)) 
    db.session.add(u)
    db.session.commit()
    flash('You are following {0}'.format(nickname))
    redirect(url_for('user', nickname=u.nickname))



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
