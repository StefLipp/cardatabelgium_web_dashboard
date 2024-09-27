import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

# Add custom CSS to hide the GitHub icon
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)


# Set the title and favicon that appear in the browser's tab bar.
st.set_page_config(
    page_title='Car Ownership & City Data Dashboard',
    page_icon=':oncoming_automobile:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare useful functions

@st.cache_data
def load_data():
    """Load car and city data from CSV files and perform a left join."""
    # Load the data
    cardata_path = Path(__file__).parent / 'data/fct_cardata.csv'
    citydata_path = Path(__file__).parent / 'data/dim_city.csv'

    cardata_df = pd.read_csv(cardata_path)
    citydata_df = pd.read_csv(citydata_path)

    # Perform a LEFT JOIN on city_id
    merged_df = pd.merge(cardata_df, citydata_df, on='city_id', how='left')

    return merged_df

# Load the merged data
data_df = load_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :oncoming_automobile: Car Ownership & City Data Dashboard

Explore data related to households, car ownership, population, and prosperity across different cities in Belgium.
'''

# Add some spacing
''
''

# Filterable inputs for selecting cities, provinces, and cardata_year range
provinces = data_df['province_or_region'].unique()

selected_provinces = st.multiselect(
    'Which provinces or regions would you like to view?',
    provinces,
    default=provinces
)

min_year = int(data_df['cardata_year'].min())
max_year = int(data_df['cardata_year'].max())

# Slider to select the range of cardata_year
year_range = st.slider(
    'Select the year range for car data:',
    min_value=min_year,
    max_value=max_year,
    value=[min_year, max_year]
)

''
''

# Filter the data based on user selection
filtered_data_df = data_df[
    (data_df['province_or_region'].isin(selected_provinces))
    & (data_df['cardata_year'] >= year_range[0])
    & (data_df['cardata_year'] <= year_range[1])
]

# Display filtered data
st.header('City and Household Data Overview', divider='gray')

st.dataframe(filtered_data_df)

''
''

# Show a chart comparing car ownership percentages with population density (pop_per_km2)
st.header('Car Ownership Percentage vs. Population Density')

# Create a scatter plot using Altair
scatter1 = alt.Chart(filtered_data_df).mark_circle(size=60).encode(
    x='pop_per_km2',
    y='household_hascar_perc_of_total',
    color='province_or_region',
    tooltip=['city_name_nl', 'pop_per_km2', 'household_hascar_perc_of_total', 'province_or_region']
).properties(
    title="Car Ownership vs Population Density"
).interactive()

# Display the scatter plot
st.altair_chart(scatter1, use_container_width=True)

''
''

# Extra section: Prosperity Index vs. Car Ownership
st.header('Prosperity Index vs. Car Ownership')

# Create another scatter plot for Prosperity Index vs Car Ownership
scatter2 = alt.Chart(filtered_data_df).mark_circle(size=60).encode(
    x='prosperity_index',
    y='household_hascar_perc_of_total',
    color='province_or_region',
    tooltip=['city_name_nl', 'prosperity_index', 'household_hascar_perc_of_total', 'province_or_region']
).properties(
    title="Prosperity Index vs Car Ownership"
).interactive()

# Display the second scatter plot
st.altair_chart(scatter2, use_container_width=True)

''
''

# New section: Car Ownership vs Household Type
st.header('Car Ownership Percentage by Household Type')

# Group the data by household type and calculate the mean car ownership percentage for each type
household_type_avg = filtered_data_df.groupby('household_type_en')['household_hascar_perc_of_total'].mean().reset_index()

# Plot the bar chart using Streamlit's built-in bar chart
st.bar_chart(
    household_type_avg,
    x='household_type_en',
    y='household_hascar_perc_of_total'
)
