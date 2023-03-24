
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

data = pd.read_csv('/Users/hritikakathuria/Downloads/opensource/dashboardteam1/Characters.csv.xls', sep = ';')
house_counts = data['House'].value_counts()
plt.bar(house_counts.index, house_counts.values)
plt.title('Character Distribution by House')
plt.xlabel('House')
plt.ylabel('Count')
plt.xticks(rotation=90)
st.title('My First Streamlit App lol')
st.pyplot()

st.set_option('deprecation.showPyplotGlobalUse', False)