import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop
import altair as alt

st.sidebar.header("How has repairability of mobile phones changed over time")
st.sidebar.markdown("""Source: iFixit Repairability Scores""")
st.sidebar.markdown("""A small project by Payam Saeedi""")

#st.subheader("")

# read csv from a github repo
iFixit = pd.read_csv("iFixit.csv")
iFixit['Score'] = iFixit['Score'].astype('int8')

brand_select = st.multiselect("Type the names of the brands you would like to compare, or select from the drop-down menu", pd.unique(iFixit['Brand']))

iFixit1 = iFixit[iFixit['Brand'].isin(brand_select)]
data = iFixit1.groupby(['Year','Brand'], as_index = False).Score.agg('mean')
data['Score'] = data['Score'].round(decimals = 2)

def get_dataset():
    return data.pivot(index = 'Year', columns = 'Brand', values = 'Score')

df = get_dataset()

Lines = alt.Chart(data).mark_line().encode(
    alt.X('Year:O', axis = alt.Axis(title = 'Year',labels = True, grid = False, labelAngle=0, labelFontSize=14, tickSize=0, labelPadding=10, labelColor = 'gray')),
    alt.Y('Score:Q', axis= alt.Axis(grid = True, labelAngle= 0, labelFontSize = 14, tickSize = 0, labelColor = 'gray')),
    # The highlight will be set on the result of a conditional statement
    color=alt.Color('Brand:N', scale=alt.Scale(), legend = alt.Legend(title = None)),
    tooltip=['Year','Score']
    
).properties(title ="Average Repairability Score of Different Brands through Time", width = 1000, height = 400).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left')

st.altair_chart(Lines)

brand_filter = st.selectbox("Select a brand to display the repairability score for each model", pd.unique(iFixit['Brand']))

iFixit = iFixit[iFixit['Brand'] == (brand_filter)]
iFixit = iFixit.sort_values(by = ['Year'], ascending = False)
st.bar_chart(iFixit, x ='Mobile Phones', y='Score')