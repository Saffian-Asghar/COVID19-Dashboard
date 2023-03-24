import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
data = pd.read_csv(url)
data = data[~data['continent'].isnull()]
data = data[~data['location'].isnull()]

st.sidebar.subheader("Select countries:")
countries = st.sidebar.multiselect("Countries:", data['location'].unique())

if not countries:
    countries = ['France']


data['date'] = pd.to_datetime(data['date'])

df_cases = data[data['location'].isin(countries)].pivot(index = 'date', columns='location', values='new_cases')
df_deaths = data[data['location'].isin(countries)].pivot(index = 'date', columns='location', values='new_deaths')

chart_type = st.sidebar.selectbox("Chart type:", ('Daily Cases', 'Daily Deaths'))

df = pd.DataFrame()
if chart_type == 'Daily Cases':
    title = "Daily New Cases by Country"
    df = df_cases
else:
    title = "Daily New Deaths by Country"
    df = df_deaths

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df.values)
ax.set_xlabel('Date')
ax.set_ylabel(title)
ax.set_title(title)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45, ha='right')



st.pyplot(fig)
