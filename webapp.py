from bokeh.models import HoverTool
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Histogram, Bar,Donut, HeatMap, TimeSeries
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.palettes import Spectral11
from bokeh.themes import Theme
from bokeh.io import curdoc
import pandas as pd
import numpy as np
from flask import Flask, render_template

app = Flask(__name__)

bokehtheme = Theme(json={
'attrs' : {
    'Figure' : {
        'background_fill_color': '#2F2F2F',
        'border_fill_color': '#2F2F2F',
        'outline_line_color': '#444444',
    },
    'Grid': {
        'grid_line_dash': [6, 4],
        'grid_line_alpha': .3,
    },
    'Title': {
        'text_color': 'white'
    }
}})

df = pd.read_csv('data/testapp.csv')
df.date = pd.to_datetime(df.date, )

dfbig = pd.read_json('data/messy_with_countries.json')
dfbig.date = pd.to_datetime(dfbig.date)

dffi = pd.read_json('data/dffi.json')

mask = dfbig['teams'].isin(['Other', 'Unaffiliated'])
df2 = dfbig[~mask]
# @app.route("/")
# def index():
#     return render_template('index.html')

#
# @app.route("/dashboard/")
# def graphme():
#     plot = create_histogram(df['Age_at_win'].dropna())
#     q = bydate(dfbig,'Prize_USD','date')
#     plot2 = create_bigbar(q, 'date','Prize_USD','Earnings By Year')
#
#     p = nlargest(dfbig, 'CountryName','Prize_USD',10)
#     plot3 = create_donut(p, 'CountryName','Prize_USD',
#                             'Earnings by Top 10 Countries')
#
#     r = nlargest(df2, 'teams','Prize_USD',5)
#     plot4 = create_bar_chart(r, 'teams','Prize_USD',
#                             'Earnings by Top 5 Teams')
#
#     script, div = components(plot2)
#     script2, div2 = components(plot)
#     script3, div3 = components(plot3)
#     script4, div4 = components(plot4)
#
#     plot = figure()
#     # plot.circle([1,2], [3,4])
#     # script2, div2 = components(plot)
#     return render_template("index.html", the_div=div, the_script=script,
#                             the_div2=div2, the_script2=script2,
#                             the_div3=div3, the_script3=script3,
#                             the_div4=div4, the_script4=script4)

@app.route("/")
def graph1():
    plot = create_histogram2(df['Age_at_win'].dropna())
    q = bydate(dfbig,'Prize_USD','date')
    plot2 = create_bar_chart2(q, 'date','Prize_USD','Earnings By Year')

    p = nlargest(dfbig, 'CountryName','Prize_USD',10)
    plot3 = create_donut2(p, 'CountryName','Prize_USD',
                            'Earnings by Top 10 Countries')

    r = nlargest(df2, 'teams','Prize_USD',5)
    plot4 = create_bar_chart2(r, 'teams','Prize_USD',
                            'Earnings by Top 5 Teams')
    plot5 = create_bar_chart3(dffi,'Feature','Importance',
                            'Feature Importance - Random Forests')

    script, div = components(plot2)
    script2, div2 = components(plot)
    script3, div3 = components(plot3)
    script4, div4 = components(plot4)
    script5, div5 = components(plot5)

    plot = figure()
    # plot.circle([1,2], [3,4])
    # script2, div2 = components(plot)
    return render_template("longpage.html", the_div=div, the_script=script,
                            the_div2=div2, the_script2=script2,
                            the_div3=div3, the_script3=script3,
                            the_div4=div4, the_script4=script4,
                            the_div5=div5, the_script5=script5)



def nlargest(df, col1, col2, n):
    x = df.groupby(df[col1])[col2].apply(lambda i: i.sum())
    tn = x.nlargest(n)
    df2 = pd.DataFrame({'year': tn.index, col2: tn})
    return df2

def bydate(df, col, date):
    x = df.groupby(df.date.dt.year)[col].apply(lambda i: i.sum())
    df2 = pd.DataFrame({'year': x.index, col: x})
    return df2

def create_bar_chart(df,col1, col2, title):
    TOOLS = [HoverTool(tooltips=[(str(col1),'$x'),(str(col2),'@y{1.11}')])]
    plot = Bar(df, col1, values=col2, title=title, tools=TOOLS,
                color=Spectral11[1], ylabel="Total Earnings (in USD)",
                legend=False, plot_width=300, plot_height=300)
    return plot

def create_bar_chart2(df,col1, col2, title):
    TOOLS = [HoverTool(tooltips=[(str(col1),'$x'),(str(col2),'@y{1.11}')])]
    plot = Bar(df, col1, values=col2, title=title, tools=TOOLS,
                color=Spectral11[1], ylabel="Total Earnings (in USD)",
                legend=False, plot_width=400, plot_height=400)
    return plot

def create_bar_chart3(df,col1, col2, title):
    TOOLS = [HoverTool(tooltips=[(str(col1),'$x'),(str(col2),'@y{1.1111}')])]
    plot = Bar(df, col1, values=col2,
               legend=False, title=title, tools=TOOLS,
               color=Spectral11[2], plot_width=400, plot_height=400)
    return plot

def create_bigbar(df,col1, col2, title):
    TOOLS = [HoverTool(tooltips=[(str(col1),'$x'),(str(col2),'@y{1.11}')])]
    plot = Bar(df, label=col1, values=col2, tools=TOOLS,
                color=Spectral11[2], ylabel="Total Earnings (in USD)",
                 legend=False, title=title, sizing_mode='stretch_both')
    return plot

def create_donut(df,col1, col2, title):
    plot = Donut(df, label=col1, values=col2, color=Spectral11,
                 title=title, plot_width=300, plot_height=300)
    return plot

def create_donut2(df,col1, col2, title):
    plot = Donut(df, label=col1, values=col2, color=Spectral11,
                 title=title, plot_width=400, plot_height=400)
    return plot

def create_histogram(data):
    TOOLS = [HoverTool(tooltips=[('Age:','$x{int}'),('total','@y')])]
    plot = Histogram(data, title='Age:', legend='bottom_right',
                    ylabel="Number of Tournaments",
                    tools=TOOLS, plot_width=300, plot_height=300)
    return plot

def create_histogram2(data):
    TOOLS = [HoverTool(tooltips=[('Age:','$x{int}'),('total','@y')])]
    plot = Histogram(data, title='Age:', legend='bottom_right',
                    ylabel="Number of Tournaments",
                    tools=TOOLS, plot_width=400, plot_height=400)
    return plot


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
