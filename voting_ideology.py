# import pandas as pd
# import altair as alt
# # from pandasql import sqldf
# # pysqldf = lambda q: sqldf(q, globals())
# # import ipywidgets as widgets
# # from ipywidgets import interact
# # from IPython.display import display, clear_output
# # import time
# import streamlit as st

# # Affinity = pd.read_csv("data/Affinity.csv", encoding="ISO-8859-1")
# # Affinity.drop(columns=["NVotesAll.x", "NVotesAll.y","Unnamed: 0"], inplace=True)
# # country_ref = pd.read_csv("data/states.csv", encoding="Windows-1252")
# # country_ref.drop(columns=["Unnamed: 0"], inplace=True)
# # subset_Affinity = Affinity[(Affinity['ccode1']==710)|(Affinity['ccode1']==365)|(Affinity['ccode1']==2)]
# # query_cty_name2 = """
# # SELECT A.ccode1, C.Countryname as ccode2, A.year, A.agree, A.IdealPointDistance from subset_Affinity as A LEFT JOIN country_ref as C on A.ccode2 = C.ccode 
# # """
# # subset_Affinity = pysqldf(query_cty_name2)

# # query_cty_name1 = """
# # SELECT C.Countryname as ccode1, A.ccode2, A.year, A.agree, A.IdealPointDistance from subset_Affinity as A LEFT JOIN country_ref as C on A.ccode1 = C.ccode 
# # """
# # Affinity_final = pysqldf(query_cty_name1)

# Affinity_final = pd.read_csv("Affinity_final.csv")
# alt.data_transformers.enable(max_rows=None)

# import streamlit as st
# import altair as alt

# # Define your Altair chart code here
# year_slider = alt.binding_range(min=1971, max=2021, step=1, name='Year:')
# year_select = alt.selection_single(name="SelectorName", fields=['year'], bind=year_slider, init={'year': 1971})

# agreeScore_point = alt.Chart(Affinity_final).mark_point(filled=True, size=90).encode(
#     y = alt.Y("agree:Q", title = 'Voting Similarity',scale=alt.Scale(domain=(0, 1))),
#     x = alt.X("IdealPointDistance:Q", title = 'Ideology Distance', scale=alt.Scale(domain=(0, 5.5))),
#     color = alt.Color("ccode1:N", legend=alt.Legend(title="Country Pair Group"), scale=alt.Scale(range=['#fe7c73', '#6c9497', '#4682b4'])),
#     tooltip=[
#         alt.Tooltip("ccode1:N", title="Country 1"),
#         alt.Tooltip("ccode2:N", title="Country 2"),
#         alt.Tooltip("agree:Q", title="Voting Similarity"),
#         alt.Tooltip("IdealPointDistance:Q", title="Ideology Distance")
#     ]
# ).transform_filter(
#     year_select
# ).properties(width=400, height = 500).add_selection(year_select)

# agreeScore_point.configure_view(
#     stroke='transparent'
# ).configure_axis(
#     labelFontSize=20,
#     titleFontSize=20,
#     grid = False
# ).configure_legend(
#     labelFontSize=18,
#     titleFontSize=18
# )




# Import the necessary libraries
import pandas as pd
import streamlit as st
import altair as alt

# Load the Affinity data and drop unnecessary columns
Affinity = pd.read_csv("data/Affinity.csv", encoding="ISO-8859-1")
Affinity.drop(columns=["NVotesAll.x", "NVotesAll.y","Unnamed: 0"], inplace=True)

# Load the country reference data and drop unnecessary columns
country_ref = pd.read_csv("data/states.csv", encoding="Windows-1252")
country_ref.drop(columns=["Unnamed: 0"], inplace=True)

# Select a subset of the Affinity data based on specific country codes
subset_Affinity = Affinity[(Affinity['ccode1']==710)|(Affinity['ccode1']==365)|(Affinity['ccode1']==2)]

# Define SQL queries to join the subset_Affinity data with country names
query_cty_name2 = """
SELECT A.ccode1, C.Countryname as ccode2, A.year, A.agree, A.IdealPointDistance from subset_Affinity as A LEFT JOIN country_ref as C on A.ccode2 = C.ccode 
"""
query_cty_name1 = """
SELECT C.Countryname as ccode1, A.ccode2, A.year, A.agree, A.IdealPointDistance from subset_Affinity as A LEFT JOIN country_ref as C on A.ccode1 = C.ccode 
"""

# Use PySQL to execute the SQL queries and create a new dataframe for the joined data
subset_Affinity = pysqldf(query_cty_name2)
Affinity_final = pysqldf(query_cty_name1)

# Load the final Affinity data
Affinity_final = pd.read_csv("Affinity_final.csv")

# Enable Altair to handle large data sets
alt.data_transformers.enable(max_rows=None)

# Define the Altair chart code
year_slider = alt.binding_range(min=1971, max=2021, step=1, name='Year:')
year_select = alt.selection_single(name="SelectorName", fields=['year'], bind=year_slider, init={'year': 1971})

agreeScore_point = alt.Chart(Affinity_final).mark_point(filled=True, size=90).encode(
    y = alt.Y("agree:Q", title = 'Voting Similarity',scale=alt.Scale(domain=(0, 1))),
    x = alt.X("IdealPointDistance:Q", title = 'Ideology Distance', scale=alt.Scale(domain=(0, 5.5))),
    color = alt.Color("ccode1:N", legend=alt.Legend(title="Country Pair Group"), scale=alt.Scale(range=['#fe7c73', '#6c9497', '#4682b4'])),
    tooltip=[
        alt.Tooltip("ccode1:N", title="Country 1"),
        alt.Tooltip("ccode2:N", title="Country 2"),
        alt.Tooltip("agree:Q", title="Voting Similarity"),
        alt.Tooltip("IdealPointDistance:Q", title="Ideology Distance")
    ]
).transform_filter(
    year_select
).properties(width=400, height = 500).add_selection(year_select)

# Configure the view, axis, and legend settings for the chart
agreeScore_point.configure_view(
    stroke='transparent'
).configure_axis(
    labelFontSize=20,
    titleFontSize=20,
    grid = False
).configure_legend(
    labelFontSize=18,
    titleFontSize=18
)

# Create the Streamlit app and display the chart
def app():
    st.title("Voting Similarity & Ideology Distance")
    st.write("Each point represents a country pair - China/Russia/USA and another country")
    st.altair_chart(agreeScore_point, use_container_width=True)

# Run the app
if __name__ == "__main__":
    app()

