from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import calendar
import altair as alt

st.title("Maket Segmentation")
st.header("Segmentation Analysis on customer data")

#reading data
dataset_df = pd.read_excel("Dataset.xls")

#replacing negative values in product A column with 0
dataset_df["Product A"] = dataset_df["Product A"].apply(lambda x: x if x > 0 else 0)
#checking if there are any negative values
#st.write((dataset_df["Product A"]<0).any())

#extracting year, month data from date column and geometry from the lat lon columns
dataset_df["year"] = dataset_df["Date"].astype(str).str.extract(r'(\d\d\d\d)')
dataset_df["month"] = dataset_df["Date"].astype(str).str.extract(r'\d{4}-(\d{2})-\d{2}')
dataset_df["month"] = dataset_df["month"].astype(int).apply(lambda x: calendar.month_abbr[x])
dataset_df["geometry"] = dataset_df.apply(lambda row: (row.Latitude, row.Longitude), axis=1)

#showing the cleaned dataframe
if st.checkbox("Show Dataframe"):
    st.write("Dataframe has " + str(dataset_df.shape[0]) +" rows and " + str(dataset_df.shape[1])+ " columns")
    st.write(dataset_df.head())

#Visualisation
st.subheader("Graph of each product sale")

products = ["Product A","Product B","Product C"]
choice = st.selectbox("Choose a product",products)
for i in range(len(products)) :
    if choice == products[i]:
        st.line_chart(dataset_df[products[i]])
        st.text("Maximum sale of " + str(products[i]) + " is " + str(dataset_df[products[i]].max()))
        st.text("Total sales of " + str(products[i]) + " is " + str(dataset_df[products[i]].sum()))
        
st.write("Product B has highest number of sales followed by Product A and Product C respectively") 

st.subheader("Monthly sales of each product")
choice2 = st.selectbox("choose a product", products)
for i in range(len(products)):
    if choice2 == products[i]:
        product_per_month = alt.Chart(dataset_df).mark_bar().encode(x=products[i], y="month")
        st.altair_chart(product_per_month)


st.subheader("Total sales of all Products per Month")  
sales_per_month = alt.Chart(dataset_df).mark_bar(color="red").encode(x="month",y="Sales")
st.altair_chart(sales_per_month)
#df = pd.DataFrame(np.random.randn(200, 3),
#columns=['a', 'b', 'c'])
#c = alt.Chart(df).mark_bar().encode(x='a', y='b', tooltip=['a', 'b'])
#.mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])     

#st.altair_chart(c)
       
st.subheader("Map Location of each Customer")
location_df = dataset_df[["Latitude","Longitude"]].rename(columns={'Latitude':'latitude','Longitude':'longitude'})
st.map(location_df, zoom=15)




#product dataframe with sales as index
#product_df = dataset_df[["Product A","Product B","Product C","CustomerName"]]
#product_df = product_df.set_index("CustomerName")

#st.subheader("Product and sales Chart")
#st.write("Visualisation of different products with amount of sales")
#st.write("Choose a product?")
#products = ["Product A", "Product B", "Product C"]
#choice= st.selectbox("products",products)
#if choice == "Product A":
    #st.bar_chart(product_df[["Product A"]])





