import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib as mpl

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
        selected = option_menu(menu_title="Data Exploration",
            options=["Price Analysis", "Availability Analysis", "Location Based", "Geospatial Visualization",
                     "Interact with the visualization"],
            icons=["currency-dollar", "buildings", "map", "geo-alt-fill", "display-fill"],
            menu_icon="file-bar-graph-fill", default_index=0, orientation="horizontal",)

        if selected == "Price Analysis":
            st.header("Price Analysis")
            tab1, tab2 = st.tabs(["Country-drill-down", "Market-level averages"])

            with tab1:
                st.subheader("💰 Price Analysis - Country-drill-down")
                country = st.selectbox("Select the Country for PA", options=df["country"].unique(), index=None,
                                        placeholder="Click here to Select",)
                if country is None:
                    st.info("Select a country to begin.")
                    st.stop()

                df_cou = df[df['country'] == country]
                df_cou.reset_index(drop=True, inplace=True)

                col1, col2 = st.columns(2)
                with col1:
                    # st.write("")
                    room_type = st.selectbox("Select the Room Type for PA", options=df_cou["room_type"].unique(),
                                             index=None, placeholder="Click here to Select",)
                    if room_type is None:
                        st.info("Select a room type.")
                    else:
                        df_cou_rt = df_cou[df_cou['room_type'] == room_type]
                        df_cou_rt.reset_index(drop=True, inplace=True)

                        # df_cou_rt_pbyp = df_cou_rt.groupby("property_type").agg({"price":"sum",
                        #                                                              "review_scores":"mean",
                        #                                                              "number_of_reviews":"sum"})
                        df_cou_rt_pbyp = df_cou_rt.groupby("property_type").agg(avg_price=("price", "mean"),
                                                                      avg_rating=("review_scores", "mean"),
                                                                      listing_count=("property_type", "size"))
                        df_cou_rt_pbyp.reset_index(inplace=True)

                        fig_bar_c = px.bar(df_cou_rt_pbyp, x='property_type', y='avg_price', title='Average Price by Property Type',
                                           hover_data=["avg_rating", "listing_count"],
                                           color_discrete_sequence=px.colors.sequential.Rainbow, width=500, height=500)
                        # hover_data = ['review_scores', 'number_of_reviews'],
                        st.plotly_chart(fig_bar_c)

                with col2:
                    # st.write("")
                    property_type = st.selectbox("Select the Property Type", options=df["property_type"].unique(),
                                              index=None, placeholder="Click here to Select",)

                    if property_type is None:
                        st.info("Select a property type.")
                    else:
                        df_cou_pt = df_cou[df_cou['property_type'] == property_type]
                        df_cou_pt.reset_index(drop=True, inplace=True)

                        # df_cou_pt_pie = df_cou_pt.groupby("host_response_time")[["price", "bedrooms"]].sum()
                        df_cou_pt_pie = df_cou_pt.groupby("host_response_time").agg(avg_price=("price", "mean"),
                                                                  listing_count=("host_response_time", "size"))
                        df_cou_pt_pie.reset_index(inplace=True)

                        # fig_piec = px.pie(df_cou_pt_pie, names = "host_response_time", values="price",
                        #                   hover_data=["bedrooms"], color_discrete_sequence=px.colors.sequential.Rainbow,
                        #                   title="PRICE FOR PROPERTY TYPES BASED ON HOST RESPONSE TIME",)
                        fig_piec = px.pie(df_cou_pt_pie, names="host_response_time", values="listing_count",
                                          hover_data=["avg_price"], color_discrete_sequence=px.colors.sequential.Rainbow,
                                          title="Listing Share by Host Response Time", )
                        st.plotly_chart(fig_piec)
            with tab2:
                st.subheader("💰 Price Analysis - Market-level averages")

                st.subheader("Average price by market (city)")
                price_by_market = (df.groupby("market")["price"].mean().sort_values(ascending=False).reset_index())
                fig1 = px.bar(price_by_market, x="market", y="price")
                st.plotly_chart(fig1, use_container_width=True)

                st.subheader("Price spread by room type")
                fig2 = px.box(df, x="room_type", y="price", points="outliers")
                st.plotly_chart(fig2, use_container_width=True)

                st.subheader("Overall price distribution")
                fig3 = px.histogram(df, x="price", nbins=50)
                st.plotly_chart(fig3, use_container_width=True)

                st.subheader("Price vs review score")
                scatter_df = df.dropna(subset=["review_scores"])
                fig4 = px.scatter(scatter_df, x="review_scores", y="price", color="room_type", hover_data=["name", "suburb"])
                st.plotly_chart(fig4, use_container_width=True)

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
            st.divider()
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
            st.divider()
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


            market_stats = pd.read_csv("market_stats.csv")  # from get_neighbourhood_price_stats-style pipeline
            #
            # st.subheader("Price overview by market")
            # st.dataframe(market_stats.style.background_gradient(subset=["avg_price"], cmap="YlOrRd"),
            #             use_container_width=True)
            # st.divider()
            # st.subheader("listings Vs prices")
            # fig1 = px.scatter(market_stats, x="listing_count", y="avg_price",
            #                  size="listing_count", color="avg_price", text="market", color_continuous_scale="Viridis",
            #                  labels={"listing_count": "Number of Listings", "avg_price": "Avg Price ($)"})
            # fig1.update_traces(textposition="top center")
            # st.plotly_chart(fig1, use_container_width=True)

            st.divider()
            st.subheader("🔎 Hidden gems: high rating, lower price")

            gem_df = df[df["review_scores"].notna()].copy()
            gem_df["value_score"] = gem_df["review_scores"] / gem_df["price"]

            top_gems = (gem_df.sort_values("value_score", ascending=False)
                .head(15)[["name", "market", "suburb", "price", "review_scores", "room_type"]])
            st.dataframe(top_gems, use_container_width=True)

            st.caption("Value score = rating ÷ price. Higher means better rating for the money — "
                "a simple way to surface well-reviewed listings that aren't the most expensive.")

            st.divider()
            st.subheader("Room type mix across markets")

            room_mix = (df.groupby(["market", "room_type"]).size().reset_index(name="count"))
            fig2 = px.bar(room_mix, x="market", y="count", color="room_type",
                barmode="stack", labels={"count": "Number of Listings"})
            st.plotly_chart(fig2, use_container_width=True)

            st.divider()
            st.subheader("Drill into a market's suburbs")

            selected_market = st.selectbox("Choose a market", df["market"].unique())
            market_df = df[df["market"] == selected_market]

            suburb_stats = (market_df.groupby("suburb")
                .agg(avg_price=("price", "mean"), listings=("price", "size")).reset_index()
                .sort_values("avg_price", ascending=False).head(15))

            fig3 = px.bar(suburb_stats, x="suburb", y="avg_price", color="listings", color_continuous_scale="Blues",
                labels={"avg_price": "Avg Price ($)", "listings": "# Listings"})
            st.plotly_chart(fig3, use_container_width=True)

            st.divider()
            st.subheader("Highest-rated listings")

            rated_market_df = market_df[market_df["review_scores"].notna()]
            fig4 = px.scatter_mapbox(rated_market_df, lat="latitude", lon="longitude", color="review_scores",
                size="price", hover_name="name", hover_data=["suburb", "price"], color_continuous_scale="RdYlGn",
                zoom=10, height=450, mapbox_style="open-street-map")
            st.plotly_chart(fig4, use_container_width=True)

        if selected == "Geospatial Visualization":
            st.header("Geospatial Visualization")
            tab1, tab2 = st.tabs(["Filter listings", "Price by country"])

            with tab1:
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

            with tab2:
                st.subheader("🗺️ Price by country")

                country_stats = df.groupby("country").agg(avg_price=("price", "mean"),
                                                          listing_count=("price", "size")).reset_index()
                # fig_choropleth = px.choropleth(country_stats, locations="country", locationmode="country names",
                #                                color="avg_price",)
                fig_choropleth = px.choropleth(country_stats, locations="country",
                                               locationmode="country names",  # matches on the actual country name
                                               color="avg_price", hover_name="country", hover_data=["listing_count"],
                                               color_continuous_scale="Viridis", title="Average price by country")
                st.plotly_chart(fig_choropleth, use_container_width=True)

        if selected == "Interact with the visualization":
            st.header("Interact with the visualization")
            tab1, tab2, tab3, tab4 = st.tabs(["Filter listings", "Explore by region and property type",
                                              "How markets grew over time", "Trace patterns across categories"])
            # df["review_scores_clean"] = df["review_scores"].replace(0, pd.NA)
            with tab1:
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
                filtered_df = df[(df["price"].between(*price_range)) & (df["market"].isin(markets)) &
                                (df["room_type"].isin(room_types)) & (df["property_type"].isin(property_types)) &
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

            with tab2:
                st.subheader("🌍 Explore by region and property type")

                treemap_df = df.groupby(["market", "property_type", "room_type"]).agg(
                    avg_price=("price", "mean"), listing_count=("price", "size")).reset_index()

                fig_treemap = px.treemap(treemap_df, path=["market", "property_type", "room_type"],
                    values="listing_count", color="avg_price", color_continuous_scale="RdYlGn_r",
                    hover_data=["avg_price"], title="Click any block to zoom in — size = listings, color = avg price")
                st.plotly_chart(fig_treemap, use_container_width=True)

            with tab3:
                st.subheader("📈 How markets grew over time")

                df["first_review_year"] = pd.to_datetime(df["first_review"], errors="coerce").dt.year

                yearly_market = (df.dropna(subset=["first_review_year"]).groupby(["first_review_year", "market"])
                    .size().reset_index(name="new_listings"))
                yearly_market["first_review_year"] = yearly_market["first_review_year"].astype(int)

                fig_anim = px.bar(yearly_market.sort_values("first_review_year"), x="market", y="new_listings",
                    animation_frame="first_review_year", range_y=[0, yearly_market["new_listings"].max() + 5],
                    title="New listings gaining their first review, by year")
                st.plotly_chart(fig_anim, use_container_width=True)

            with tab4:
                st.subheader("🔗 Trace patterns across categories")

                df["price_bucket"] = pd.cut(df["price"], bins=[0, 50, 100, 200, 500, df["price"].max()],
                    labels=["<$50", "$50-100", "$100-200", "$200-500", "$500+"])

                parcats_df = df[["market", "property_type", "room_type", "price_bucket"]].dropna()
                # limit to top markets so the chart stays readable
                top_markets = df["market"].value_counts().head(6).index
                parcats_df = parcats_df[parcats_df["market"].isin(top_markets)]

                fig_parcats = px.parallel_categories(parcats_df, dimensions=["market", "property_type", "room_type", "price_bucket"],
                    color_continuous_scale=px.colors.sequential.Inferno)
                st.plotly_chart(fig_parcats, use_container_width=True)




if select == "QCI":
    with st.container(border=True):
        st.header("⚡ Quick Chart Insights (QCI)")

        # --- KPI row ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Listings", f"{len(df):,}")
        col2.metric("Avg Price", f"${df['price'].mean():.0f}")
        col3.metric("Markets Covered", df["market"].nunique())
        col4.metric("Avg Rating", f"{df[df['review_scores'] > 0]['review_scores'].mean():.0f}/100")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top 10 markets by listings")
            top_markets = df["market"].value_counts().head(10).reset_index()
            top_markets.columns = ["market", "count"]
            fig = px.bar(top_markets, x="count", y="market", orientation="h")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Property type breakdown")
            prop_counts = df["property_type"].value_counts().head(8).reset_index()
            prop_counts.columns = ["property_type", "count"]
            fig = px.pie(prop_counts, names="property_type", values="count", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        st.divider()
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Superhost vs price")
            fig = px.box(df, x="host_is_superhost", y="price", points=False)
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.subheader("Accommodates vs price")
            sample = df.sample(min(1000, len(df)))  # sample for speed on scatter
            fig = px.scatter(sample, x="accommodates", y="price", opacity=0.5)
            st.plotly_chart(fig, use_container_width=True)
        st.divider()
        col5, col6 = st.columns(2)

        with col5:
            st.subheader("Host response time")
            resp_counts = df["host_response_time"].value_counts().reset_index()
            resp_counts.columns = ["response_time", "count"]
            fig = px.bar(resp_counts, x="response_time", y="count")
            st.plotly_chart(fig, use_container_width=True)

        with col6:
            st.subheader("Cancellation policy split")
            cancel_counts = df["cancellation_policy"].value_counts().reset_index()
            cancel_counts.columns = ["policy", "count"]
            fig = px.pie(cancel_counts, names="policy", values="count", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        st.divider()
        st.subheader("🏆 Top-rated listings")
        top_rated = (df[df["review_scores"] > 0].sort_values(["review_scores", "number_of_reviews"], ascending=False)
            .head(10)[["name", "market", "review_scores", "number_of_reviews", "price"]])
        st.dataframe(top_rated, use_container_width=True)

if select == "Contact":
    pass