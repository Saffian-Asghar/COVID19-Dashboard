import pandas as pd
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

st.title('COVID-19 dashboard')

#visulaization by continent
continent_cases = df.groupby('continent')['total_cases'].max()
fig = plt.figure()
plt.bar(continent_cases.index, continent_cases.values)
plt.title('Total COVID-19 Cases by Continent')
plt.xlabel('Continent')
plt.ylabel('Total Cases')
plt.xticks(rotation=90)
st.pyplot(fig)


country_cases = df.loc[df['location'].isin(['United States', 'India', 'Brazil', 'Russia', 'United Kingdom'])]
country_cases = country_cases.groupby(['location', 'date'])['new_cases'].sum().unstack()
fig2, ax = plt.subplots()
country_cases.plot.line(ax=ax)
ax.set_title('Daily New COVID-19 Cases')
ax.set_xlabel('Date')
ax.set_ylabel('New Cases')
ax.legend(title='Country', loc='upper left', bbox_to_anchor=(1, 1))
ax.get_legend().remove()
st.pyplot(fig2)


continent_cases = df.groupby('continent')['total_cases'].max().reset_index()
fig3 = sns.barplot(x='continent', y='total_cases', data=continent_cases)
fig3.set_title('Total COVID-19 Cases by Continent')
fig3.set(xlabel='Continent', ylabel='Total Cases')
fig3.set_xticklabels(fig3.get_xticklabels(), rotation=45, ha='right')
st.pyplot(fig3.figure)



countries = ['United States', 'India', 'Brazil', 'Russia', 'United Kingdom']
country_cases = df.loc[df['location'].isin(countries)]
country_cases = country_cases.groupby(['location', 'date'])['new_cases_smoothed_per_million'].sum().reset_index()

fig = px.line(country_cases, x='date', y='new_cases_smoothed_per_million', color='location', title='Daily New COVID-19 Cases')
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='New Cases per million',
    legend_title='Country',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
    )
)

st.plotly_chart(fig)

import pandas as pd
import streamlit as st


st.dataframe(df)

st.write('Search by country:')
search_term = st.text_input('Enter a search term:')
filtered_df = df[df['location'].str.contains(search_term)]
st.dataframe(filtered_df)


# Filter data for specific countries
countries = ['United States', 'India', 'Brazil', 'Russia', 'United Kingdom', 'France', 'Austria', 'Australia']
df = df[df['location'].isin(countries)]

# Group data by country and date
df = df.groupby(['location', 'date']).sum().reset_index()

# Create function to plot data for specific country
def plot_country(country):
    # Filter data for specific country
    country_data = df[df['location'] == country]
    # Create figure and axes
    fig, ax = plt.subplots()
    # Plot data
    ax.plot(country_data['date'], country_data['new_cases'])
    # Set axis labels
    ax.set_xlabel('Date')
    ax.set_ylabel('New Cases')
    # Set title
    ax.set_title(f"Daily New COVID-19 Cases in {country}")
    # Show plot
    st.pyplot(fig)

# Set default country
default_country = 'United States'

# Create slider for selecting country
country_slider = st.select_slider(
    "Select a country:",
    options=countries,
    value=default_country
)

# Plot data for selected country
plot_country(country_slider)


# # Filter data for specific countries
# countries = ['United States', 'India', 'Brazil', 'Russia', 'United Kingdom']
# df = df[df['location'].isin(countries)]

# # Group data by country
# df = df.groupby(['location']).max().reset_index()

# # Create function to plot data for specific country
# def plot_country(country):
#     # Filter data for specific country
#     country_data = df[df['location'] == country]
#     # Get total cases, deaths, and recoveries
#     cases = country_data['total_cases'].values[0]
#     deaths = country_data['total_deaths'].values[0]
#     recoveries = country_data['total_recovered'].values[0]
#     # Create figure and axes
#     fig, ax = plt.subplots()
#     # Create stacked bar chart
#     ax.bar(country, cases, label='Total Cases')
#     ax.bar(country, deaths, bottom=cases, label='Total Deaths')
#     ax.bar(country, recoveries, bottom=cases+deaths, label='Total Recoveries')
#     # Set axis labels
#     ax.set_xlabel('Country')
#     ax.set_ylabel('Number of Cases')
#     # Set title
#     ax.set_title(f"COVID-19 Cases, Deaths, and Recoveries in {country}")
#     # Show legend
#     ax.legend()
#     # Show plot
#     st.pyplot(fig)

# # Set default country
# default_country = 'United States'

# # Create slider for selecting country
# country_slider = st.select_slider(
#     "Select a country:",
#     options=countries,
#     value=default_country
# )

# # Plot data for selected country
# plot_country(country_slider)


# Filter data for specific countries
countries = ['United States', 'India', 'Brazil', 'Russia', 'United Kingdom']
df = df[df['location'].isin(countries)]

# Group data by country and date
df = df.groupby(['location', 'date']).sum().reset_index()

# Create function to plot data for all selected countries
def plot_countries():
    # Create figure and axes
    fig, ax = plt.subplots()
    # Plot data for each country
    for country in countries:
        country_data = df[df['location'] == country]
        ax.plot(country_data['date'], country_data['new_cases'], label=country)
    # Set axis labels
    ax.set_xlabel('Date')
    ax.set_ylabel('New Cases')
    # Set title
    ax.set_title("Daily New COVID-19 Cases")
    # Show legend
    ax.legend()
    # Show plot
    st.pyplot(fig)

# Plot data for all selected countries
plot_countries()