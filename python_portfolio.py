from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from datetime import date
    from dateutil.relativedelta import relativedelta
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    six_months = date.today() + relativedelta(months=-12)

    start=six_months
    end=datetime.datetime.now()
    df=data.DataReader(name="AMD",data_source="yahoo",start=start,end=end)

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
    p.title.text="Candlestick Chart"
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
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]
    # in this case, the render_template function takes 5 arguments; the page to be rendered, and the 4 variables that call the bokeh plot.
    return render_template("plot.html",script1=script1,div1=div1,cdn_js=cdn_js,cdn_css=cdn_css)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
