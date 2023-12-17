# Import libraries
import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import plotly.express as px
import folium
from streamlit_folium import folium_static


# Page Title
st.title("Welcome to the Airbnb NYC House Searcher Tool")


# PIL.Image
image = Image.open('NYC_Photo.png')
st.image(image, use_column_width=False)


# Table
@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()
st.header('AirBnB Data NYC (2019-09-12)')
st.dataframe(df.head(10))


st.write("---")


# Drop Down Menu
nyc_five_boroughs = df["neighbourhood_group"].unique()
selected_borough= st.selectbox("Borough", nyc_five_boroughs, 0)

nyc_borough_neighbourhood= df[df["neighbourhood_group"]== selected_borough]['neighbourhood'].unique()
selected_neighborhood= st.selectbox("Neighbourhood",nyc_borough_neighbourhood,0)


# Price Selector
st.markdown("""### Select a Price Range """)
values = st.slider("Price range", float(df.price.min()), 1000., (50., 300.))
userprintout= df[(df["neighbourhood_group"]== selected_borough)&
                 (df['neighbourhood']== selected_neighborhood)&
                 (df['price'].between(values[0],values[1]))]
finaluserprintout=len(userprintout)
st.write(f"  Total  {finaluserprintout} housing rental are found in {selected_neighborhood} {selected_borough } with price between &#36;{values[0]} and &#36;{values[1]}")


# Map
if not userprintout.empty:
    m = folium.Map(location=[userprintout["latitude"].iloc[0], userprintout["longitude"].iloc[0]], zoom_start=12)

    for index, row in userprintout.iterrows():
        name, host_name, room_type, neighborhood, lat, lon, price = row["name"], row["host_name"], row["room_type"], row["neighbourhood"], row["latitude"], row["longitude"], row["price"]
        popup_html = f"Name: {name}<br> Neighborhood: {neighborhood}<br> Host Name: {host_name}<br>Room Type: {room_type} <Price: ${price:.2f}"

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Price: ${price:.2f}"
        ).add_to(m)
    folium_static(m)
else:
    st.warning("No available apartments/houses are found with the criteria you have selected. Please adjust the criteria to search again.")

