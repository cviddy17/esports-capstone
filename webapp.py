from bokeh.models import HoverTool
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Histogram, Bar, HeatMap, TimeSeries
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
import pandas as pd
import numpy as np
from flask import Flask, render_template

app = Flask(__name__)

df = pd.read_csv('testapp.csv')

@app.route("/")
def graphme():
    plot = create_histogram(df['Age_at_win'].dropna(),
                            'Age')
    plot2 = create_TS('Prizes')
    script, div = components(plot)
    script2, div2 = components(plot2)

    plot = figure()
    # plot.circle([1,2], [3,4])
    # script2, div2 = components(plot)
    return render_template("chart.html", the_div=div, the_script=script,
                            the_div2=div2, the_script2=script2
                            )

def create_TS(title):
    # source = ColumnDataSource(data)
    plot = figure(x_axis_type='datetime', title=title, plot_height=30)
    plot.line(df['Prize_USD'], df['date'])
    return plot

def create_histogram(data, title):
    TOOLS = [HoverTool(tooltips=[('Age:','@x'),('total','@y')])]
    plot = Histogram(data, title=title, tools=TOOLS)
    return plot


if __name__ == "__main__":
    app.run(debug=True)
