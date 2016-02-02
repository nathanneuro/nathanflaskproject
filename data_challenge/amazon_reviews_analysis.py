import pandas as pd
import gzip
from sqlalchemy import create_engine
import timeit

def main():
  destination = '/Volumes/Storage/Lab data/Data Analysis/electronicsreviews.db'
  disk_engine = create_engine('sqlite:///' + destination)

  # First, make new SQL table of just electronics

  # Second, join metadata
  df = pd.read_sql_query('SELECT reviewText, asin, overall FROM electronics LEFT OUTER JOIN metadata on asin')


  # Third, search for terms to do with broken or returned or replaced
  # Terms: broken, returned, replaced, broke, 

  # Count number of term hits per product
  # Add column to metadata table with this number


  # Add column to metadata table with number of total reviews for the product

  
  # Add column with Percent of reviews that had terms

  # Add column for average rating for product


  return


if __name__ == '__main__':
   main()

