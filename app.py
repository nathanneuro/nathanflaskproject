from flask import Flask, render_template, request, redirect, Response
import requests
from bokeh.embed import components
import bokeh.plotting as plt
#from bokeh.plotting import figure

import pygal
import os
import pandas as pd
# from collections import OrderedDict
from flask_wtf import Form
from wtforms import FloatField, validators, FieldList, FormField #, StringField
#import flaskconfig as config
import utils

#set FLASKDEMO_SETTINGS = '/flaskconfig.py'
#app.config.from_envvar('nathanflask')

app = Flask(__name__) # , instance_relative_config=True)
WTF_CSRF_ENABLED = True
SECRET_KEY = 'development_test'
SECRET_KEY = str(os.getenv("SECRET_KEY"))
DEBUG = (os.getenv("DEBUG"), True)
#app.config.from_object('config')
#app.config.from_pyfile('config.py')
#app.secret_key = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED
# recommended  Flask(__name__.split('.')[0])


# Used https://github.com/andrewyue/dailycandles/blob/master/app.py by Andrew Yue
# As a reference for trickier parts like this
def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

class NineForm(Form):
    neg = FloatField(label='Median Wage', default=-1, validators=[validators.InputRequired()])
    half1 = FloatField(label='Observed GDP Growth', default=0.5, validators=[validators.InputRequired()])
    half2 = FloatField(label='Predicted GPD Growth (OPEC)', default=0.5, validators=[validators.InputRequired()])
    half3 = FloatField(label='PISA Digital Literacy', default=0.5, validators=[validators.InputRequired()])
    pos1 = FloatField(label='PISA Digital Math Ability', default=1, validators=[validators.InputRequired()])
    qua2 = FloatField(label='PISA Math scores', default=0.25, validators=[validators.InputRequired()])
    qua3 = FloatField(label='PISA Reading Scores', default=0.25, validators=[validators.InputRequired()])
    qua4 = FloatField(label='PISA Science Scores', default=0.25, validators=[validators.InputRequired()])
    qua5 = FloatField(label='PISA Share of Top Math Performers', default=0.25, validators=[validators.InputRequired()])
      

class TenForm(Form):
    neg = FloatField(label='Median Wage', default=-1, validators=[validators.InputRequired()])
    half1 = FloatField(label='Observed GDP Growth', default=0.5, validators=[validators.InputRequired()])
    half2 = FloatField(label='Predicted GPD Growth (OPEC)', default=0.5, validators=[validators.InputRequired()])
    half3 = FloatField(label='PISA Digital Literacy', default=0.5, validators=[validators.InputRequired()])
    pos1 = FloatField(label='PISA Digital Math Ability', default=1, validators=[validators.InputRequired()])
    qua2 = FloatField(label='PISA Math scores', default=0.25, validators=[validators.InputRequired()])
    qua3 = FloatField(label='PISA Reading Scores', default=0.25, validators=[validators.InputRequired()])
    qua4 = FloatField(label='PISA Science Scores', default=0.25, validators=[validators.InputRequired()])
    qua5 = FloatField(label='PISA Share of Top Math Performers', default=0.25, validators=[validators.InputRequired()])
    pos2 = FloatField(label='City Financial Forecast (Citi Group)', default=1, validators=[validators.InputRequired()])


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/proposal')
def proposal():
    return render_template('proposal.html')

@app.route('/proposal2')
def proposal2():
    return render_template('proposal2.html')

@app.route('/proposal2_graph1')
def proposal2_graph1():
    return render_template('proposal2_graph1.html')

@app.route('/proposal2_graph2')
def proposal2_graph2():
    return render_template('proposal2_graph2.html')


@app.route('/table2')
def show_table2():
    data = pd.read_csv('static/Chasing_Flynn.csv')
    countries = data
    countries = countries.sort_values(['Country.Name'], axis=0, ascending=True, na_position='last')
    countries = countries.set_index(['Country.Name'])

    cities = data
    cities = cities.sort_values(['City.name'], axis=0, ascending=True, na_position='last')
    cities = cities.set_index(['City.name'])
    return render_template('showtable2.html', tables=[countries.to_html(classes='country'), cities.to_html(classes='city')], titles= ['By Country', 'By City'])


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


@app.route('/graph1', methods=['GET', 'POST'])
def graph1():
    global dfworld
    form = NineForm()
    weights = getitem(request.args, 'weights', list([-1,0.5,0.5,0.5,1,0.25,0.25,0.25,0.25]))
    if request.method == 'POST' and form.validate():
        weights = []
        i = 0
        for field in form:
            if i != 0:
                weights.append(field.data)
            i = i + 1
        print(weights, "from form")

    if isinstance(weights, str) == True:
        print("oh no, a string")
        weights = [-1,0.5,0.5,0.5,1,0.25,0.25,0.25,0.25]

    targets = ['income', 'gpd_obs', 'gdp_proj', 'digi_read', 'digi_math', 'pisa_math', 'pisa_read', 'pisa_sci', 'top_mathers']
    factor_names = ['Gallup Median Wage', 'Observed GDP Growth', 'Predicted GPD Growth (OPEC)', 'PISA Digital Literacy', 'PISA Digital Math Ability', 'PISA Math scores', 'PISA Reading Scores', 'PISA Science Scores', 'PISA Share of Top Math Performers']
    print(weights)
    print("length of weights", len(weights))
    #9 total weights for [income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
    #session = requests.Session()
    #session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))

    # Raw data to Pandas dataframe
    df = pd.read_csv('static/Code_Worker_Quest.csv')
    
    df.set_index(['Country.Code'], inplace = True)
    df = df.fillna(0)
    df = df[df.index != '0']
    df = utils.norm_df(df, weights, targets)
    dfworld = df.sort_values('weight_score', axis=0, ascending=False, na_position='last')
    top_countries = pd.DataFrame(df.groupby(df.index).first())
    top_countries = top_countries.sort_values('weight_score', axis=0, ascending=False, na_position='last')
    top_countries = top_countries.iloc[:10, [0, -1]]
    tchtml = top_countries.to_html(classes='country')
    return render_template('graph1.html', form=form, weights=weights, tables=tchtml)

@app.route('/graph1plot/')
def graph1plot():
    global dfworld
    plot = utils.world_plot(dfworld, "title optional")
    return Response(response=plot, content_type='image/svg+xml')

@app.route('/graph2plot/')
def graph2plot():
    global top_cities
    factor_names = ['Gallup Median Wage', 'Observed GDP Growth', 'Predicted GPD Growth (OPEC)', 'PISA Digital Literacy', 'PISA Digital Math Ability', 'PISA Math scores', 'PISA Reading Scores', 'PISA Science Scores', 'PISA Share of Top Math Performers', 'Citi Group Financial Forecast']
    
    plot = utils.line_plot(top_cities, 5, factor_names, "title optional")
    return Response(response=plot, content_type='image/svg+xml')


@app.route('/graph2', methods=['GET', 'POST'])
def graph2():
    global top_cities
    form = TenForm()
    weights = getitem(request.args, 'weights', [-1,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,1])
    print(weights)
    targets = ['gallup.median.income', 'gpd_obs', 'gdp_proj', 'digi_read', 'digi_math', 'pisa_math', 'pisa_read', 'pisa_sci', 'top_mathers', 'citi_score']
    


    
    df2 = pd.read_csv('static/Code_Worker_Quest.csv')

    # Set df index before calling norm_df
    df2 = df2.fillna(0)

    df2 = df2[df2['City.name'] != 0]
    # Call norm_df function from utilities
    dfline = utils.norm_df(df2, weights, targets)
    if request.method == 'POST' and form.validate():
        weights = []
        i = 0
        for field in form:
            if i != 0:
                weights.append(field.data)
            i = i + 1
        dfline = utils.norm_df(df2, weights, targets)
        #print(weights, "from form")

    dfline.set_index(['City.name'], inplace = True)
    dfline = dfline.sort_values('weight_score', axis=0, ascending=False)
    #print(df2[1:5].values)
    #, na_position='last')
    # Create new dataframe of five top cities
    top_cities = df2.iloc[:5,-11:]
    # top_cities = pd.DataFrame(df.iloc[:,[-11, -10,-9,-8,-7,-6,-5,-4,-3,-2,-1]])
    top_cities = top_cities.sort_values('weight_score', axis=0, ascending=False, na_position='last')
    #print(top_cities)



    if isinstance(weights, str) == True:
        print("oh no, a string")
        weights = [-1,0.5,0.5,0.5,1,0.25,0.25,0.25,0.25]
    

    return render_template('graph2.html', form=form, weights=weights, tables=top_cities.to_html(classes='city'))



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
