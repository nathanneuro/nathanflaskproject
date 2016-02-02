import pandas as pd
import gzip
from sqlalchemy import create_engine
import timeit


def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)


def DF_to_SQL(path, chunksize, destination, table_name):
  start_time = timeit.default_timer()
  i = 0
  df = {}
  chunk = 1
  for d in parse(path):
    df[i] = d
    i += 1
    # adding in a break, so I can look at head
    if i > chunksize * chunk:
      chunk_to_SQL(df, destination, table_name)
      print("Chunk #", chunk, " saved. Time elapsed: ", int(timeit.default_timer() - start_time), " seconds")
      df = {}
      chunk += 1
  chunk_to_SQL(df, destination, table_name)
  print("Last Chunk #", chunk, "saved. Total time elapsed: ", int(timeit.default_timer() - start_time), " seconds")
  return


def chunk_to_SQL(df, destination, table_name):
  df = pd.DataFrame.from_dict(df, orient='index')
  
  df['reviewTime'] = pd.to_datetime(df['reviewTime']) # Convert to datetime or SQL fails
  # Convert 'helpful' list to str
  df['helpful'] = df['helpful'].apply(str)
  #print(df.head())
  df.to_sql(table_name, disk_engine, if_exists='append', index_label = 'index')
  return


def main():
  destination = '/Volumes/Storage/Lab data/Data Analysis/electronicsreviews.db'
  global disk_engine
  disk_engine = create_engine('sqlite:///' + destination)
  df = DF_to_SQL('/Volumes/Storage/Lab data/Data Analysis/reviews_electronics.json.gz', 100000, destination, 'electronics')
  return


if __name__ == '__main__':
   main()

