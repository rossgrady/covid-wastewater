#!/usr/bin/env python
# coding: utf-8

# In[90]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np
from scipy import stats
from datetime import date
from IPython.display import display, HTML, Markdown, Javascript
pd.options.mode.chained_assignment = None  # default='warn'


# In[91]:


wastewater = pd.read_csv('~/bin/Viral Gene Copies Persons.csv', encoding="utf-16", sep='\t', thousands=',', parse_dates=['Date'], infer_datetime_format=True)  


# In[92]:


with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
    display(wastewater)


# In[93]:


wastewater_counties = wastewater.query('County == "Durham" | County == "Orange" | County == "Wake"')

with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
    display(wastewater_counties)
    #display(wastewater['County'].unique())


# In[94]:


wastewater_counties['year'] = wastewater_counties['Date'].dt.isocalendar().year
wastewater_counties['week'] = wastewater_counties['Date'].dt.isocalendar().week
wastewater_counties_filtered = wastewater_counties[wastewater_counties['Viral Gene Copies Per Person'].transform(lambda x : (x<x.quantile(0.95))&(x>(x.quantile(0.05)))).eq(1)]
wastewater_counties_filtered['copies'] = wastewater_counties_filtered['Population Served'] * wastewater_counties_filtered['Viral Gene Copies Per Person']


# In[95]:


with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(wastewater_counties_filtered)


# In[96]:


wastewater_triangle_new = wastewater_counties_filtered.groupby(['year', 'week']).agg({'copies' : 'sum', 'Population Served': 'sum'})
wastewater_noindex = wastewater_triangle_new.reset_index()
wastewater_noindex['copies-per-person'] = wastewater_noindex['copies']/wastewater_noindex['Population Served']
wastewater_averaged = wastewater_noindex.filter(items=['year','week','copies-per-person'])

with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    #display(wastewater_triangle_new)
    #display(wastewater_noindex)
    display(wastewater_averaged)


# In[97]:


wastewater_pivot = wastewater_averaged.pivot(index='week', columns='year')

with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(wastewater_pivot)


# In[98]:


ax = wastewater_pivot.plot(figsize=(20,10), rot=0, grid=True, colormap='cool', lw=2, xticks = [0,5,10,15,20,25,30,35,40,45,50], style='o-')
ax.legend(['2021','2022','2023'], loc=9, fontsize='x-large')


# In[99]:


wastewater_2023 = wastewater_counties_filtered[(wastewater_counties_filtered['Date'] >= '2023-01-01')]
wastewater_grouped = wastewater_2023.groupby([pd.Grouper(key='Date', freq='7D'), 'Wastewater Treatment Plant']).agg({'copies' : 'mean', 'County' : 'first', 'Population Served': 'mean'})
wastewater_county = wastewater_grouped.groupby(['Date', 'County']).agg({'copies' : 'sum', 'Population Served': 'sum'})
wastewater_county['Viral Gene Copies Per Person'] = wastewater_county['copies']/wastewater_county['Population Served']
wastewater_tograph = wastewater_county.filter(items=['Date', 'County', 'Viral Gene Copies Per Person'])

with pd.option_context('display.max_rows', 60, 'display.max_columns', None):
    #display(wastewater_2023)
    #display(wastewater_grouped)
    #display(wastewater_filtered.round(0))
    #display(wastewater_county)
    display(wastewater_tograph)


# In[100]:


ax = wastewater_tograph.unstack().plot.bar(figsize=(24,10), rot=70).axhline(y=2000000);


# In[ ]:




