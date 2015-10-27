from flask import Flask, render_template, request, redirect
import requests
from bokeh.embed import components
import bokeh.plotting as plt

app = Flask(__name__)
# recommended  Flask(__name__.split('.')[0])

@app.route("/")
def main():
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html')

stock = 'GOOG'
api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
raw_data = session.get(api_url)


@app.route('/graph')
def graph():
    plot = plt.figure(tools=TOOLS,
                      title='Data from Quandle WIKI set',
                      x_axis_label='date',
                      x_axis_type='datetime')
    script, div = components(plot)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)
