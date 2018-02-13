from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Blog
from .forms import UpdateProfile,BlogForm
from .. import db,photos
import markdown2

@main.route('/')
def index():
    '''
        View root page function that returns the index page and its data
    '''
    poems = Blog.query.all()
    title = 'POETRY HOME | Home of Poetry'

    return render_template('index.html',poems=poems,title=title)

@main.route('/user/<uname>')
def profile(uname):
    user=User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    title = "My Profile"

    return render_template("profile/profile.html",title=title,user=user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blog/new',methods=['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title=form.title.data
        body=form.body.data
        new_blog=Blog(title=title,body=body)
        new_blog.save_blog()
        return redirect(url_for('main.index'))
    title = 'Home of poetry'
    return render_template('new_blog.html',title=title,blog_form=form)
    
@main.route('/about')
def about():
    title = 'Home Of Poetry'
    return render_template('about.html',title=title)