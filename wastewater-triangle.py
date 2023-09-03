#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np
from scipy import stats
from datetime import date
from IPython.display import display, HTML, Markdown, Javascript
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:


wastewater = pd.read_csv('~/bin/Viral Gene Copies Persons.csv', encoding="utf-16", sep='\t', thousands=',', parse_dates=['Date'], infer_datetime_format=True)  


# In[3]:


with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
    display(wastewater)


# In[4]:


wastewater_counties = wastewater.query('County == "Durham" | County == "Orange" | County == "Wake"')

with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
    display(wastewater_counties)
    display(wastewater['County'].unique())


# In[5]:


wastewater_counties['year'] = wastewater_counties['Date'].dt.isocalendar().year
wastewater_counties['week'] = wastewater_counties['Date'].dt.isocalendar().week


# In[6]:


with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(wastewater_counties)


# In[7]:


wastewater_filtered_new = wastewater_counties[wastewater_counties['Viral Gene Copies Per Person'].transform(lambda x : (x<x.quantile(0.97))&(x>(x.quantile(0.005)))).eq(1)]
wastewater_triangle_new = wastewater_filtered_new.groupby(['year', 'week']).agg({'Viral Gene Copies Per Person' : 'mean'})
wastewater_noindex = wastewater_triangle_new.reset_index()

with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(wastewater_triangle_new)
    display(wastewater_noindex)


# In[8]:


wastewater_pivot = wastewater_noindex.pivot(index='week', columns='year')
with pd.option_context('display.max_rows', 30, 'display.max_columns', None):
    display(wastewater_pivot)


# In[9]:


ax = wastewater_pivot.plot(figsize=(20,10), rot=0, grid=True, colormap='cool', lw=2, xticks = [0,5,10,15,20,25,30,35,40,45,50], style='o-')
ax.legend(['2021','2022','2023'], loc=9, fontsize='x-large')


# In[10]:


wastewater_2023 = wastewater_counties[(wastewater_counties['Date'] >= '2023-01-01')]
wastewater_grouped = wastewater_2023.groupby([pd.Grouper(key='Date', freq='7D'), 'Wastewater Treatment Plant']).agg({'Viral Gene Copies Per Person' : 'mean', 'County' : 'first'})
wastewater_filtered = wastewater_grouped[wastewater_grouped['Viral Gene Copies Per Person'].transform(lambda x : (x<x.quantile(0.99))&(x>(x.quantile(0.001)))).eq(1)]
wastewater_county = wastewater_filtered.groupby(['Date', 'County']).agg({'Viral Gene Copies Per Person' : 'mean'})

with pd.option_context('display.max_rows', 60, 'display.max_columns', None):
    display(wastewater_filtered.round(0))
    display(wastewater_county)


# In[11]:


ax = wastewater_county.unstack().plot.bar(figsize=(24,10), rot=70).axhline(y=2000000);


# In[ ]:




