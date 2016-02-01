import pandas as pd
import gzip
from sqlalchemy import create_engine

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)


# From the data source website, all at once
def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
    # adding in a break, so I can look at head
    if i > 4:
        break
  return pd.DataFrame.from_dict(df, orient='index')

df = getDF('reviews_Video_Games.json.gz')
df.head()
