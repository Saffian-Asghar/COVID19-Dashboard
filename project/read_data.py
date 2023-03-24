import pandas as pd
import pandas as pd
import streamlit as st
data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
print(data.head())
print(data.columns)