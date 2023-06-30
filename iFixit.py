import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop
import altair as alt
from bs4 import BeautifulSoup as bs
import requests

st.sidebar.header("How has the repairability of Laptops, Tablets and Smartphones changed over time?")
st.sidebar.markdown("""Source: iFixit Repairability Scores""")
st.sidebar.markdown("""A small data-driven story by Payam Saeedi""")

tab1, tab2, tab3 = st.tabs(["Smartphones", "Tablets", "Laptops"])

def scrape_iFixit(url):
    r = r=requests.get(url)
    soup = bs(r.content)
    
    Model = soup.find_all(True, {"class":["selected"]})
    model_list = []
    for row in Model:
        model_list.append(row.get_text())
    model_list.remove("Release")
    
    Score = soup.find_all('h3')
    score_list = []
    for row in Score:
        score_list.append(row.get_text())
    
    Brand = soup.find_all("div", {"class":"cell device-name"})
    brand_list = []
    for element in Brand:
        brand_list.append(element.get_text().split()[0])
    
    Year = soup.find_all(True, {"data-format":["year"]})
    year = []
    for row in Year:
        year.append(row['datetime'][0:4])
    
    df = pd.DataFrame(list(zip(model_list, score_list, year, brand_list)), columns = ['Device Name','Score','Year','Brand'])
    return df

#Scraping the dataset
iFixit = scrape_iFixit('https://www.ifixit.com/smartphone-repairability')
iFixit_Tablet = scrape_iFixit('https://www.ifixit.com/tablet-repairability')
iFixit_Laptop = scrape_iFixit('https://www.ifixit.com/laptop-repairability')

#Fixing the problems with the mobile dataset
iFixit['Brand'] = iFixit['Brand'].str.replace('iPhone','Apple')
iFixit['Device Name']=iFixit['Device Name'].str.replace('iPhone','')
for index, row in iFixit.iterrows():
    if row['Brand'] == 'Apple': 
        row['Device Name'] = 'iPhone '+ row['Device Name']

iFixit['Score'] = iFixit['Score'].astype('int8')

#Fixing the problems with the tablet dataset
iFixit_Tablet['Brand'] = iFixit_Tablet['Brand'].str.replace('iPad','Apple')
iFixit_Tablet['Device Name']=iFixit_Tablet['Device Name'].str.replace('iPad','')
for index, row in iFixit_Tablet.iterrows():
    if row['Brand'] == 'Apple': 
        row['Device Name'] = 'iPad '+ row['Device Name']

iFixit_Tablet['Score'] = iFixit_Tablet['Score'].astype('int8')

#Fixing the problems with the laptop dataset

iFixit_Laptop['Brand'] = iFixit_Laptop['Brand'].str.replace('MacBook','Apple')
iFixit_Laptop['Device Name']=iFixit_Laptop['Device Name'].str.replace('MacBook','')
for index, row in iFixit_Laptop.iterrows():
    if row['Brand'] == 'Apple': 
        row['Device Name'] = 'MacBook '+ row['Device Name']

iFixit_Laptop['Score'] = iFixit_Laptop['Score'].astype('int8')

#Workflow begins here
#Smartphone data
with tab1:

    brand_select = st.multiselect("Type the names of the brands you would like to compare, or select from the drop-down menu", pd.unique(iFixit['Brand']))

    iFixit1 = iFixit[iFixit['Brand'].isin(brand_select)]
    data = iFixit1.groupby(['Year','Brand'], as_index = False).Score.agg('mean')
    data['Score'] = data['Score'].round(decimals = 2)

    def get_dataset():
        return data.pivot(index = 'Year', columns = 'Brand', values = 'Score')

    df = get_dataset()

    Lines_Phones = alt.Chart(data).mark_line().encode(
        alt.X('Year:O', axis = alt.Axis(title = 'Year',labels = True, grid = False, labelAngle=0, labelFontSize=14, tickSize=0, labelPadding=10, labelColor = 'gray')),
        alt.Y('Score:Q', axis= alt.Axis(grid = True, labelAngle= 0, labelFontSize = 14, tickSize = 0, labelColor = 'gray')),
        # The highlight will be set on the result of a conditional statement
        color=alt.Color('Brand:N', scale=alt.Scale(), legend = alt.Legend(title = None)),
        tooltip=['Year','Score']

    ).properties(title ="Average Repairability Score of Different Brands through Time", width = 1000, height = 400).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left')

    st.altair_chart(Lines_Phones)

    brand_filter = st.selectbox("Select a brand to display the repairability score for each model", pd.unique(iFixit['Brand']))

    iFixit = iFixit[iFixit['Brand'] == (brand_filter)]
    iFixit = iFixit.sort_values(by = ['Year'], ascending = False)

    #st.bar_chart(iFixit, x ='Device Name', y='Score')

    Bars_Phones = alt.Chart(iFixit).mark_bar().encode(
        alt.X('Device Name:N', sort = None, axis = alt.Axis(title = 'Brand',labels = True, grid = False, labelAngle=-90, labelFontSize=14, tickSize=0, labelPadding=10, labelColor = 'gray')),
        alt.Y('Score:Q', axis= alt.Axis(grid = True, labelAngle= 0, labelFontSize = 14, tickSize = 0, labelColor = 'gray'))

    ).properties(title ="Repairability Scores per Brand", width = 800, height = 400).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left')

    st.altair_chart(Bars_Phones)

#Tablet data:
with tab2:

    brand_select = st.multiselect("Type the names of the brands you would like to compare, or select from the drop-down menu", pd.unique(iFixit_Tablet['Brand']))

    iFixit1_Tablet = iFixit_Tablet[iFixit_Tablet['Brand'].isin(brand_select)]
    data_Tablet = iFixit1_Tablet.groupby(['Year','Brand'], as_index = False).Score.agg('mean')
    data_Tablet['Score'] = data_Tablet['Score'].round(decimals = 2)

    def get_dataset_Tablet():
        return data_Tablet.pivot(index = 'Year', columns = 'Brand', values = 'Score')

    df_Tablet = get_dataset_Tablet()

    Lines_Tablet = alt.Chart(data_Tablet).mark_line().encode(
        alt.X('Year:O', axis = alt.Axis(title = 'Year',labels = True, grid = False, labelAngle=0, labelFontSize=14, tickSize=0, labelPadding=10, labelColor = 'gray')),
        alt.Y('Score:Q', axis= alt.Axis(grid = True, labelAngle= 0, labelFontSize = 14, tickSize = 0, labelColor = 'gray')),
        # The highlight will be set on the result of a conditional statement
        color=alt.Color('Brand:N', scale=alt.Scale(), legend = alt.Legend(title = None)),
        tooltip=['Year','Score']

    ).properties(title ="Average Repairability Score of Different Brands through Time", width = 1000, height = 400).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left')

    st.altair_chart(Lines_Tablet)

    brand_filter = st.selectbox("Select a brand to display the repairability score for each model", pd.unique(iFixit_Tablet['Brand']))

    iFixit_Tablet = iFixit_Tablet[iFixit_Tablet['Brand'] == (brand_filter)]
    iFixit_Tablet = iFixit_Tablet.sort_values(by = ['Year'], ascending = False)

    #st.bar_chart(iFixit, x ='Device Name', y='Score')

    Bars_Tablet = alt.Chart(iFixit_Tablet).mark_bar().encode(
        alt.X('Device Name:N', sort = None, axis = alt.Axis(title = 'Brand',labels = True, grid = False, labelAngle=-90, labelFontSize=14, tickSize=0, labelPadding=10, labelColor = 'gray')),
        alt.Y('Score:Q', axis= alt.Axis(grid = True, labelAngle= 0, labelFontSize = 14, tickSize = 0, labelColor = 'gray'))

    ).properties(title ="Repairability Scores per Brand", width = 800, height = 400).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left')

    st.altair_chart(Bars_Tablet)

#Laptop data:
with tab3:
    
    brand_select = st.multiselect("Type the names of the brands you would like to compare, or select from the drop-down menu", pd.unique(iFixit_Laptop['Brand']))

    iFixit1_Laptop = iFixit_Laptop[iFixit_Laptop['Brand'].isin(brand_select)]
    data_Laptop = iFixit1_Laptop.groupby(['Year','Brand'], as_index = False).Score.agg('mean')
    data_Laptop['Score'] = data_Laptop['Score'].round(decimals = 2)

    def get_dataset_Laptop():
        return data_Laptop.pivot(index = 'Year', columns = 'Brand', values = 'Score')

    df_Laptop = get_dataset_Laptop()

    Lines_Laptop = alt.Chart(data_Laptop).mark_line().encode(
        alt.X('Year:O', axis = alt.Axis(title = 'Year',labels = True, grid = False, labelAngle=0, labelFontSize=14, tickSize=0, labelPadding=10, labelColor = 'gray')),
        alt.Y('Score:Q', axis= alt.Axis(grid = True, labelAngle= 0, labelFontSize = 14, tickSize = 0, labelColor = 'gray')),
        # The highlight will be set on the result of a conditional statement
        color=alt.Color('Brand:N', scale=alt.Scale(), legend = alt.Legend(title = None)),
        tooltip=['Year','Score']

    ).properties(title ="Average Repairability Score of Different Brands through Time", width = 1000, height = 400).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left')

    st.altair_chart(Lines_Laptop)

    brand_filter = st.selectbox("Select a brand to display the repairability score for each model", pd.unique(iFixit_Laptop['Brand']))

    iFixit_Laptop = iFixit_Laptop[iFixit_Laptop['Brand'] == (brand_filter)]
    iFixit_Laptop = iFixit_Laptop.sort_values(by = ['Year'], ascending = False)

    #st.bar_chart(iFixit, x ='Device Name', y='Score')

    Bars_Laptop = alt.Chart(iFixit_Laptop).mark_bar().encode(
        alt.X('Device Name:N', sort = None, axis = alt.Axis(title = 'Brand',labels = True, grid = False, labelAngle=-90, labelFontSize=14, tickSize=0, labelPadding=10, labelColor = 'gray')),
        alt.Y('Score:Q', axis= alt.Axis(grid = True, labelAngle= 0, labelFontSize = 14, tickSize = 0, labelColor = 'gray'))

    ).properties(title ="Repairability Scores per Brand", width = 800, height = 400).configure_view(stroke = 'transparent',strokeWidth=0, strokeOpacity = 0).configure_title(anchor='start', color = 'grey').configure_axisX(titleAlign='left')

    st.altair_chart(Bars_Laptop)