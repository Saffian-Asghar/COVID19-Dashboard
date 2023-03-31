import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df
df = load_data('https://covid.ourworldindata.org/data/owid-covid-data.csv')

# Define a list of pre-defined countries
countries = ['United States', 'India', 'Brazil', 'Russia', 'United Kingdom', 'France', 'Italy', 'Spain', 'Germany', 'China']

# Create a date range selector
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime(df['date']).min())
end_date = st.sidebar.date_input("End date", value=pd.to_datetime(df['date']).max())

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the data based on the selected date range
mask = (pd.to_datetime(df['date']) >= start_date) & (pd.to_datetime(df['date']) <= end_date)
df = df.loc[mask]

# Create a variable selector
options = ['number', 'cumulative_number', 'rolling_average']
variable = st.sidebar.selectbox('Select a variable to display', options)

# Create a country selector
selected_countries = st.sidebar.multiselect('Select countries to display', countries, default=countries)

# Create an option selector for cases or deaths
options_cases_deaths = ['Cases', 'Deaths']
selected_option = st.sidebar.selectbox('Select an option', options_cases_deaths)

# Filter the data based on the selected countries
df = df[df['location'].isin(selected_countries)]

# Group the data by date and country
df_grouped = df.groupby(['date', 'location']).sum().reset_index()

# Create the plot
fig, ax = plt.subplots()
# Set the number of x-axis ticks
num_ticks = 10

# Plot the data
for country in selected_countries:
    # Filter the data for the current country
    country_data = df_grouped[df_grouped['location'] == country]
    
    # Calculate the selected variable
    if variable == 'cumulative_number':
        if selected_option == 'Cases':
            country_data['value'] = country_data['total_cases_per_million']
        else:
            country_data['value'] = country_data['total_deaths_per_million']
    elif variable == 'rolling_average':
        window_size = 7
        if selected_option == 'Cases':
            country_data['value'] = country_data['new_cases_per_million'].rolling(window_size).mean()
        else:
            country_data['value'] = country_data['new_deaths_per_million'].rolling(window_size).mean()
    else:
        if selected_option == 'Cases':
            country_data['value'] = country_data['new_cases_per_million']
        else:
            country_data['value'] = country_data['new_deaths_per_million']
    
    # Plot the data
    ax.plot(country_data['date'], country_data['value'], label=country)

# Set the plot title and axes labels
ax.set_title(f"{selected_option.capitalize()} {variable.capitalize()} of COVID-19 per million")
ax.set_xlabel('Date')
ax.set_ylabel(f"{selected_option.capitalize()} {variable.capitalize()}")

# Add a legend to the plot
ax.legend()

# Set the x-axis tick labels to show only every nth label
n = len(df['date']) // num_ticks
ax.xaxis.set_major_locator(ticker.IndexLocator(base=n, offset=0))

# Show the plot in Streamlit
st.pyplot(fig)