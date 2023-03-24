import pandas as pd
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
print(data.head())
print(data.columns)

#visulaization by continent
continent = data.iloc[61:,2].values
cases = data.iloc[61:,4].values
dates = data.iloc[61:,3]
plt.plot(dates, cases)