from flask import Flask,render_template
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
import os,sys,utils

curdir=os.path.abspath(os.path.dirname(__file__))
os.chdir(curdir)

app=Flask(__name__,static_folder="./static",template_folder="./templates")
CurrentConfig.GLOBAL_ENV=Environment(loader=FileSystemLoader("./templates"))

@app.route("/")
def index():
    return render_template("index.html",last_update=utils.getAllCovid19Data()["component"][0]["mapLastUpdatedTime"])

@app.route("/relative")
def relative():
    return render_template("relative.html",last_update=utils.getAllCovid19Data()["component"][0]["mapLastUpdatedTime"])

@app.route("/ajax-chart-data")
def ajax_chart_data():
    _,cn_map=utils.chinaCovid19Map(type_=["confirmed","died","crued","asymptomatic"])
    return cn_map.dump_options_with_quotes()

@app.route("/ajax-chart-data-relative")
def ajax_chart_data_relative():
    _,cn_map=utils.chinaCovid19MapRelative(type_=["confirmed","died","crued","asymptomatic"])
    return cn_map.dump_options_with_quotes()

if __name__=="__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)