import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

# Streamlit
st.set_page_config(layout="wide")
st.title("Airbnb Data Analysis")

df = pd.read_csv(r"C:\Users\Administrator\Desktop\Airbnb\airbnb_data.csv")


with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration", "QCI", "Contact"],
        icons=["house-fill", "clipboard-data-fill", "bar-chart-fill", "person-square"],)

if select == "Home":
    pass

if select == "Data Exploration":
    with st.container(border=True):
        sec1_col_icon, sec1_col_title = st.columns([0.05, 0.95])
        selected = option_menu(
            menu_title="Data Exploration",
            options=["Price Analysis", "Availability Analysis", "Location Based", "Geo Visualization", "Top Analysis"],
            icons=["cloud-download", "database-gear", "bar-chart"],
            menu_icon="database-gear",
            default_index=0,
            orientation="horizontal",
        )

        if selected == "Price Analysis":
            st.header("Price Analysis")
            col1, col2 = st.columns(2)
            with col1:
                country = st.selectbox("Select the Country", options=df["country"].unique(), index=None,
                                        placeholder="Click here to Select",
                                        accept_new_options=True)
                df_cou = df[df['country'] == country]
                df_cou.reset_index(drop=True, inplace=True)

                room_type = st.selectbox("Select the Room Type", options=df_cou["room_type"].unique(),
                                         index=None, placeholder="Click here to Select",
                                         accept_new_options=True)

                df_cou_room = df_cou[df_cou['room_type'] == room_type]
                df_cou_room.reset_index(drop=True, inplace=True)

                df_cou_room_barc = df_cou_room.groupby("property_type").agg({"price":"sum", "review_scores":"mean", "number_of_reviews":"sum"})
                df_cou_room_barc.reset_index(inplace=True)

                fig_bar_c = px.bar(df_cou_room_barc, x='property_type', y='price', title='PRICE FOR PROPERTY TYPES',
                                   hover_data=['review_scores', 'number_of_reviews'],
                                   color_discrete_sequence=px.colors.sequential.Rainbow, width=500, height=500)
                st.plotly_chart(fig_bar_c)

            with col2:
                 property_type = st.selectbox("Select the Property Type", options=df["property_type"].unique(),
                                              index=None, placeholder="Click here to Select",
                                              accept_new_options=True)
                 df_cou_pt = df_cou[df_cou['country'] == country]
                 df_cou_pt.reset_index(drop=True, inplace=True)

if select == "QCI":
    pass
if select == "Contact":
    pass