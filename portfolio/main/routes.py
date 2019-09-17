from flask import render_template, request, Blueprint, send_file
from portfolio.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html", title="Home")


@main.route("/blog/")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("blog.html", posts=posts, title="Blog")


@main.route('/about/')
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

# @main.route('/tetris-score', methods=["GET","POST"])
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


@main.route("/downloads")
def downloads():
        # return send_file(file.filename,attachment_filename=file.filename,
        # as_attachment=True)
    return render_template("downloads.html", title="Downloads")


@main.route("/return_file")
def return_file():
        # return send_file(file.filename,attachment_filename=file.filename,
        # as_attachment=True)
    return send_file('/Users/Honzor/Desktop/PROGRAMMING/Python/projects/python_portfolio/mysite/demo/portfolio/static/pictures/Jan Bertlik - CV.pdf', attachment_filename='Jan Bertlik - CV.pdf')


@main.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")


@main.route("/projects")
def projects():
    return render_template("projects.html", title="Projects")


@main.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from datetime import date
    from dateutil.relativedelta import relativedelta
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    six_months = date.today() + relativedelta(months=-6)

    start = six_months
    end = datetime.datetime.now()

    stock_names = ["AMD", "MSFT"]

    df = data.DataReader(name=stock_names[0], data_source="yahoo", start=start, end=end)

    def increase_decrease(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"

        return value

    df["Status"] = [increase_decrease(c, o) for c, o in zip(df.Close, df.Open)]

    df["Middle"] = (df.Open+df.Close)/2
    df["Height"] = abs(df.Close-df.Open)

    # can repalce responsive=True with: sizing_mode='scale_width'
    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    p.title.text = stock_names[0]
    p.grid.grid_line_alpha = 0.4

    hours_12 = 12*60*60*1000

    # .segment method takes 4 manditory arguments;high of both x & y, and low of both x & y
    p.segment(df.index, df.High, df.index, df.Low, color="black")

    # .rect is the rectangle method. Arguments are: rect(x axis, y axis, width, height)
    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"], fill_color="#00FA9A", line_color="black")

    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
           hours_12, df.Height[df.Status == "Decrease"], fill_color="#FF1493", line_color="black")

    script1, div1 = components(p)
    script2, div2 = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

##############

    df2 = data.DataReader(name=stock_names[1], data_source="yahoo", start=start, end=end)

    df2["Status"] = [increase_decrease(c, o) for c, o in zip(df2.Close, df2.Open)]

    df2["Middle"] = (df2.Open+df2.Close)/2
    df2["Height"] = abs(df2.Close-df2.Open)

    # can repalce responsive=True with: sizing_mode='scale_width'
    p2 = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    p2.title.text = stock_names[1]
    p2.grid.grid_line_alpha = 0.4

    p2.segment(df2.index, df2.High, df2.index, df2.Low, color="black")

    p2.rect(df2.index[df2.Status == "Increase"], df2.Middle[df2.Status == "Increase"],
            hours_12, df2.Height[df2.Status == "Increase"], fill_color="#00FA9A", line_color="black")

    p2.rect(df2.index[df2.Status == "Decrease"], df2.Middle[df2.Status == "Decrease"],
            hours_12, df2.Height[df2.Status == "Decrease"], fill_color="#FF1493", line_color="black")

    script1, div1 = components(p)
    script2, div2 = components(p2)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]

    return render_template("plot.html", script1=script1, div1=div1, script2=script2, div2=div2, cdn_js=cdn_js, cdn_css=cdn_css, title="Stocks")
