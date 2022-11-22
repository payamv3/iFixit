import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 

st.sidebar.header("How has repairability of mobile phones changed over time")
st.sidebar.markdown("""Source: iFixit Repairability Scores""")
st.sidebar.markdown("""A small project by Payam Saeedi""")

#st.subheader("Text")

# read csv from a github repo
iFixit = pd.read_csv("iFixit.csv")
iFixit['Score'] = iFixit['Score'].astype('int8')

brand_select = st.multiselect("Type the names of the brands you would like to compare, or select from the drop-down menu", pd.unique(iFixit['Brand']))

iFixit1 = iFixit[iFixit['Brand'].isin(brand_select)]
data = iFixit1.groupby(['Year','Brand'], as_index = False).Score.agg('mean')
data['Score'] = data['Score'].astype('float')
data['Year'] = data['Year'].astype('str')

def get_dataset():
    return data.pivot(index = 'Year', columns = 'Brand', values = 'Score')

df = get_dataset()
st.line_chart(df)

brand_filter = st.selectbox("Select a brand to display the repaiability score for each model", pd.unique(iFixit['Brand']))

iFixit = iFixit[iFixit['Brand'] == (brand_filter)]

st.bar_chart(iFixit, x ='Mobile Phones', y='Score')