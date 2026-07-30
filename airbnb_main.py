import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

# Streamlit
st.set_page_config(layout="wide")
st.title("Airbnb Data Analysis")

# Read Airbnb CSV Data
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
            options=["Price Analysis", "Availability Analysis", "Location Based", "Geospatial Visualization", "Top Analysis"],
            icons=["cloud-download", "database-gear", "bar-chart"],
            menu_icon="database-gear",
            default_index=0,
            orientation="horizontal",
        )

        if selected == "Price Analysis":
            st.header("Price Analysis")

            col1, _ = st.columns(2)
            with col1:
                country = st.selectbox("Select the Country for PA", options=df["country"].unique(), index=None,
                                        placeholder="Click here to Select",)
                df_cou = df[df['country'] == country]
                df_cou.reset_index(drop=True, inplace=True)

            col1, col2 = st.columns(2)
            with col1:
                st.write("")
                room_type = st.selectbox("Select the Room Type for PA", options=df_cou["room_type"].unique(),
                                         index=None, placeholder="Click here to Select",)

                df_cou_room = df_cou[df_cou['room_type'] == room_type]
                df_cou_room.reset_index(drop=True, inplace=True)

                df_cou_room_barc = df_cou_room.groupby("property_type").agg({"price":"sum",
                                                                             "review_scores":"mean",
                                                                             "number_of_reviews":"sum"})
                df_cou_room_barc.reset_index(inplace=True)

                fig_bar_c = px.bar(df_cou_room_barc, x='property_type', y='price', title='PRICE FOR PROPERTY TYPES',
                                   hover_data=['review_scores', 'number_of_reviews'],
                                   color_discrete_sequence=px.colors.sequential.Rainbow, width=500, height=500)
                st.plotly_chart(fig_bar_c)

            with col2:
                st.write("")
                property_type = st.selectbox("Select the Property Type", options=df["property_type"].unique(),
                                          index=None, placeholder="Click here to Select",)
                df_cou_pt = df_cou[df_cou['property_type'] == property_type]
                df_cou_pt.reset_index(drop=True, inplace=True)

                df_cou_pt_pie = df_cou_pt.groupby("host_response_time")[["price", "bedrooms"]].sum()
                df_cou_pt_pie.reset_index(inplace=True)

                fig_piec = px.pie(df_cou_pt_pie, names = "host_response_time", values="price",
                                  hover_data=["bedrooms"], color_discrete_sequence=px.colors.sequential.Rainbow,
                                  title="PRICE FOR PROPERTY TYPES BASED ON HOST RESPONSE TIME",)
                st.plotly_chart(fig_piec)

        if selected == "Availability Analysis":
            st.header("Availability Analysis")
            st.subheader("Filter and drill down based on region/property type")
            col1, _ = st.columns(2)
            with col1:
                country = st.selectbox("Select the Country for AA", options=df["country"].unique(), index=None,
                                        placeholder="Click here to Select",)
                if country is None:
                    st.info("Select a country to begin exploring availability.")
                    st.stop()

                df_cou_aa = df[df['country'] == country]
                df_cou_aa.reset_index(drop=True, inplace=True)

            col1, _ = st.columns(2)
            with col1:
                st.write("")
                property_type_aa = st.selectbox("Select the Property Type for AA", options=df['property_type'].unique(),
                                                index=None, placeholder="Click here to Select",)

                if property_type_aa is None:
                    st.info("Select a property type to continue.")
                    st.stop()

                df_cou_aa_pt = df_cou_aa[df_cou_aa['property_type'] == property_type_aa]
                df_cou_aa_pt.reset_index(drop=True, inplace=True)

                if df_cou_aa_pt.empty:
                    st.warning("No listings match this combination. Try a different property type.")
                    st.stop()

            # col1, col2 = st.columns(2)
            # with col1:
            #     df_sunb_a30 = px.sunburst(df_cou_aa_pt, path=["room_type", "bed_type", "is_location_exact"],
            #                               values="availability_30", width=500, height=500,
            #                               title="AVAILABILITY 30",color_discrete_sequence=px.colors.sequential.Rainbow)
            #     st.plotly_chart(df_sunb_a30)
            #
            # with col2:
            #     st.write("")
            #
            #     df_sunb_a60 = px.sunburst(df_cou_aa_pt, path=["room_type", "bed_type", "is_location_exact"],
            #                               values="availability_60", width=500, height=500,
            #                               title="AVAILABILITY 60", color_discrete_sequence=px.colors.sequential.Rainbow)
            #     st.plotly_chart(df_sunb_a60)
            #
            # col3, col4 = st.columns(2)
            # with col3:
            #     df_sunb_a90 = px.sunburst(df_cou_aa_pt, path=["room_type", "bed_type", "is_location_exact"],
            #                               values="availability_90", width=500, height=500,
            #                               title="AVAILABILITY 90", color_discrete_sequence=px.colors.sequential.Rainbow)
            #     st.plotly_chart(df_sunb_a90)
            # with col4:
            #     df_sunb_a365 = px.sunburst(df_cou_aa_pt, path=["room_type", "bed_type", "is_location_exact"],
            #                               values="availability_365", width=500, height=500,
            #                               title="AVAILABILITY 365", color_discrete_sequence=px.colors.sequential.Rainbow)
            #     st.plotly_chart(df_sunb_a365)

            # --- Sunburst grid: 30/60/90/365 ---
            availability_windows = ["availability_30", "availability_60", "availability_90", "availability_365"]
            cols = st.columns(2)

            for i, window in enumerate(availability_windows):
                with cols[i % 2]:
                    fig = px.sunburst(df_cou_aa_pt, path=["room_type", "bed_type", "is_location_exact"],
                                     values=window, width=500, height=500, title=window.replace("_", " ").upper(),
                                     color_discrete_sequence=px.colors.sequential.Rainbow)
                    st.plotly_chart(fig, use_container_width=True)

            room_type_aa = st.selectbox("Select the Room Type for AA", options=df_cou_aa_pt["room_type"].unique(),
                                     index=None, placeholder="Click here to Select",)
            if room_type_aa is None:
                st.info("Select a room type to see availability by host response time.")
                st.stop()

            df_cou_aa_pt_room = df_cou_aa_pt[df_cou_aa_pt['room_type'] == room_type_aa]
            df_cou_aa_pt_room.reset_index(drop=True, inplace=True)
            df_grouped = df_cou_aa_pt_room.groupby("host_response_time")[["availability_30", "availability_60",
                                                        "availability_90", "availability_365"]].sum()
            df_grouped.reset_index(inplace=True)

            fig_df_caaptr_bar = px.bar(df_grouped, x="host_response_time", y=["availability_30", "availability_60",
                                      "availability_90", "availability_365"], title="TOTAL AVAILABILITY BY HOST RESPONSE TIME",
                                       barmode="group", )
            st.plotly_chart(fig_df_caaptr_bar, use_container_width=True)

            st.subheader("Throughout the year")
            st.subheader("Availability snapshot (30/60/90/365 days)")

            avg_availability = df[["availability_30", "availability_60", "availability_90",
                                   "availability_365"]].mean().reset_index()
            avg_availability.columns = ["window", "avg_days_available"]

            fig1 = px.bar(avg_availability,x="window", y="avg_days_available",
                labels={"avg_days_available": "Avg days available", "window": "Time window"})
            st.plotly_chart(fig1, use_container_width=True)

            st.caption("Lower availability = higher occupancy (listing is booked more often). "
                "This compares near-term vs long-term booking pressure across the filtered listings.")

            st.subheader("Booking demand throughout the year (review activity as proxy)")

            monthly_reviews = pd.read_csv(r"monthly_reviews.csv")

            fig2 = px.line(monthly_reviews, x="month", y="review_count", markers=True,
                labels={"review_count": "Number of reviews", "month": "Month"})
            st.plotly_chart(fig2, use_container_width=True)

            st.caption("Review dates are used as a proxy for booking activity, since the dataset "
                "doesn't include actual booking calendars. Higher review counts in a month "
                "suggest more stays occurred around that time.")

        if selected == "Location Based":
            # st.header("Location Based")
            # selected_market = st.selectbox("Choose a city", df["market"].unique())
            # city_df = df[df["market"] == selected_market]
            #
            # selected_suburb = st.selectbox("Choose a suburb", city_df["suburb"].unique())
            # suburb_df = city_df[city_df["suburb"] == selected_suburb]
            # print(suburb_df)

            st.header("📌 Location-Based Insights")

            neighbourhood_stats = pd.read_csv(r"neighbourhood_stats.csv")

            st.subheader("Price stats by neighbourhood (via MongoDB aggregation)")
            st.dataframe(neighbourhood_stats, use_container_width=True)

            # Let user drill into one neighbourhood
            selected_neighbourhood = st.selectbox("Explore a specific neighbourhood",
                neighbourhood_stats["neighbourhood"].tolist())

            # st.write("Columns in dataset:", df.columns.tolist())
            neighbourhood_data = df[df["host_neighbourhood"] == selected_neighbourhood]
            st.write("Columns in dataset:", neighbourhood_data.columns.tolist())
            col1, col2, col3 = st.columns(3)
            col1.metric("Listings", len(neighbourhood_data))
            col2.metric("Avg Price", f"${neighbourhood_data['price'].mean():.0f}")
            col3.metric("Avg Rating", f"{neighbourhood_data['rating'].mean():.1f}")

            # Map zoomed to that neighbourhood
            fig_lb = px.scatter_mapbox(neighbourhood_data, lat="latitude", lon="longitude", color="price", size="rating",
                hover_name="name", zoom=12, height=450, mapbox_style="open-street-map")
            st.plotly_chart(fig_lb, use_container_width=True)

        if selected == "Geospatial Visualization":
            st.header("Geospatial Visualization")

            # df["review_scores_clean"] = df["review_scores"].replace(0, pd.NA)

            price_range = st.slider("Price range ($)", int(df["price"].min()), int(df["price"].max()),
                (int(df["price"].min()), int(df["price"].max())))

            markets = st.multiselect("City / Market", df["market"].unique().tolist(),
                                      default=None, placeholder="Choose Market")

            room_types = st.multiselect("Room type", df["room_type"].unique().tolist(),
                                        default=None, placeholder="Choose Room Type")

            filtered_df = df[(df["price"].between(*price_range)) & (df["market"].isin(markets)) &
                (df["room_type"].isin(room_types))]

            st.write(f"Showing {len(filtered_df)} listings, Zoom in to check all")

            # map_df = filtered_df.dropna(subset=["review_scores_clean"])  # avoid size errors

            fig = px.scatter_mapbox( filtered_df, lat="latitude", lon="longitude", color="price",
                                     size="review_scores", hover_name="name",
                                     hover_data={"price": True, "review_scores": True, "suburb": True,
                                     "latitude": False, "longitude": False},
                                     color_continuous_scale=px.colors.sequential.Plasma, zoom=1, height=500,
                                     mapbox_style="open-street-map")
            st.plotly_chart(fig, use_container_width=True)

        if selected == "Top Analysis":
            st.header("Top Analysis")

            # df["review_scores_clean"] = df["review_scores"].replace(0, pd.NA)

            # ---- ONE set of filters, in the sidebar, used by every section below ----
            st.subheader("🔍 Filter listings")

            price_range = st.slider("Price range ($)", int(df["price"].min()), int(df["price"].max()),
                (int(df["price"].min()), int(df["price"].max())))

            markets = st.multiselect("City / Market", df["market"].unique().tolist(),
                                            default=None, placeholder="Choose Market")

            room_types = st.multiselect("Room type", df["room_type"].unique().tolist(),
                                                default=None, placeholder="Choose Room Type")

            property_types = st.multiselect("Property type", df["property_type"].unique().tolist(),
                                                    default=None, placeholder="Choose Property Type")

            min_reviews = st.slider("Minimum number of reviews", 0, int(df["number_of_reviews"].max()), 0)

            # Apply all filters in one place
            filtered_df = df[(df["price"].between(*price_range)) &
                            (df["market"].isin(markets)) &
                            (df["room_type"].isin(room_types)) &
                            (df["property_type"].isin(property_types)) &
                            (df["number_of_reviews"] >= min_reviews)]

            # st.title("🏠 Airbnb Data Explorer")
            st.write(f"**{len(filtered_df)}** listings match your filters")

            df["first_review"] = pd.to_datetime(df["first_review"], errors="coerce")

            min_date = df["first_review"].min()
            max_date = df["first_review"].max()

            date_range = st.date_input("First review between", value=(min_date, max_date),
                                                min_value=min_date, max_value=max_date)

            if len(date_range) == 2:
                start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
                df = df[df["first_review"].between(start_date, end_date)]
                # filtered_df = filtered_df[filtered_df["first_review"].between(date_range[0], date_range[1])]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Listings", len(filtered_df))
            col2.metric("Avg Price", f"${filtered_df['price'].mean():.0f}")
            col3.metric("Avg Rating", f"{filtered_df['review_scores'].mean():.0f}/100")
            col4.metric("Markets", filtered_df["market"].nunique())

if select == "QCI":
    pass
if select == "Contact":
    pass