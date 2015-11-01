from flask import Flask, render_template, request, redirect
import requests
from bokeh.embed import components
import bokeh.plotting as plt
import os
import pandas as pd

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
    data = pd.read_csv('Code_Worker_Quest.csv')
    #[income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
    countries = data.set_index(['Country.Name'])
    cities = data.set_index(['City.name'])
    return render_template('table.html', tables=[countries.to_html(classes='country'), cities.to_html(classes='city')], titles= ['By Country', 'By City'])


@app.route('/graph1')
def graph1():
    args = request.args
    weights = getitem(args, 'weights', '1,1,1,1,1,1,1,1,1')
    #9 total weights for [income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]

    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    # raw_data = session.get(api_url)
    raw = requests.get(api_url)
    if(raw.json().get('error') is True):  # changed from == unicode
        # any returned error message means there's uh, an error
        return render_template('grapherror.html')
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
        return render_template('graph1.html', script=script, div=div, stock=ticker.upper())

@app.route('/graph2')
def graph2():
    args = request.args
    weights = getitem(args, 'weights', '1,1,1,1,1,1,1,1,1,1')
    #10 total weights for [income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers, citi_score]

    if(raw.json().get('error') is True):  # changed from == unicode
        # any returned error message means there's uh, an error
        return render_template('grapherror.html')
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
        return render_template('graph2.html', script=script, div=div, stock=ticker.upper())





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
