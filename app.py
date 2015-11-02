from flask import Flask, render_template, request, redirect
import requests
from bokeh.embed import components
import bokeh.plotting as plt
from bokeh.plotting import figure
from bokeh.palettes import brewer
from bokeh.charts import Bar, output_file
import os
import pandas as pd
import numpy as np
from collections import OrderedDict
import plotly.plotly as py
from plotly.graph_objs import Area

app = Flask(__name__)
# recommended  Flask(__name__.split('.')[0])


# Used https://github.com/andrewyue/dailycandles/blob/master/app.py by Andrew Yue
# As a reference for trickier parts like this
def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/proposal')
def proposal():
    return render_template('proposal.html')

@app.route('/table')
def show_table():
    data = pd.read_csv('static/Code_Worker_Quest.csv')
    #[income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
    # percent variation from mean
    #countries = data.loc[data['Country.Name'] == True]
    countries = data
    countries = countries.sort_values(['Country.Name'], axis=0, ascending=True, na_position='last')
    countries = countries.set_index(['Country.Name'])

    #cities = data.loc[data['City.name'] == Tr]
    cities = data
    cities = cities.sort_values(['City.name'], axis=0, ascending=True, na_position='last')
    cities = cities.set_index(['City.name'])
    return render_template('showtable.html', tables=[countries.to_html(classes='country'), cities.to_html(classes='city')], titles= ['By Country', 'By City'])


@app.route('/graph1')
def graph1():
    args = request.args
    weights = getitem(args, 'weights', [-1,0.5,0.5,0.5,1,0.25,0.25,0.25,0.25])
    #9 total weights for [income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    
    # Raw data to Pandas dataframe
    df = pd.read_csv('static/Code_Worker_Quest.csv')
    #[income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
    #countries = data.loc[data.Country.Name == Tr
    df.set_index(['Country.Name'], inplace = True)
    # Making the plot
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    plot = plt.figure(tools=TOOLS,
                      title='Optimality of Countries for hiring Code Workers',
                      x_axis_label='Scores')
    #plot.line(df, , color='green', legend='A', alpha=0.7)
    #plot.line(df, , color='red', legend='B', alpha=0.7)

    plot.yaxis.axis_label = '% Variation from Mean'
    script, div = components(plot)
    
    return render_template('graph1.html', script=script, div=div, weights=weights)

@app.route('/graph2')
def graph2():
    weights = getitem(request.args, 'weights', [-1,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,1])
    #10 total weights for [income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers, citi_score]
    
    #if(raw.json().get('error') is True):  # changed from == unicode
        # any returned error message means there's uh, an error
        #return render_template('grapherror.html')
    #else:
    # Raw data to Pandas dataframe
    df = pd.read_csv('static/Code_Worker_Quest.csv')
    df = df.fillna(0)
    # Create custom column
    df['weight_score'] = df['income']*weights[0] + df['gdp_obs']*weights[1] + df['gdp_proj']*weights[2] + df['digi_read']*weights[3] + df['digi_math']*weights[4] + df['pisa_math']*weights[5] + df['pisa_read']*weights[6] + df['pisa_sci']*weights[7] + df['top_mathers']*weights[8] + df['citi_score']*weights[9]
    df = df.set_index(['City.name'])
    df = df[df.index != 0]
    df = df.sort_values('weight_score', axis=0, ascending=False, na_position='last')
    # Create new dataframe of five top cities
    top_cities = pd.DataFrame(df.iloc[:5,-10:])
    #top_cities_disp['City.name'] = df.loc['City.name']
    #top_cities_disp['weight_score'] = df.loc['weight_score']
    #top_cities_disp = top_cities_disp[:5,]
    top_cities = top_cities.sort_values('weight_score', axis=0, ascending=False, na_position='last')
    #top_cities_disp = top_cities_disp.sort_values('weight_score', axis=0, ascending=False, na_position='last')

    # Making the plot
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    
    colors = brewer["Spectral"][5]

    def create_area_chart(data, palette):
        _chart_styling = dict(height=800,
                      width=1200,
                      xgrid=False,
                      ygrid=True,
                      tools=TOOLS)
        return Area(data,
            title="Top Five Tech Hire Cities",
            stacked=True,
            palette=colors,
            **_chart_styling)
    
    #a = create_area_chart(top_cities.values, colors)
    cols = top_cities.columns.values.tolist()
    ind = top_cities.index.tolist()
    print(ind)
    #d = {}
    #d = top_cities.to_dict(orient='index')
    print(cols)
    ar = top_cities.values
    print(top_cities.values)
    #p.grid.minor_grid_line_color = '#eeeeee'
    #print(d)
    #print(d[0])
    #p.scatter(top_cities.values, top_cities.values)
    p = figure(plot_width=900, plot_height=600)
    p.line(cols, ar[0], line_width=2)
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Value'
    #bar = Bar(cols, ind[0][0])
    script, div = components(p)
    return render_template('graph2.html', script=script, div=div, weights=weights, tables=top_cities.to_html(classes='city'))





@app.route('/stockgraph')
def stockgraph():
    args = request.args
    ticker = getitem(args, 'ticker', 'GOOG')
    api_key = 'J57eFVXL_QaU2GkUyLkj'
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/{}.json?api_key={}'. format(ticker, api_key)
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    # raw_data = session.get(api_url)
    raw = requests.get(api_url)
    if(raw.json().get('error') is True):  # changed from == unicode
        # any returned error message means there's uh, an error
        return render_template('stockerror.html')
    else:
        # Raw data to Pandas dataframe
        df = pd.DataFrame(raw.json().get('data'), columns=raw.json().get('column_names'))
        df['Date'] = pd.to_datetime(df['Date'])
        # Making the plot
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
        plot = plt.figure(tools=TOOLS,
                          title='Data from Quandle WIKI set',
                          x_axis_label='date',
                          x_axis_type='datetime')
        plot.line(df.Date, df.Open, color='green', legend='Open', alpha=0.7)
        plot.line(df.Date, df.Close, color='red', legend='Close', alpha=0.7)

        plot.yaxis.axis_label = 'Price'
        script, div = components(plot)
        return render_template('stockgraph.html', script=script, div=div, stock=ticker.upper())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0',port=port, debug=False)
