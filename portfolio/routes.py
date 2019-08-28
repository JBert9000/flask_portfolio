import os
import secrets
from PIL import Image
from flask import (abort, flash, Markup, redirect, render_template,
                   request, Response, session, url_for)
from portfolio import app, db, bcrypt
from datetime import datetime
import sys
import logging
from portfolio.send_email2 import send_email
from sqlalchemy.sql import func
from portfolio.models import User, Post
from portfolio.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template("home.html", title="Home")


@app.route("/register/",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
        password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data}, your account has been created. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", title="Register", form=form)

@app.route("/login/",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('blog'))
        else:
            flash(f'Login Failed. Please check email and password.', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('blog'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pictures',picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account",methods=["GET","POST"])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Profile updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/'+current_user.image_file)
    return render_template('account.html', title="Profile", image_file=image_file, form=form)


@app.route("/blog/")
def blog():
    posts=Post.query.all()
    return render_template("blog.html",posts=posts, title="Blog")

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Successfully posted!', 'success')
        return redirect(url_for('blog'))
    return render_template("create_post.html",form=form, title="New Post",
                            legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Successfully updated your post!', 'success')
        return redirect(url_for('post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                            form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Successfully deleted your post!', 'success')
    return redirect(url_for('blog'))

@app.route('/about/')
def about():
    return render_template("about.html", title="About")


# class Data(db.Model):
#     __tablename__="data"
#     id=db.Column(db.Integer,primary_key=True)
#     email_=db.Column(db.String(120),unique=True)
#     score_=db.Column(db.Integer)
#
#
#     def __init__(self,email_,score_):
#         self.email_=email_
#         self.score_=score_

# @app.route('/tetris-score', methods=["GET","POST"])
# def tetrisScore():
#     if request.method=='POST':
#         email=request.form["email_name"]
#         # score=request.form["tetris_score"]
#         score=request.get_json()
#
#         print("********************************" + str(score))
#
#         data=Data(email,score)
#         db.session.add(data)
#         db.session.commit()
#
#         send_email(email,score)
#
#         return render_template("tetris-score.html")
#     # return render_template('tetris-score.html',text="Your score has been updated.")

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from datetime import date
    from dateutil.relativedelta import relativedelta
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    six_months = date.today() + relativedelta(months=-6)

    start=six_months
    end=datetime.datetime.now()

    stock_names=["AMD","MSFT"]

    # def tickers(stock_names):
    #     for i in stock_names:
    #         return i


    df=data.DataReader(name=stock_names[0],data_source="yahoo",start=start,end=end)

    def increase_decrease(c,o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"

        return value

    df["Status"]=[increase_decrease(c,o) for c,o in zip(df.Close,df.Open)]

    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Close-df.Open)

    p=figure(x_axis_type='datetime',width=1000,height=300,sizing_mode='scale_width') # can repalce responsive=True with: sizing_mode='scale_width'
    p.title.text=stock_names[0]
    p.grid.grid_line_alpha=0.4

    hours_12=12*60*60*1000

    #.segment method takes 4 manditory arguments;high of both x & y, and low of both x & y
    p.segment(df.index,df.High,df.index,df.Low,color="black")

    #.rect is the rectangle method. Arguments are: rect(x axis, y axis, width, height)
    p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"],
           hours_12,df.Height[df.Status=="Increase"],fill_color="#00FA9A",line_color="black")

    p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
           hours_12,df.Height[df.Status=="Decrease"],fill_color="#FF1493",line_color="black")

    script1,div1=components(p)
    script2,div2=components(p)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]

##############

    df2=data.DataReader(name=stock_names[1],data_source="yahoo",start=start,end=end)

    df2["Status"]=[increase_decrease(c,o) for c,o in zip(df2.Close,df2.Open)]

    df2["Middle"]=(df2.Open+df2.Close)/2
    df2["Height"]=abs(df2.Close-df2.Open)

    p2=figure(x_axis_type='datetime',width=1000,height=300,sizing_mode='scale_width') # can repalce responsive=True with: sizing_mode='scale_width'
    p2.title.text=stock_names[1]
    p2.grid.grid_line_alpha=0.4

    p2.segment(df2.index,df2.High,df2.index,df2.Low,color="black")

    p2.rect(df2.index[df2.Status=="Increase"],df2.Middle[df2.Status=="Increase"],
           hours_12,df2.Height[df2.Status=="Increase"],fill_color="#00FA9A",line_color="black")

    p2.rect(df2.index[df2.Status=="Decrease"],df2.Middle[df2.Status=="Decrease"],
           hours_12,df2.Height[df2.Status=="Decrease"],fill_color="#FF1493",line_color="black")

    script1,div1=components(p)
    script2,div2=components(p2)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]

    return render_template("plot.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_js=cdn_js,cdn_css=cdn_css, title="Stocks")





# db=SQLAlchemy(app)
#
# class Data(db.Model):
#     __tablename__="data"
#     id=db.Column(db.Integer,primary_key=True)
#     email_=db.Column(db.String(120),unique=True)
#     height_=db.Column(db.Integer)
#
#     def __init__(self,email_,height_):
#         self.email_=email_
#         self.height_=height_

# @app.route("/height_collector/")
# def height_collector():
#     return render_template("height_collector.html")

# @app.route("/success", methods=['POST'])
# def success():
#     if request.method=='POST':
#         email=request.form["email_name"]
#         height=request.form["height_name"]
#
#
#         if db.session.query(Data).filter(Data.email_==email).count()==0:
#             data=Data(email,height)
#             db.session.add(data)
#             db.session.commit()
#             average_height=db.session.query(func.avg(Data.height_)).scalar()
#             average_height=round(average_height,1)
#             count=db.session.query(Data.height_).count()
#             send_email(email,height,average_height,count)
#             # try:
#             #     db.session.commit()
#             # except IntegrityError:
#             #     db.session.rollback()
#             return render_template("success.html")
#     return render_template('height_collector.html',text="Looks like this email was already used.")


@app.route("/downloads")
def downloads():
        # return send_file(file.filename,attachment_filename=file.filename,
        # as_attachment=True)
    return render_template("downloads.html", title="Downloads")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")

@app.route("/projects")
def projects():
    return render_template("projects.html", title="Projects")
