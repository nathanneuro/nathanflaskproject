# Dataframe processing with Pandas
import pandas as pd
import numpy as np

df = pd.read_csv('../static/Code_Worker_Quest.csv')
#[income, gpd_obs, gdp_proj, digi_read, digi_math, pisa_math, pisa_read, pisa_sci, top_mathers]
# converting to percent variation from mean
df['income'] = (df['gallup.median.income'] / df['gallup.median.income'].mean(axis=0)) * 100
df['gdp_obs'] = (df['Obs.GDP.growth'] / df['Obs.GDP.growth'].mean(axis=0)) * 100
df['gdp_proj'] = (df['Pro.GDP.growth'] / df['Pro.GDP.growth'].mean(axis=0)) * 100
df['digi_read'] = (df['digi.read.score'] / df['digi.read.score'].mean(axis=0)) * 100
df['digi_math'] = (df['digi.math.score'] / df['digi.math.score'].mean(axis=0)) * 100
df['pisa_math'] = (df['Math.pisa2012'] / df['Math.pisa2012'].mean(axis=0)) * 100
df['pisa_read'] = (df['Reading.pisa2012'] / df['Reading.pisa2012'].mean(axis=0)) * 100
df['pisa_sci'] = (df['Science.pisa2012'] / df['Science.pisa2012'].mean(axis=0)) * 100
df['top_mathers'] = (df['Share.Top.Mathers.pisa2012'] / df['Share.Top.Mathers.pisa2012'].mean(axis=0)) * 100
df['citi_score'] = (df['citigroup2025.score'] / df['citigroup2025.score'].mean(axis=0)) * 100


df.to_csv("../static/Code_Worker_Quest.csv")
