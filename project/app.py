import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data('https://covid.ourworldindata.org/data/owid-covid-data.csv')

countries = df['location'].unique()

options_cases_deaths = ['Cases', 'Deaths']
selected_option = st.sidebar.selectbox('Select an option', options_cases_deaths)
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime(df['date']).min())
end_date = st.sidebar.date_input("End date", value=pd.to_datetime(df['date']).max())

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

mask = (pd.to_datetime(df['date']) >= start_date) & (pd.to_datetime(df['date']) <= end_date)
df = df.loc[mask]

options = ['Count', 'Cumulative Count', '7-Day Rolling Average']
variable = st.sidebar.selectbox('Select the type of numerical data', options)

if variable != 'Cumulative Count':
    selected_countries = st.sidebar.multiselect('Select one or more countries', countries, default=['France'])
else:
    selected_countries = [st.sidebar.selectbox('Select a country', countries)]
df = df[df['location'].isin(selected_countries)]

df_grouped = df.groupby(['date', 'location']).sum().reset_index()

fig = px.line(df_grouped, x='date', y='new_cases_per_million', color='location', 
              labels={'new_cases_per_million': f"{selected_option.capitalize()} {variable.capitalize()} per million"},
              title=f"{selected_option.capitalize()} {variable.capitalize()} of COVID-19 per million",
              range_x=[start_date, end_date])

if variable == 'Cumulative Count':
    selected_country = selected_countries[0]
    if selected_option == 'Cases':
        fig.update_traces(y=df_grouped['total_cases_per_million'])
        daily_change = 20 * df_grouped.groupby('location')['total_cases_per_million'].diff().fillna(0)
    else:
        fig.update_traces(y=df_grouped['total_deaths_per_million'])
        daily_change = 20 * df_grouped.groupby('location')['total_deaths_per_million'].diff().fillna(0)
        
    daily_change_fig = px.line(df_grouped, x='date', y=daily_change, color='location',
                               labels={'y': f"Daily change in {selected_option.lower()} {variable.lower()} per million"},
                               title=f"Daily change in {selected_option.capitalize()} {variable.capitalize()} of COVID-19 per million",
                               range_x=[start_date, end_date])
    fig.add_trace(go.Scatter(x=df_grouped.loc[df_grouped['location']==selected_country, 'date'], 
                                      y=daily_change, 
                                      mode='lines', 
                                      line=dict(color='grey', width=2),
                                      name=f'{selected_country} - Derivative'))
    # fig.add_trace(daily_change_fig['data'][0], line=go.scatter.Line(color="gray"))

elif variable == '7-Day Rolling Average':
    window_size = 7
    if selected_option == 'Cases':
        rolling_avg = df_grouped['new_cases_per_million'].rolling(window_size).mean()
    else:
        rolling_avg = df_grouped['new_deaths_per_million'].rolling(window_size).mean()
    fig.update_traces(y=rolling_avg)

# Render the plot using Streamlit
st.plotly_chart(fig)
