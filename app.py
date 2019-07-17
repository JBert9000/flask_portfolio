from flask import Flask, render_template, request
import sys
import logging
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

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

    return render_template("plot.html",script1=script1,div1=div1,script2=script2,div2=div2,cdn_js=cdn_js,cdn_css=cdn_css)



app.config['SQLALCHEMY_DATABASE_URI']='postgresql://zeta_g:postgres123@localhost/height_data_collector'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer,primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_

@app.route("/height_collector/")
def height_collector():
    return render_template("height_collector.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]

        data=Data(email,height)
        if db.session.query(Data).filter(Data.email_==email).count==0:
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            # try:
            #     db.session.commit()
            # except IntegrityError:
            #     db.session.rollback()
            return render_template("success.html")
    return render_template('height_collector.html',text="Looks like this email was already used.")

if __name__=="__main__":
    app.run(debug=True)