#!/usr/bin/env python
# coding: utf-8

# In[175]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np
from scipy import stats
from datetime import date
from sodapy import Socrata
from IPython.display import display, HTML, Markdown, Javascript
pd.options.mode.chained_assignment = None  # default='warn'


# In[176]:


# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cdc.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cdc.gov,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

nc_results = client.get("g653-rqe2", where="key_plot_id IN ('NWSS_nc_1523_Treatment plant_raw wastewater', 'NWSS_nc_303_Treatment plant_raw wastewater', 'NWSS_nc_369_Treatment plant_raw wastewater', 'NWSS_nc_332_Treatment plant_raw wastewater', 'NWSS_nc_334_Treatment plant_raw wastewater', 'NWSS_nc_335_Treatment plant_raw wastewater', 'NWSS_nc_84_Treatment plant_raw wastewater', 'NWSS_nc_85_Treatment plant_raw wastewater', 'NWSS_nc_86_Treatment plant_raw wastewater')", limit=8000)

# Convert to pandas DataFrame
nc_ww_data = pd.DataFrame.from_records(nc_results)


# In[177]:


with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(nc_ww_data)
    display(nc_ww_data.dtypes)


# In[178]:


triangle_pops = pd.read_csv('triangle-counties-cdc-ww-metadata.csv')


# In[179]:


pops_df = pd.DataFrame.from_records(populations, columns=['key_plot_id', 'population_served'])
with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(triangle_pops)


# In[180]:


nc_ww_data_enriched = nc_ww_data.merge(triangle_pops, how='left', left_on='key_plot_id', right_on='key_plot_id')


# In[181]:


with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(nc_ww_data_enriched)


# In[182]:


nc_ww_data_enriched = nc_ww_data_enriched.dropna()
nc_ww_data_enriched['pcr_conc_smoothed'] = pd.to_numeric(nc_ww_data_enriched['pcr_conc_smoothed'])
nc_ww_data_enriched = nc_ww_data_enriched[nc_ww_data_enriched['pcr_conc_smoothed'] > 0]
nc_ww_data_enriched['date'] = pd.to_datetime(nc_ww_data_enriched['date'])
nc_ww_data_enriched = nc_ww_data_enriched[(nc_ww_data_enriched['date'] > '2023-01-01')]
with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(nc_ww_data_enriched.dtypes)
    display(nc_ww_data_enriched)


# In[183]:


nc_ww_data_enriched['year'] = nc_ww_data_enriched['date'].dt.isocalendar().year
nc_ww_data_enriched['week'] = nc_ww_data_enriched['date'].dt.isocalendar().week
#nc_ww_data_enriched_filtered = nc_ww_data_enriched[nc_ww_data_enriched['pcr_conc_smoothed'].transform(lambda x : (x<x.quantile(0.99))&(x>(x.quantile(0.01)))).eq(1)]
nc_ww_data_enriched_filtered = nc_ww_data_enriched
nc_ww_data_enriched_filtered['copies'] = nc_ww_data_enriched_filtered['population_served'] * nc_ww_data_enriched_filtered['pcr_conc_smoothed']

with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(nc_ww_data_enriched_filtered.dtypes)
    display(nc_ww_data_enriched_filtered)


# In[184]:


nc_ww_data_agg = nc_ww_data_enriched_filtered.groupby(['year', 'week']).agg({'copies' : 'sum', 'population_served': 'sum'})
nc_ww_data_agg_noindex = nc_ww_data_agg.reset_index()
nc_ww_data_agg_noindex['copies-per-person'] = nc_ww_data_agg_noindex['copies']/nc_ww_data_agg_noindex['population_served']
nc_ww_data_averaged = nc_ww_data_agg_noindex.filter(items=['year','week','copies-per-person'])
with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(nc_ww_data_averaged)


# In[186]:


nc_ww_data_pivot = nc_ww_data_averaged.pivot(index='week', columns='year')

with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(nc_ww_data_pivot)


# In[187]:


ay = nc_ww_data_pivot.plot(figsize=(20,10), rot=0, grid=True, colormap='cool', lw=2, xticks = [0,5,10,15,20,25,30,35,40,45,50], style='o-')
ay.legend(['2023'], loc=9, fontsize='x-large')


# In[ ]:




