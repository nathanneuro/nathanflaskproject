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
from flask_wtf import Form
from wtforms import FloatField, validators #, StringField
import flaskconfig as config

#set FLASKDEMO_SETTINGS = '/../../flaskkey.cfg'
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
#app.config.from_object('flaskdemo.default_settings')
#app.config.from_envvar('FLASKDEMO_SETTINGS')
# recommended  Flask(__name__.split('.')[0])


# Used https://github.com/andrewyue/dailycandles/blob/master/app.py by Andrew Yue
# As a reference for trickier parts like this
def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

class NineForm(Form):
    neg = FloatField(label='Median Wage', default=-1)
    half1 = FloatField(label='Observed GDP Growth', default=0.5)
    half2 = FloatField(label='Predicted GPD Growth (OPEC)', default=0.5)
    half3 = FloatField(label='PISA Digital Literacy', default=0.5)
    pos1 = FloatField(label='PISA Digital Math Ability', default=1)
    qua2 = FloatField(label='PISA Math scores', default=0.25)
    qua3 = FloatField(label='PISA Reading Scores', default=0.25)
    qua4 = FloatField(label='PISA Science Scores', default=0.25)
    qua5 = FloatField(label='PISA Share of Top Math Performers', default=0.25)
      

class TenForm(Form):
    neg = FloatField(label='Median Wage', default=-1)
    half1 = FloatField(label='Observed GDP Growth', default=0.5)
    half2 = FloatField(label='Predicted GPD Growth (OPEC)', default=0.5)
    half3 = FloatField(label='PISA Digital Literacy', default=0.5)
    pos1 = FloatField(label='PISA Digital Math Ability', default=1)
    qua2 = FloatField(label='PISA Math scores', default=0.25)
    qua3 = FloatField(label='PISA Reading Scores', default=0.25)
    qua4 = FloatField(label='PISA Science Scores', default=0.25)
    qua5 = FloatField(label='PISA Share of Top Math Performers', default=0.25)
    pos2 = FloatField(label='City Financial Forecast (Citi Group)', default=1)


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


@app.route('/graph1', methods=('GET', 'POST'))
def graph1():
    form = NineForm()
    args = request.args
    weights = getitem(request.args, 'weights', [-1,0.5,0.5,0.5,1,0.25,0.25,0.25,0.25])
    if isinstance(weights, str) == True:
        print("oh no, a string")
        weights = [-1,0.5,0.5,0.5,1,0.25,0.25,0.25,0.25]
    #if form.validate_on_submit():
    #    return redirect('/graph1')
    #9 total weights for [income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
    #session = requests.Session()
    #session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))

    # Raw data to Pandas dataframe
    df = pd.read_csv('static/Code_Worker_Quest.csv')
    #[income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
    
    df.set_index(['Country.Name'], inplace = True)
    df['country_weight'] = (df['income']*weights[0] + df['gdp_obs']*weights[1] + df['gdp_proj']*weights[2] + df['digi_read']*weights[3] + df['digi_math']*weights[4] + df['pisa_math']*weights[5] + df['pisa_read']*weights[6] + df['pisa_sci']*weights[7] + df['top_mathers']*weights[8])/9
    # df = df[df.index != 0]
    df = df.sort_values('country_weight', axis=0, ascending=False, na_position='last')
    top_countries = pd.DataFrame(df.groupby(df.index).first())
    top_countries = top_countries.sort_values('country_weight', axis=0, ascending=False, na_position='last')
    top_countries = top_countries.iloc[:10, [23]]
    tchtml = top_countries.to_html(classes='country')
    # Making the plot
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    #plot = plt.figure(tools=TOOLS,
                     # title='Optimality of Countries for hiring Code Workers',
                     # x_axis_label='Scores')
    #plot.line(top_countries, 'Country.Name', values = 'weight_score', color='green', legend='A', alpha=0.7)
    #plot.line(df, , color='red', legend='B', alpha=0.7)
    # bar = Bar(top_cities, 'Country.Name', values = 'weight_score')
    #plot.yaxis.axis_label = '% Variation from Mean'
    
    #script, div = components(plot)
    script = 1
    div = 1
    return render_template('graph1.html', script=script, div=div, weights=weights, tables=tchtml)

@app.route('/graph2', methods=('GET', 'POST'))
def graph2():
    form = TenForm()
    if form.validate_on_submit():
        return redirect('/graph2')
    weights = getitem(request.args, 'weights', [-1,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,1])
    print(weights)
    if isinstance(weights, str) == True:
        print("oh no, a string")
        
        #10 total weights for [income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers, citi_score]
    
    #if(raw.json().get('error') is True):  # changed from == unicode
        # any returned error message means there's uh, an error
        #return render_template('grapherror.html')
    #else:
    # Raw data to Pandas dataframe
    df = pd.read_csv('static/Code_Worker_Quest.csv')
    df = df.fillna(0)
    # Create custom column
    df['weight_score'] = (df['income']*weights[0] + df['gdp_obs']*weights[1] + df['gdp_proj']*weights[2] + df['digi_read']*weights[3] + df['digi_math']*weights[4] + df['pisa_math']*weights[5] + df['pisa_read']*weights[6] + df['pisa_sci']*weights[7] + df['top_mathers']*weights[8] + df['citi_score']*weights[9])/10
    df = df.set_index(['City.name'])
    df = df[df.index != 0]
    df = df.sort_values('weight_score', axis=0, ascending=False, na_position='last')
    # Create new dataframe of five top cities
    #top_cities_disp['City.name'] = df.loc['City.name']
    #top_cities_disp['weight_score'] = df.loc['weight_score']
    #top_cities_disp = top_cities_disp[:5,]
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
    
    
    top_cities = pd.DataFrame(df.iloc[:5,[1,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1]])
    top_cities = top_cities.sort_values('weight_score', axis=0, ascending=False, na_position='last')
    bar = Bar(top_cities, 'Country.Name', values = 'weight_score')
    script, div = components(bar)
    return render_template('graph2.html', form=form, script=script, div=div, weights=weights, tables=top_cities.to_html(classes='city'))


@app.route('/stockgraph')
def stockgraph():
    args = request.args
    ticker = getitem(args, 'ticker', 'GOOG')
    api_key = ''
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/{}.json?'. format(ticker)
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
    app.run(host='0.0.0.0',port=port, debug=True)
