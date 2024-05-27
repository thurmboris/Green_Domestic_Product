import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import re

# Define the custom CSS
custom_css = """
<style>
.stApp {
    background-color: #333333; /* Black background color */
    color: white;
}

.stMarkdown, .stText, .stWrite {
    color: white; /* Ensure other texts remain white */
}

.stTitle {
    color: white; /* White color for the title */
}

h1 {
    color: #FFD700; /* Titles color */
    text-align: center; /* Center the titles */
}

h2, h3 {
    color: #FFD700; /* Titles color */
    text-align: center; /* Center the titles */
}

h4, h5, h6 {
    color: #FFD700; /* Titles color */
}

/* Target blockquote element and its pseudo-element */
blockquote {
    border-left: 1px solid white; /* Change the color of the blockquote line */
    color: white; /* Ensure text inside blockquote is white */
}

blockquote:before {
    background-color: white; /* Ensure pseudo-element is also white */
}

.stSelectbox > label {
    color: white;
}

.stMultiselect > label {
    color: white;
}

.stRadio > label {
    color: white;
}


.main > div {
            padding-left: 0rem;
            padding-right: 0rem;
        }

</style>
"""

# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Load data
Emissions = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data_final/Emissions.csv')
External_costs = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data_final/ExternalCosts.csv')
GrDP = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data_final/GrDP.csv')
Decoupling_OECD = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data_final/Decoupling_OECD_Indicator.csv')
Decoupling_Intensity_Factor = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data_final/Decoupling_Intensity_Factor.csv')
Decoupling_Relative_Difference = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data_final/Decoupling_Relative_Difference.csv')

#############################
##### GrDP Dashboard  ######
############################

# Title
st.title("Going beyond the GDP with the GrDP")

st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: 0px; padding-top: 5px; color: white'> Factoring health and environmental costs in economic success. </h2>", unsafe_allow_html=True)

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)  # Add big spacing

st.image("https://viewpointvancouver.ca/wp-content/uploads/2012/11/new-yorker-shareholder-value.jpg", caption="Source: New Yorker", use_column_width=True)
#st.image("https://dwighttowers.wordpress.com/wp-content/uploads/2011/05/polyp_cartoon_economic_growth_ecology.jpg?w=450&h=359", caption="Source: Dwighttowers", use_column_width=True)

##########################
##### Abstract ######
#########################

# Introduction paragraph
st.header("Abstract")

st.write("""
At E4S, we propose a shift beyond Gross Domestic Product (GDP) towards a more comprehensive indicator: the Green Domestic Product (GrDP). The idea behind the GrDP is to extend the scope of the GDP by integrating the depletion of natural, social, and human capital. Concretely, the GrDP is defined as the GDP minus the external costs associated with economic activities, including the costs related to the emissions of greenhouse gases (GHG), air pollutants, and heavy metals.
Our research underscores three key findings:

1. In Europe, the gap between GDP and GrDP is narrowing, indicating that the economy is growing while external costs due to pollution are decreasing.

2. Pollution costs persist at significant levels throughout Europe, ranging from approximately 5% of GDP in Switzerland and Nordic countries to over 30% in Eastern European nations.

3. While there are glimpses of decoupling between economic growth and pollution, the pace of decarbonisation remains insufficient to achieve our goal of net zero GHG emissions by 2050.

Our decisions are heavily influenced by what we know and by what we measure. Therefore, flawed measurements can skew our judgment and lead to distorted decisions. With GrDP, which accounts for economic, environmental, and social dimensions, our aim is to empower individuals, particularly policymakers, to make more informed and sustainable choices. This approach transcends the traditional dichotomy between fostering economic growth and protecting the environment, offering a path towards sustainable prosperity and well-being.
""")

##########################
##### Introduction ######
#########################

# Introduction paragraph
st.header("What is the Green Domestic Product?")

st.write("""
The Gross Domestic Product (GDP) is a valuable indicator measuring the monetary value of all goods and services produced in a country within a given time period. However, the GDP is not and never was an indicator of economic performance and social progress. Already in 1934, Simon Kuznets, who invented the Gross National Product (GNP) – GDP’s predecessor, warned that national income statistics do not measure welfare. Indeed, while economic science is interested in properly managing all resources, the GDP does not encompass the indirect impacts of productive activities such as environmental pollution. Thus, the GDP is not a good measure of the value effectively created because it fails to account for the depletion of natural, social, and human capital associated with economic activities.
""")

st.write("""
Today, the climate crisis requires urgent action to decarbonise our society. However, there is often a perceived dichotomy between promoting economic growth and protecting environmental sustainability. But these two objectives need not be conflicting, as stated in 2009 by the Stiglitz-Sen-Fitoussi Commission:
""")

st.markdown("> What we measure affects what we do; and if our measurements are flawed, decisions may be distorted. Choices between promoting GDP and protecting the environment may be false choices, once environmental degradation is appropriately included in our measurement of economic performance. So too, we often draw inferences about what are good policies by looking at what policies have promoted economic growth; but if our metrics of performance are flawed, so too may be the inferences that we draw.")

st.markdown("<div style='text-align: right;'> Stiglitz, Sen, Fitoussi et al., 2009. <a href='https://ec.europa.eu/eurostat/documents/8131721/8131772/Stiglitz-Sen-Fitoussi-Commission-report.pdf'>Report by the Commission on the Measurement of Economic Performance and Social Progress</a>. p7</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Add big spacing

st.markdown("""With E4S, we propose a novel indicator, the Green Domestic Product (GrDP), to remedy some of the shortcomings of GDP. The GrDP is calculated by subtracting the external costs associated with producing goods and services from the standard measurement of GDP. The current scope of the GrDP includes the emissions of greenhouse gases (GHG), air pollutants, and heavy metals. The impacts covered include climate change, health issues, decrease in crops’ yields and biomass production, buildings degradation, and damages to ecosystems due to eutrophication. You can learn more about the GrDP, including a detailed description of the method used, data scources, and assumptions, on the [E4S webpage Green Domestic Product](https://e4s.center/resources/reports/green-domestic-product/). 
""")

st.write("""
This article allows you to interactively explore the pollution and external costs, GrDP, and decoupling between economic growth and environmental pollution in European countries.
""")

# Create a table of contents
toc_items = ["Abstract",
             "What is the Green Domestic Product?",
             "Air pollution is decreasing",
             "External costs remain significant", 
             "The GrDP of European countries", 
             "Can we decouple economic growth and pollution?"]

# Render the table of contents on the side of the page
st.sidebar.header("Table of Contents")
for item in toc_items:
    # Manually specify the anchor link for headers with special characters
    if "?" in item:
        anchor_link = item.lower().replace(' ', '-').replace('.', '').replace('?', '')  # Remove question mark from anchor link
    else:
        anchor_link = item.lower().replace(' ', '-').replace('.', '')
    st.sidebar.markdown(f"- [{item}](#{anchor_link})")

        
#############################################
##### Air pollution is decreasing...  ######
############################################

# Section: External costs
st.header("Air pollution is decreasing")

# Subsection: Greenhouse gases
st.subheader("Greenhouse gas emissions: far from net-zero")

st.markdown("""
GHGs are responsible for climate change, which has a wide range of negative impacts on human society and ecosystems by altering temperature and precipitation patterns. Climate change impacts include, for instance, a decrease in economic and agricultural productivity due to more frequent heatwaves and droughts, the destruction of manufactured capital due to extreme events, and biodiversity loss.

This interactive chart shows the evolution of GHG emissions in European countries, according to various reporting methods: 
- Territorial Emissions: accounts for all emissions from residents and non-residents inside a country. The National Emission Inventory follows the Intergovernmental Panel on Climate Change (IPCC) guidelines and is used as a basis for setting GHGs reduction targets in the context of international agreements such as the Kyoto Protocol and the Paris Agreement.
- Residential Emissions: accounts for all emissions resulting from the activities of a country’s residents, including the ones abroad.
- Transfer Emissions: emissions generated by the production of goods and services that are imported minus the emissions generated by the production of goods and services that are exported, as calculated in the [Global Carbon Atlas](https://globalcarbonatlas.org/emissions/carbon-emissions/). 
- Footprint Emissions: sum of the residential and transfer emissions. These emissions are often called "consumption-based" since emissions are allocated according to where they were consumed, rather than where they were produced with territorial emissions reporting.
""")

# Option to select graph
options = [':blue[Evolution of GHG emissions]', ':blue[Map]', ':blue[Table]']
selected_option = st.radio("Select display option", options)

# Select GHG data 
GHG_data = Emissions.loc[:,['countries', 'Year', 'Territorial GHG emissions [t]', 'Residential GHG emissions [t]', 'Footprint GHG emissions [t]', 'Transfer GHG emissions [t]']]
GHG_data['Transfer GHG emissions [t]'] *= -1
unique_countries = sorted(External_costs['countries'].unique())
GHG_data = GHG_data.loc[GHG_data.countries.isin(unique_countries)]

# Depending on the selected option, display the corresponding content
if selected_option == ':blue[Evolution of GHG emissions]':     # Plot of the evolution of GHG
    # Selection of country
    default_country = 'Switzerland'
    selected_country = st.selectbox("Select a country:", unique_countries, index=unique_countries.index(default_country))
    # Filter data based on selected country
    country_data = GHG_data[GHG_data['countries'] == selected_country]
    # Create traces for different emissions
    traces = [
    go.Scatter(x=country_data['Year'], y=country_data['Territorial GHG emissions [t]'], mode='lines', name='Territorial Emissions',
               line=dict(color='rgb(31, 119, 180)')),  # Blue
    go.Scatter(x=country_data['Year'], y=country_data['Residential GHG emissions [t]'], mode='lines', name='Residential Emissions',
               line=dict(color='rgb(255, 127, 14)')),  # Orange
    go.Scatter(x=country_data['Year'], y=country_data['Footprint GHG emissions [t]'], mode='lines', name='Footprint Emissions',
               line=dict(color='rgb(44, 160, 44)'))  # Green
]
    # Create layout
    layout = go.Layout(
        title=f'GHG emissions of {selected_country}',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Tonnes of CO2eq', rangemode='tozero'),  # Fix minimum y-axis value at zero
        margin=dict(l=40, r=40, t=40, b=30)
    )
    # Plot graph
    st.plotly_chart({'data': traces, 'layout': layout}, use_container_width=True)
elif selected_option == ':blue[Map]':            # Map of European countries
    # Display map functionality
    selected_scenario = st.selectbox("Select Scenario:", GHG_data.columns[2:])
    # Define function to plot map
    def plot_map(column):
        # Visualization options
        if  selected_scenario == 'Transfer GHG emissions [t]':
            color_scale = px.colors.diverging.RdYlGn_r  # Green for negative, red for positive
            range_col = (-GHG_data['Transfer GHG emissions [t]'].max(), GHG_data['Transfer GHG emissions [t]'].max())     # Range to fix the legend independently of years
        else:
            color_scale = px.colors.sequential.Oranges  # Shades of orange for GHG emissions
            range_col = (0, GHG_data[['Territorial GHG emissions [t]', 'Residential GHG emissions [t]', 'Footprint GHG emissions [t]']].max().max()) # Range to fix the legend independently of years

        # Define the min and max values for the color range per year
        GHG_data['min_value'] = GHG_data.groupby('Year')[column].transform('min')
        GHG_data['max_value'] = GHG_data.groupby('Year')[column].transform('max')

        # Create map
        fig = px.choropleth(
            GHG_data,
            locations='countries',
            locationmode='country names',
            color=column,
            hover_name='countries',
            animation_frame='Year',  # Assuming 'Year' is the column name
            title="",
            color_continuous_scale=px.colors.sequential.Oranges,
            scope='europe',
            height=600,
            width=800
        )

        # Adjust the color range for each frame
        for frame in fig.frames:
            year = frame.name
            year_data = GHG_data[GHG_data['Year'] == year]

            # Check if the slice is not empty
            if not year_data.empty:
                min_value = year_data['min_value'].iloc[0]
                max_value = year_data['max_value'].iloc[0]
                frame.data[0].zmin = min_value
                frame.data[0].zmax = max_value
            else:
                # Set default min and max if data is not available for the year
                frame.data[0].zmin = GHG_data[column].min()
                frame.data[0].zmax = GHG_data[column].max()
        
        # Update Layout
        fig.update_coloraxes(colorbar_title=column)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_geos(projection_scale=1)

        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)
        
    plot_map(selected_scenario)
elif selected_option == ':blue[Table]':   # Dataframe with data
    all_countries_option = "All countries"
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + unique_countries, default=all_countries_option)
    if all_countries_option in selected_countries:
        filtered_data = GHG_data.copy()  # Make a copy of the original DataFrame
    else:
        filtered_data = GHG_data[GHG_data['countries'].isin(selected_countries)]
    st.write(filtered_data)


    
# Subsection: Air pollutant
st.subheader("Emissions of air pollutants and heavy metals: some notable progress")

st.markdown("""
Fossil-fuel combustion and industrial and agricultural processes emit various other air pollutants. Once in the atmosphere, these pollutants can be directly inhaled by humans. They can also react with the environment, creating new harmful substances. Finally, they can contaminate water and soils, and then be ingested by ecosystems and in turn by humans. 

Human exposure to air pollutants leads to various respiratory and cardiovascular diseases (e.g., asthma and bronchitis) and excess mortality. Similarly, heavy metals exposure is a cause of health issues such as cancer, diabetes, respiratory and cardiovascular diseases. Lead and mercury can also be responsible for IQ loss. The impacts are not restricted to human health though. Ozone exposure decreases crops’ yields and biomass production in forests. NOx and SO2 damages buildings by degrading stone and metalwork. NOx and NH3 affect ecosystems by modifying the nitrogen balance due to eutrophication. 

This interactive chart shows the evolution of major air pollutants:
- “main” air pollutants: particulate matter (PM2.5 and PM10), sulphur oxides (SOx), ammonia (NH3), nitrogen oxides (NOx), and non-methane volatile organic compounds (NMVOC),
- heavy metals: arsenic (As), cadmium (Cd), chromium (Cr), lead (Pb), mercury (Hg), nickel (Ni).
""")

# Option to select graph
options_AP = [':blue[Evolution of air pollutant emissions]', ':blue[Map]', ':blue[Table]']
selected_option_AP = st.radio("Select display option:", options_AP)

# Select air pollutant data 
AP_data = Emissions.loc[:, ['countries', 'Year', 'PM2.5 [t]',  'PM10 [t]', 'SOx [t]', 'NH3 [t]', 'NOx [t]', 'NMVOC [t]', 'As [t]', 'Cd [t]', 'Cr [t]', 'Pb [t]', 'Hg [t]', 'Ni [t]']]
AP_list = ['PM2.5',  'PM10', 'SOx', 'NH3', 'NOx', 'NMVOC', 'As', 'Cd', 'Cr', 'Pb', 'Hg', 'Ni']
AP_data = AP_data.loc[AP_data.countries.isin(unique_countries)]
default_pollutant = 'PM2.5'
unique_countries_AP = unique_countries
default_country_AP = 'Switzerland'
selected_pollutant = st.selectbox("Select a pollutant:", AP_list, index=AP_list.index(default_pollutant))
selected_pollutant_col = selected_pollutant + ' [t]'

# Depending on the selected option, display the corresponding content
if selected_option_AP == ':blue[Evolution of air pollutant emissions]':     # Plot of the evolution of air pollutant
    # Selection of country
    selected_country_AP = st.selectbox("Select a country:", unique_countries_AP, index=unique_countries_AP.index(default_country_AP), key='country_AP_selectbox')
    # Filter data based on selected country
    country_data_AP = AP_data.loc[AP_data['countries'] == selected_country_AP, ['Year', selected_pollutant_col]]
    # Create traces for different emissions
    traces_AP = [
        go.Scatter(x=country_data_AP['Year'], y=country_data_AP[selected_pollutant_col], mode='lines', name=selected_pollutant)
    ]
    # Create layout
    layout_AP = go.Layout(
        title=f'Emissions of {selected_pollutant} in {selected_country_AP}',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Tonnes', rangemode='tozero'),  # Fix minimum y-axis value at zero
        margin=dict(l=40, r=40, t=40, b=30)
    )
    # Plot graph
    st.plotly_chart({'data': traces_AP, 'layout': layout_AP}, use_container_width=True)
elif selected_option_AP == ':blue[Map]': # Map of European countries
    
    def plot_map_AP(column):
        # Define the min and max values for the color range per year
        AP_data['min_value'] = AP_data.groupby('Year')[column].transform('min')
        AP_data['max_value'] = AP_data.groupby('Year')[column].transform('max')

        # Create map
        fig = px.choropleth(
            AP_data,
            locations='countries',
            locationmode='country names',
            color=column,
            hover_name='countries',
            animation_frame='Year',  # Assuming 'Year' is the column name
            title="",
            color_continuous_scale=px.colors.sequential.Oranges,
            scope='europe',
            height=600,
            width=800
        )

        # Adjust the color range for each frame
        for frame in fig.frames:
            year = frame.name
            year_data = AP_data[AP_data['Year'] == year]

            # Check if the slice is not empty
            if not year_data.empty:
                min_value = year_data['min_value'].iloc[0]
                max_value = year_data['max_value'].iloc[0]
                frame.data[0].zmin = min_value
                frame.data[0].zmax = max_value
            else:
                # Set default min and max if data is not available for the year
                frame.data[0].zmin = AP_data[column].min()
                frame.data[0].zmax = AP_data[column].max()
        
        # Update Layout
        fig.update_coloraxes(colorbar_title=column)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_geos(projection_scale=1)

        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)

    plot_map_AP(selected_pollutant_col)
elif selected_option_AP == ':blue[Table]':   # Dataframe with data
    all_countries_option = "All countries"
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + unique_countries, default=all_countries_option, key='table_air_pol')
    if all_countries_option in selected_countries:
        filtered_data = AP_data.copy()  # Make a copy of the original DataFrame
    else:
        filtered_data = AP_data[AP_data['countries'].isin(selected_countries)]
    st.write(filtered_data)


    
###################################################################
##### ...but external costs remain significant  ######
##################################################################

# Section: External costs
st.header("External costs remain significant")    

st.markdown("""
In our context, external costs - or [externalities](https://en.wikipedia.org/wiki/Externality) - are the costs of air pollution to society and to the environment. Several methods are used to value externalities. Here is a short overview, and you can find a more detailed description in the methodology report available on the [E4S website](https://e4s.center/resources/reports/green-domestic-product/).

For the main air pollutants and heavy metals, we rely on the damage costs, i.e., the costs incurred by the pollution, such as agricultural production loss due to a decrease in crop yields. Most air pollutants lead to excess mortality. Although valuing excess mortality might raise ethical questions, the alternative – i.e., not accounting for such impacts – is arguably worse. Two techniques can be used to value excess mortality:
- The value of statistical life (VSL) measures how much people are willing to pay for a reduction in their risk of dying from adverse health conditions.
- The value of life-year (VOLY) estimates the damage costs based upon the loss of life expectancy, expressed as potential years of life lost and accounting for the age at which deaths occur. VOLY provides a lower estimate than VSL for health damages.

For greenhouse gases, we rely on avoidance costs, i.e., the costs to prevent externalities by decarbonizing, for two main reasons. First, damage costs are prone to significant uncertainties, with values from the literature ranging from a few euros to several thousand euros per ton of CO2. Second, international agreements have the goal to limit global temperature rise to 1.5-2°C above pre-industrial levels, thus preventing catastrophic climate change impacts. To account for uncertainties in the cost of decarbonization, we estimated the external costs with three values, taken from the European Commission report [Handbook on the external costs of transport (2020)](https://op.europa.eu/en/publication-detail/-/publication/9781f65f-8448-11ea-bf12-01aa75ed71a1/language-en): low (63 €/tCO2eq), central (104 €/tCO2eq), and high (524 €/tCO2eq).
""")

st.write("""
This interactive chart illustrates the evolution of external costs in European countries, based on the various reporting methods and externalities pricing techniques introduced earlier.
""")

# Option to select graph for external costs
options_EC = [':blue[Evolution of external costs]', ':blue[Map]', ':blue[Table]']
selected_option_EC = st.radio("Select display option:", options_EC, key="radio_EC")

# Select External Costs data
EC_data = External_costs.loc[:, ['countries', 'Year', 'External costs (Territorial & Low GHG with VOLY) scenario [Euro]',
       'External costs (Territorial & Low GHG with VSL) scenario [Euro]',
       'External costs (Territorial & Central GHG with VOLY) scenario [Euro]',
       'External costs (Territorial & Central GHG with VSL) scenario [Euro]',
       'External costs (Territorial & High GHG with VOLY) scenario [Euro]',
       'External costs (Territorial & High GHG with VSL) scenario [Euro]',
       'External costs (Residential & Low GHG with VOLY) scenario [Euro]',
       'External costs (Residential & Low GHG with VSL) scenario [Euro]',
       'External costs (Residential & Central GHG with VOLY) scenario [Euro]',
       'External costs (Residential & Central GHG with VSL) scenario [Euro]',
       'External costs (Residential & High GHG with VOLY) scenario [Euro]',
       'External costs (Residential & High GHG with VSL) scenario [Euro]',
       'External costs (Footprint & Low GHG with VOLY) scenario [Euro]',
       'External costs (Footprint & Low GHG with VSL) scenario [Euro]',
       'External costs (Footprint & Central GHG with VOLY) scenario [Euro]',
       'External costs (Footprint & Central GHG with VSL) scenario [Euro]',
       'External costs (Footprint & High GHG with VOLY) scenario [Euro]',
       'External costs (Footprint & High GHG with VSL) scenario [Euro]',
       '(Territorial & Low GHG with VOLY) scenario [%]',
       '(Territorial & Low GHG with VSL) scenario [%]',
       '(Territorial & Central GHG with VOLY) scenario [%]',
       '(Territorial & Central GHG with VSL) scenario [%]',
       '(Territorial & High GHG with VOLY) scenario [%]',
       '(Territorial & High GHG with VSL) scenario [%]',
       '(Residential & Low GHG with VOLY) scenario [%]',
       '(Residential & Low GHG with VSL) scenario [%]',
       '(Residential & Central GHG with VOLY) scenario [%]',
       '(Residential & Central GHG with VSL) scenario [%]',
       '(Residential & High GHG with VOLY) scenario [%]',
       '(Residential & High GHG with VSL) scenario [%]',
       '(Footprint & Low GHG with VOLY) scenario [%]',
       '(Footprint & Low GHG with VSL) scenario [%]',
       '(Footprint & Central GHG with VOLY) scenario [%]',
       '(Footprint & Central GHG with VSL) scenario [%]',
       '(Footprint & High GHG with VOLY) scenario [%]',
       '(Footprint & High GHG with VSL) scenario [%]']]
EC_list = ['Territorial & Low GHG with VOLY', 'Territorial & Low GHG with VSL', 'Territorial & Central GHG with VOLY', 'Territorial & Central GHG with VSL', 'Territorial & High GHG with VOLY', 'Territorial & High GHG with VSL', 'Residential & Low GHG with VOLY', 'Residential & Low GHG with VSL', 'Residential & Central GHG with VOLY', 'Residential & Central GHG with VSL', 'Residential & High GHG with VOLY', 'Residential & High GHG with VSL', 'Footprint & Low GHG with VOLY', 'Footprint & Low GHG with VSL', 'Footprint & Central GHG with VOLY', 'Footprint & Central GHG with VSL', 'Footprint & High GHG with VOLY', 'Footprint & High GHG with VSL']
default_scenario_EC = 'Territorial & Central GHG with VSL'
unique_countries_EC = EC_data['countries'].unique()
default_country_EC = 'Switzerland'

# Depending on the selected option, display the corresponding content
if selected_option_EC == ':blue[Evolution of external costs]':  # Plot of the evolution of air pollutant
    # Selection of scenario
    selected_scenario_EC = st.selectbox("Select a scenario:", EC_list, index=EC_list.index(default_scenario_EC), key="select_scenario_EC")
    # Selection of countries
    selected_countries_EC = st.multiselect("Select countries:", unique_countries_EC, default=[default_country_EC], key='countries_EC_multiselect')
    # Option to select between 'Euro' and '% of GDP'
    options_metric_EC = ['Euro', '% of GDP']
    selected_metric = st.selectbox("Select metric:", options_metric_EC, key="radio_metric_EC")
    if selected_metric == 'Euro':
        selected_scenario_col_EC = 'External costs (' + selected_scenario_EC + ') scenario [Euro]'
        
        # Create layout
        layout_EC = go.Layout(
        title=f'External costs ({selected_scenario_EC} scenario) in selected countries in Euros',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Euro', rangemode='tozero'),  # Fix minimum y-axis value at zero
        margin=dict(l=40, r=40, t=40, b=30)
    )
    else:
        selected_scenario_col_EC = '(' + selected_scenario_EC + ') scenario [%]'
        # Create layout
        layout_EC = go.Layout(
        title=f'External costs ({selected_scenario_EC} scenario) in selected countries as % of GDP',
        xaxis=dict(title='Year'),
        yaxis=dict(title='% of GDP', rangemode='tozero'),  # Fix minimum y-axis value at zero
        margin=dict(l=40, r=40, t=40, b=30)
    )
    # Create traces for different countries
    traces_EC = []
    for country in selected_countries_EC:
        country_data_EC = EC_data.loc[EC_data['countries'] == country, ['Year', selected_scenario_col_EC]]
        traces_EC.append(go.Scatter(x=country_data_EC['Year'], y=country_data_EC[selected_scenario_col_EC], mode='lines', name=country))
    # Plot graph
    st.plotly_chart({'data': traces_EC, 'layout': layout_EC}, use_container_width=True)
elif selected_option_EC == ':blue[Map]':  # Map of European countries
    # Selection of scenario
    selected_scenario_EC = st.selectbox("Select a scenario:", EC_list, index=EC_list.index(default_scenario_EC), key="select_scenario_EC")
    # Option to select between 'Euro' and '% of GDP'
    options_metric_EC = ['% of GDP', 'Euro']
    selected_metric = st.selectbox("Select metric:", options_metric_EC, key="radio_metric_EC")
    if selected_metric == 'Euro':
        selected_scenario_col_EC = 'External costs (' + selected_scenario_EC + ') scenario [Euro]'
        title_EC = 'External costs [Euro]'
    else:
        selected_scenario_col_EC = '(' + selected_scenario_EC + ') scenario [%]'
        title_EC = 'External costs [% of GDP]'
    # Define function to plot map
    def plot_map_EC(column):
        # Define the min and max values for the color range per year
        EC_data['min_value'] = EC_data.groupby('Year')[column].transform('min')
        EC_data['max_value'] = EC_data.groupby('Year')[column].transform('max')

        # Create map
        fig = px.choropleth(
            EC_data,
            locations='countries',
            locationmode='country names',
            color=column,
            hover_name='countries',
            animation_frame='Year',  # Assuming 'Year' is the column name
            title="",
            color_continuous_scale=px.colors.sequential.Oranges,
            scope='europe',
            height=600,
            width=800
        )

        # Adjust the color range for each frame
        for frame in fig.frames:
            year = frame.name
            year_data = EC_data[EC_data['Year'] == year]

            # Check if the slice is not empty
            if not year_data.empty:
                min_value = year_data['min_value'].iloc[0]
                max_value = year_data['max_value'].iloc[0]
                frame.data[0].zmin = min_value
                frame.data[0].zmax = max_value
            else:
                # Set default min and max if data is not available for the year
                frame.data[0].zmin = EC_data[column].min()
                frame.data[0].zmax = EC_data[column].max()
        
        # Update Layout
        fig.update_coloraxes(colorbar_title=title_EC)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_geos(projection_scale=1)

        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)
       
    plot_map_EC(selected_scenario_col_EC)
    
elif selected_option_EC == ':blue[Table]':  # Dataframe with data
    all_countries_option = "All countries"
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + list(unique_countries_EC), default=all_countries_option)
    if all_countries_option in selected_countries:
        filtered_data = EC_data.copy()  # Make a copy of the original DataFrame
    else:
        filtered_data = EC_data[EC_data['countries'].isin(selected_countries)]
    st.write(filtered_data)

    
############################################
##### The GrDP of European countries  ######
###########################################   

# Section: GrDP
st.header("The GrDP of European countries")

st.write("""
Here is how we calculate the GrDP:
$$
GrDP = GDP - External Costs 
$$
""")

st.write("""
This interactive chart illustrates the evolution of GDP in European countries, based on the various reporting methods and externalities pricing techniques introduced earlier.
""")

   
options_GrDP = [':blue[Evolution GDP and GrDP]', ':blue[Map]', ':blue[Table]']
selected_option_GrDP = st.radio("Select display option:", options_GrDP, key="radio_total")

# Select GrDP and GDP data 
GrDP_data = GrDP.loc[:, ['countries', 'Year', 'GrDP (Territorial & Low GHG with VOLY) scenario [Euro]',
       'GrDP (Territorial & Low GHG with VSL) scenario [Euro]',
       'GrDP (Territorial & Central GHG with VOLY) scenario [Euro]',
       'GrDP (Territorial & Central GHG with VSL) scenario [Euro]',
       'GrDP (Territorial & High GHG with VOLY) scenario [Euro]',
       'GrDP (Territorial & High GHG with VSL) scenario [Euro]',
       'GrDP (Residential & Low GHG with VOLY) scenario [Euro]',
       'GrDP (Residential & Low GHG with VSL) scenario [Euro]',
       'GrDP (Residential & Central GHG with VOLY) scenario [Euro]',
       'GrDP (Residential & Central GHG with VSL) scenario [Euro]',
       'GrDP (Residential & High GHG with VOLY) scenario [Euro]',
       'GrDP (Residential & High GHG with VSL) scenario [Euro]',
       'GrDP (Footprint & Low GHG with VOLY) scenario [Euro]',
       'GrDP (Footprint & Low GHG with VSL) scenario [Euro]',
       'GrDP (Footprint & Central GHG with VOLY) scenario [Euro]',
       'GrDP (Footprint & Central GHG with VSL) scenario [Euro]',
       'GrDP (Footprint & High GHG with VOLY) scenario [Euro]',
       'GrDP (Footprint & High GHG with VSL) scenario [Euro]', 'GrDP per capita (Territorial & Low GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Territorial & Low GHG with VSL) scenario [Euro]',
   'GrDP per capita (Territorial & Central GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Territorial & Central GHG with VSL) scenario [Euro]',
   'GrDP per capita (Territorial & High GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Territorial & High GHG with VSL) scenario [Euro]',
   'GrDP per capita (Residential & Low GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Residential & Low GHG with VSL) scenario [Euro]',
   'GrDP per capita (Residential & Central GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Residential & Central GHG with VSL) scenario [Euro]',
   'GrDP per capita (Residential & High GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Residential & High GHG with VSL) scenario [Euro]',
   'GrDP per capita (Footprint & Low GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Footprint & Low GHG with VSL) scenario [Euro]',
   'GrDP per capita (Footprint & Central GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Footprint & Central GHG with VSL) scenario [Euro]',
   'GrDP per capita (Footprint & High GHG with VOLY) scenario [Euro]',
   'GrDP per capita (Footprint & High GHG with VSL) scenario [Euro]']]
GDP_data = GrDP.loc[:, ['countries', 'Year', 'GDP per capita [Euro]']]
GDP_data = GrDP.loc[:, ['countries', 'Year', 'GDP [Euro]', 'GDP per capita [Euro]']]
GrDP_list = ['Territorial & Low GHG with VOLY', 'Territorial & Low GHG with VSL', 'Territorial & Central GHG with VOLY', 'Territorial & Central GHG with VSL', 'Territorial & High GHG with VOLY', 'Territorial & High GHG with VSL', 'Residential & Low GHG with VOLY', 'Residential & Low GHG with VSL', 'Residential & Central GHG with VOLY', 'Residential & Central GHG with VSL', 'Residential & High GHG with VOLY', 'Residential & High GHG with VSL', 'Footprint & Low GHG with VOLY', 'Footprint & Low GHG with VSL', 'Footprint & Central GHG with VOLY', 'Footprint & Central GHG with VSL', 'Footprint & High GHG with VOLY', 'Footprint & High GHG with VSL']
default_GrDP = 'Territorial & Central GHG with VSL'
unique_countries_GrDP = GrDP_data['countries'].unique()
default_country_GrDP = 'Switzerland'
selected_GrDP = st.selectbox("Select a scenario:", GrDP_list, index=GrDP_list.index(default_GrDP))

# Depending on the selected option, display the corresponding content
if selected_option_GrDP == ':blue[Evolution GDP and GrDP]':     # Plot of the evolution of GDP and GrDP
    # Selection of country
    selected_country_GrDP = st.selectbox("Select a country:", unique_countries_GrDP, index=list(unique_countries_GrDP).index(default_country_GrDP), key='country_GrDP_selectbox')
        # Option to select between 'Total' and 'Per capita'
    options_metric = ['Total', 'Per capita']
    selected_metric = st.selectbox("Select metric:", options_metric, key="radio_metric_GrDP")
    if selected_metric == 'Total':
        selected_GrDP_col = 'GrDP (' + selected_GrDP + ') scenario [Euro]'
        selected_GDP_col = 'GDP [Euro]'
        # Create layout
        layout_GrDP = go.Layout(
        title=f'GrDP ({selected_GrDP} scenario) and GDP of {selected_country_GrDP}',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Euro', rangemode='tozero'),  # Fix minimum y-axis value at zero
        margin=dict(l=40, r=40, t=40, b=30)
        )
    else:
        selected_GrDP_col = 'GrDP per capita (' + selected_GrDP + ') scenario [Euro]'
        selected_GDP_col = 'GDP per capita [Euro]'
        # Create layout
        layout_GrDP = go.Layout(
        title=f'GrDP per capita ({selected_GrDP} scenario) and GDP per capita of {selected_country_GrDP}',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Euro', rangemode='tozero'),  # Fix minimum y-axis value at zero
        margin=dict(l=40, r=40, t=40, b=30)
        )
    # Filter data based on selected country
    country_data_GrDP = GrDP_data.loc[GrDP_data['countries'] == selected_country_GrDP, ['Year', selected_GrDP_col]]
    country_data_GDP = GDP_data.loc[GDP_data['countries'] == selected_country_GrDP, ['Year', selected_GDP_col]]
    # Create traces for different emissions
    traces_GrDP = [
        go.Scatter(x=country_data_GDP['Year'], y=country_data_GDP[selected_GDP_col], mode='lines', name='GDP'),
        go.Scatter(x=country_data_GrDP['Year'], y=country_data_GrDP[selected_GrDP_col], mode='lines', name='GrDP')
    ]
    # Plot graph
    st.plotly_chart({'data': traces_GrDP, 'layout': layout_GrDP}, use_container_width=True)
elif selected_option_GrDP == ':blue[Map]': # Map of European countries
    # Option to select between 'Total' and 'Per capita'
    options_metric = ['Per capita', 'Total']
    selected_metric = st.selectbox("Select metric:", options_metric, key="radio_metric_GrDP")
    if selected_metric == 'Total':
        selected_GrDP_col = 'GrDP (' + selected_GrDP + ') scenario [Euro]'
        title_GrDP = 'GrDP [Euro]'
    else:
        selected_GrDP_col = 'GrDP per capita (' + selected_GrDP + ') scenario [Euro]'
        title_GrDP = 'GrDP per capita [Euro]'
    # Define function to plot map
    def plot_map_GrDP(column):
        # Define the min and max values for the color range per year
        GrDP_data['min_value'] = GrDP_data.groupby('Year')[column].transform('min')
        GrDP_data['max_value'] = GrDP_data.groupby('Year')[column].transform('max')

        # Create map
        fig = px.choropleth(GrDP_data,
                            locations='countries',
                            locationmode='country names',
                            color=column,
                            hover_name='countries',
                            animation_frame='Year',
                            title="",
                            color_continuous_scale=px.colors.sequential.Oranges,
                            scope='europe',
                            height=600,
                            width=800)

        # Adjust the color range for each frame
        for frame in fig.frames:
            year = frame.name
            year_data = GrDP_data[GrDP_data['Year'] == year]

            # Check if the slice is not empty
            if not year_data.empty:
                min_value = GrDP_data['min_value'].iloc[0]
                max_value = GrDP_data['max_value'].iloc[0]
                frame.data[0].zmin = min_value
                frame.data[0].zmax = max_value
            else:
                # Set default min and max if data is not available for the year
                frame.data[0].zmin = GrDP_data[column].min()
                frame.data[0].zmax = GrDP_data[column].max()
        
        # Update Layout
        fig.update_coloraxes(colorbar_title=title_GrDP)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_geos(projection_scale=1)

        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)
        
    plot_map_GrDP(selected_GrDP_col)
elif selected_option_GrDP == ':blue[Table]':   # Dataframe with data
    all_countries_option = "All countries"
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + list(unique_countries_GrDP), default=all_countries_option, key='Table_GrDP')
    if all_countries_option in selected_countries:
        filtered_data = GrDP_data.copy()  # Make a copy of the original DataFrame
    else:
        filtered_data = GrDP_data[GrDP_data['countries'].isin(selected_countries)]
    st.write(filtered_data)
    
###########################################################
##### Can we decouple economic growth and pollution ######
#########################################################

# Section: Decoupling
st.header("Can we decouple economic growth and pollution?")

st.write("##### What is decoupling ?")

st.write("According to the [OECD](https://one.oecd.org/document/sg/sd(2002)1/final/en/pdf):")

st.markdown("> Decoupling occurs when the growth rate of an environmental pressure is less than that of its economic driving force (e.g. GDP) over a given period.") 

st.markdown("""
The following chart illustrates the decoupling between economic growth (represented by GDP) and pollution (represented by emissions of various pollutants). We use two indicators to evaluate decoupling: the OECD indicator and the Intensity of Decoupling Factor.

##### OECD Indicator (D)

The OECD indicator can be interpreted as follows:
- **D < 0**: No decoupling
- **0 < D < 1**: Decoupling
- **D = 1**: Emissions = 0
- **D > 1**: Negative emissions

##### Intensity of Decoupling Factor (IF)

The Intensity of Decoupling Factor distinguishes between relative and absolute decoupling:
- **IF < -1**: No decoupling
- **-1 < IF < 0**: Relative decoupling
- **IF > 0**: Absolute decoupling

##### Types of Decoupling

- **Relative Decoupling**: Environmental impact continues to grow but at a slower rate compared to economic growth.
- **Absolute Decoupling**: Environmental impact decreases even as the economy grows.
""")

##########################################
################ Bar Plot ################
##########################################

options_Decoupling = [':blue[Bar plot]', ':blue[Table]']
selected_option_Decoupling = st.radio("Select display option:", options_Decoupling, key="radio_Decoupling")

if selected_option_Decoupling == ':blue[Bar plot]':
    options = ['GDP', 'Population']
    selected_metric = st.selectbox("Select quantity:", options, key="dropdown_quantity_decoupling")

    if selected_metric == 'GDP':

        # Selecting necessary columns
        Decoupling_OECD_data = Decoupling_OECD.loc[:, [
            'countries', 'Year', 'Territorial GHG emissions_GDP',
            'Residential GHG emissions_GDP', 'Transfer GHG emissions_GDP',
            'Footprint GHG emissions_GDP', 'Heavy Metals Emissions_GDP',
            'Air Pollutants Emissions_GDP', 'As_GDP', 'Pb_GDP', 'NOx_GDP',
            'SOx_GDP', 'NH3_GDP', 'PM2.5_GDP', 'PM10_GDP', 'NMVOC_GDP',
            'Cd_GDP', 'Hg_GDP', 'Cr_GDP', 'Ni_GDP'
        ]]
        Decoupling_Intensity_Factor_data = Decoupling_Intensity_Factor.loc[:, [
            'countries', 'Year', 'Territorial GHG emissions_GDP',
            'Residential GHG emissions_GDP', 'Transfer GHG emissions_GDP',
            'Footprint GHG emissions_GDP', 'Heavy Metals Emissions_GDP',
            'Air Pollutants Emissions_GDP', 'As_GDP', 'Pb_GDP', 'NOx_GDP',
            'SOx_GDP', 'NH3_GDP', 'PM2.5_GDP', 'PM10_GDP', 'NMVOC_GDP',
            'Cd_GDP', 'Hg_GDP', 'Cr_GDP', 'Ni_GDP'
        ]]

        Emissions_list = [
            'Territorial GHG emissions', 'Footprint GHG emissions',
            'Residential GHG emissions', 'Heavy Metals Emissions', 'Air Pollutants Emissions',
            'NOx', 'SOx', 'NH3', 'PM2.5', 'PM10', 'NMVOC', 'As', 'Pb', 'Cd', 'Hg', 'Cr', 'Ni'
        ]
        default_emission_decoupling = 'Territorial GHG emissions'
        selected_emission_decoupling = st.selectbox(
            "Select a scenario:", Emissions_list, index=Emissions_list.index(default_emission_decoupling)
        )
        selected_Decoupling_col = selected_emission_decoupling + '_GDP'
        Indicator_list = ['OECD', 'Intensity of Decoupling Factor']
        default_indicator = 'OECD'
        selected_indicator = st.selectbox(
            "Select an indicator:", Indicator_list, index=Indicator_list.index(default_indicator)
        )

        # Filter data based on selected indicator and emission type
        if selected_indicator == 'OECD':
            data_decoupling = Decoupling_OECD_data.loc[
                Decoupling_OECD_data['Year'] == 2021, ['countries', selected_Decoupling_col]
            ]
        else:
            data_decoupling = Decoupling_Intensity_Factor_data.loc[
                Decoupling_Intensity_Factor_data['Year'] == 2021, ['countries', selected_Decoupling_col]
            ]

        # Sort the data by the selected decoupling column in descending order
        data_decoupling = data_decoupling.sort_values(by=selected_Decoupling_col, ascending=True)

        # Create traces for different emissions
        Bar_plot_decoupling = [
            go.Bar(x=data_decoupling[selected_Decoupling_col], y=data_decoupling['countries'], name=selected_emission_decoupling, orientation='h')
        ]

        # Create layout
        layout_decoupling = go.Layout(
            title=f'Decoupling of {selected_emission_decoupling} with GDP between 2011 and 2021 per Country ({selected_indicator})',
            xaxis_title=f'Decoupling of {selected_emission_decoupling} with GDP',
            yaxis_title='Country',
            xaxis=dict(rangemode='tozero'),  # Fix minimum x-axis value at zero
            margin=dict(l=50, r=40, t=40, b=50),  # Increase left and bottom margins
            height=600,  # Set a fixed height for the plot
            yaxis=dict(automargin=True)  # Automatically adjust margins to fit labels
        )

        # Plot graph
        st.plotly_chart({'data': Bar_plot_decoupling, 'layout': layout_decoupling}, use_container_width=True)

    elif selected_metric == 'Population':

        # Selecting necessary columns
        Decoupling_OECD_data = Decoupling_OECD.loc[:, [
            'countries', 'Year', 'Territorial GHG emissions_Population',
            'Residential GHG emissions_Population',
            'Transfer GHG emissions_Population',
            'Footprint GHG emissions_Population',
            'As_Population',
            'Pb_Population',
            'NOx_Population',
            'SOx_Population',
            'NH3_Population',
            'PM2.5_Population',
            'PM10_Population',
            'NMVOC_Population',
            'Cd_Population',
            'Hg_Population',
            'Cr_Population',
            'Ni_Population',
            'Heavy Metals Emissions_Population',
            'Air Pollutants Emissions_Population'
        ]]
        Decoupling_Intensity_Factor_data = Decoupling_Intensity_Factor.loc[:, [
            'countries', 'Year', 'Territorial GHG emissions_Population',
            'Residential GHG emissions_Population',
            'Transfer GHG emissions_Population',
            'Footprint GHG emissions_Population',
            'As_Population',
            'Pb_Population',
            'NOx_Population',
            'SOx_Population',
            'NH3_Population',
            'PM2.5_Population',
            'PM10_Population',
            'NMVOC_Population',
            'Cd_Population',
            'Hg_Population',
            'Cr_Population',
            'Ni_Population',
            'Heavy Metals Emissions_Population',
            'Air Pollutants Emissions_Population'
        ]]

        Emissions_list = [
            'Territorial GHG emissions', 'Footprint GHG emissions',
            'Residential GHG emissions', 'Heavy Metals Emissions', 'Air Pollutants Emissions',
            'NOx', 'SOx', 'NH3', 'PM2.5', 'PM10', 'NMVOC', 'As', 'Pb', 'Cd', 'Hg', 'Cr', 'Ni'
        ]
        default_emission_decoupling = 'Territorial GHG emissions'
        selected_emission_decoupling = st.selectbox(
            "Select a scenario:", Emissions_list, index=Emissions_list.index(default_emission_decoupling)
        )
        selected_Decoupling_col = selected_emission_decoupling + '_Population'
        Indicator_list = ['OECD', 'Intensity of Decoupling Factor']
        default_indicator = 'OECD'
        selected_indicator = st.selectbox(
            "Select an indicator:", Indicator_list, index=Indicator_list.index(default_indicator)
        )

        # Filter data based on selected indicator and emission type
        if selected_indicator == 'OECD':
            data_decoupling = Decoupling_OECD_data.loc[
                Decoupling_OECD_data['Year'] == 2021, ['countries', selected_Decoupling_col]
            ]
        else:
            data_decoupling = Decoupling_Intensity_Factor_data.loc[
                Decoupling_Intensity_Factor_data['Year'] == 2021, ['countries', selected_Decoupling_col]
            ]

        # Sort the data by the selected decoupling column in descending order
        data_decoupling = data_decoupling.sort_values(by=selected_Decoupling_col, ascending=True)

        # Create traces for different emissions
        Bar_plot_decoupling = [
            go.Bar(x=data_decoupling[selected_Decoupling_col], y=data_decoupling['countries'], name=selected_emission_decoupling, orientation='h')
        ]

        # Create layout
        layout_decoupling = go.Layout(
            title=f'Decoupling of {selected_emission_decoupling} with population between 2011 and 2021 per Country ({selected_indicator})',
            xaxis_title=f'Decoupling of {selected_emission_decoupling} with population',
            yaxis_title='Country',
            xaxis=dict(rangemode='tozero'),  # Fix minimum x-axis value at zero
            margin=dict(l=50, r=40, t=40, b=50),  # Increase left and bottom margins
            height=600,  # Set a fixed height for the plot
            yaxis=dict(automargin=True)  # Automatically adjust margins to fit labels
        )

        # Plot graph
        st.plotly_chart({'data': Bar_plot_decoupling, 'layout': layout_decoupling}, use_container_width=True)

elif selected_option_Decoupling == ':blue[Table]':
    options = ['OECD', 'Intensity of Decoupling Factor']
    selected_indicator_table = st.selectbox("Select indicator:", options, key="dropdown_quantity_decoupling_table")
    
    if selected_indicator_table == 'OECD':
        Decoupling_OECD_filtered = Decoupling_OECD.loc[:, [
            'countries', 'Year', 'Territorial GHG emissions_GDP',
            'Residential GHG emissions_GDP', 'Transfer GHG emissions_GDP',
            'Footprint GHG emissions_GDP', 'Heavy Metals Emissions_GDP',
            'Air Pollutants Emissions_GDP', 'As_GDP', 'Pb_GDP', 'NOx_GDP',
            'SOx_GDP', 'NH3_GDP', 'PM2.5_GDP', 'PM10_GDP', 'NMVOC_GDP',
            'Cd_GDP', 'Hg_GDP', 'Cr_GDP', 'Ni_GDP', 'Territorial GHG emissions_Population',
            'Residential GHG emissions_Population',
            'Transfer GHG emissions_Population',
            'Footprint GHG emissions_Population',
            'As_Population',
            'Pb_Population',
            'NOx_Population',
            'SOx_Population',
            'NH3_Population',
            'PM2.5_Population',
            'PM10_Population',
            'NMVOC_Population',
            'Cd_Population',
            'Hg_Population',
            'Cr_Population',
            'Ni_Population',
            'Heavy Metals Emissions_Population',
            'Air Pollutants Emissions_Population'
        ]]

        all_countries_option = "All countries"
        unique_countries_OECD = Decoupling_OECD_filtered['countries'].unique()
        selected_countries = st.multiselect("Select countries:", [all_countries_option] + list(unique_countries_OECD), default=all_countries_option)
        if all_countries_option in selected_countries:
            filtered_data = Decoupling_OECD_filtered.copy()  # Make a copy of the original DataFrame
        else:
            filtered_data = Decoupling_OECD_filtered[Decoupling_OECD_filtered['countries'].isin(selected_countries)]
        st.write(filtered_data)

    elif selected_indicator_table == 'Intensity Factor':
        Decoupling_IF_filtered = Decoupling_Intensity_Factor.loc[:, [
            'countries', 'Year', 'Territorial GHG emissions_GDP',
            'Residential GHG emissions_GDP', 'Transfer GHG emissions_GDP',
            'Footprint GHG emissions_GDP', 'Heavy Metals Emissions_GDP',
            'Air Pollutants Emissions_GDP', 'As_GDP', 'Pb_GDP', 'NOx_GDP',
            'SOx_GDP', 'NH3_GDP', 'PM2.5_GDP', 'PM10_GDP', 'NMVOC_GDP',
            'Cd_GDP', 'Hg_GDP', 'Cr_GDP', 'Ni_GDP', 'Territorial GHG emissions_Population',
            'Residential GHG emissions_Population',
            'Transfer GHG emissions_Population',
            'Footprint GHG emissions_Population',
            'As_Population',
            'Pb_Population',
            'NOx_Population',
            'SOx_Population',
            'NH3_Population',
            'PM2.5_Population',
            'PM10_Population',
            'NMVOC_Population',
            'Cd_Population',
            'Hg_Population',
            'Cr_Population',
            'Ni_Population',
            'Heavy Metals Emissions_Population',
            'Air Pollutants Emissions_Population'
        ]]

        all_countries_option = "All countries"
        unique_countries_IF = Decoupling_IF_filtered['countries'].unique()
        selected_countries = st.multiselect("Select countries:", [all_countries_option] + list(unique_countries_IF), default=all_countries_option)
        if all_countries_option in selected_countries:
            filtered_data = Decoupling_IF_filtered.copy()  # Make a copy of the original DataFrame
        else:
            filtered_data = Decoupling_IF_filtered[Decoupling_IF_filtered['countries'].isin(selected_countries)]
        st.write(filtered_data)

    
##############################################
################ Scatter Plot ################
##############################################

st.markdown("""
The following chart, which plots the relative differences in emissions (ΔEmissions) and GDP (ΔGDP), distinguishes even more forms of decoupling:

- **Strong Negative Decoupling**: Emissions decrease proportionally more than GDP decreases.

- **Weak Negative Decoupling**: Emissions decrease less than GDP decreases.

- **Recessive Coupling**: Emissions decrease at a rate similar to or slightly more than GDP decreases.

- **Recessive Decoupling**: Emissions decrease much more than GDP decreases.

- **Weak Decoupling**: Emissions remain stable or decrease slightly, while GDP increases.

- **Expansive Negative Decoupling**: Emissions increase much more than GDP increases.

- **Expansive Coupling**: Emissions increase at a rate similar to GDP increases.

- **Strong Decoupling**: Emissions decrease proportionally more than GDP increases.

""")

import pandas as pd
import plotly.graph_objs as go
import streamlit as st

# Define color for each decoupling category
color_mapping = {
    'darkred': 'Strong negative decoupling',        # Dark Red
    'darkorange': 'Weak negative decoupling',       # Dark Orange
    'deeppink': 'Expansive coupling',               # Deep Pink
    'gold': 'Expansive negative decoupling',        # Gold
    'royalblue': 'Weak decoupling',                 # Royal Blue
    'darkviolet': 'Recessive decoupling',           # Dark Violet
    'darkmagenta': 'Recessive coupling',            # Dark Magenta
    'darkgreen': 'Strong decoupling',               # Dark Green
    'grey': 'Default color'                         # Grey
}

# Convert the dictionary to a DataFrame
df_color_mapping = pd.DataFrame(list(color_mapping.items()), columns=['Color', 'Category'])

# Create a reverse mapping from category to color for easy lookup
category_to_color = df_color_mapping.set_index('Category')['Color'].to_dict()

# Assuming Decoupling_Relative_Difference is already defined and loaded

options_RelDif = [':blue[Scatter plot]', ':blue[Table]']
selected_option_RelDif = st.radio("Select display option:", options_RelDif, key="radio_RelDif")

def get_color(row, metric_col):
    if row[metric_col] > 0 and row[selected_RelDif_col] > 0:
        if row[selected_RelDif_col] / row[metric_col] > 1.2:
            return category_to_color['Expansive negative decoupling']
        elif row[selected_RelDif_col] / row[metric_col] >= 0.8:
            return category_to_color['Expansive coupling']
        else:
            return category_to_color['Weak decoupling']
    elif row[metric_col] > 0 and row[selected_RelDif_col] < 0:
        return category_to_color['Strong decoupling']
    elif row[metric_col] < 0 and row[selected_RelDif_col] < 0:
        if row[selected_RelDif_col] / row[metric_col] > 1.2:
            return category_to_color['Recessive coupling']
        elif row[selected_RelDif_col] / row[metric_col] >= 0.8:
            return category_to_color['Recessive decoupling']
        else:
            return category_to_color['Weak negative decoupling']
    elif row[metric_col] < 0 and row[selected_RelDif_col] > 0:
        return category_to_color['Strong negative decoupling']
    else:
        return category_to_color['Default color']
    
RelDif_data = Decoupling_Relative_Difference.loc[:, [
        'countries', 'Year', 'Territorial GHG emissions',
        'Residential GHG emissions',
        'Transfer GHG emissions',
        'Footprint GHG emissions',
        'As', 'Pb', 'NOx', 'SOx', 'NH3', 'PM2.5', 'PM10', 'NMVOC',
        'Cd', 'Hg', 'Cr', 'Ni', 'GDP', 'Population', 'Heavy Metals Emissions', 'Air Pollutants Emissions'
    ]]

if selected_option_RelDif == ':blue[Scatter plot]':
    options = ['GDP', 'Population']
    selected_metric = st.selectbox("Select quantity:", options, key="dropdown_quantity_RelDif")

    Emissions_list = [
        'Territorial GHG emissions', 'Footprint GHG emissions',
        'Residential GHG emissions', 'Heavy Metals Emissions', 'Air Pollutants Emissions',
        'NOx', 'SOx', 'NH3', 'PM2.5', 'PM10', 'NMVOC', 'As', 'Pb', 'Cd', 'Hg', 'Cr', 'Ni'
    ]
    default_emission_RelDif = 'Territorial GHG emissions'
    selected_emission_RelDif = st.selectbox(
        "Select a scenario:", Emissions_list, index=Emissions_list.index(default_emission_RelDif), key="emission_rel_diff_selectbox"
    )
    selected_RelDif_col = selected_emission_RelDif

    # Filter data based on selected emission type
    data_rel_dif = RelDif_data.loc[
        RelDif_data['Year'] == 2021, ['countries', 'GDP', 'Population', selected_RelDif_col]
    ]

    data_rel_dif['color'] = data_rel_dif.apply(lambda row: get_color(row, selected_metric), axis=1)

    # Create traces for different emissions as a scatter plot
    Scatter_plot_RelDif = [
        go.Scatter(
            x=data_rel_dif[selected_metric], 
            y=data_rel_dif[selected_RelDif_col], 
            mode='markers',
            marker=dict(color=data_rel_dif['color']),
            text=data_rel_dif['countries'],  # Add country names for hover text
            hoverinfo='text+x+y',  # Specify what info to show on hover
            showlegend=False
        )
    ]

    # Identify unique colors present in the data
    unique_colors = data_rel_dif['color'].unique()

    # Add custom legend traces
    for color in unique_colors:
        category_name = df_color_mapping[df_color_mapping['Color'] == color]['Category'].values[0]
        Scatter_plot_RelDif.append(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(color=color),
                showlegend=True,
                name=category_name
            )
        )

    x_min = min(data_rel_dif[selected_metric])
    x_max = max(data_rel_dif[selected_metric])
    y_min = min(data_rel_dif[selected_RelDif_col])
    y_max = max(data_rel_dif[selected_RelDif_col])

    x_axis_min = - x_max - 0.1
    x_axis_max = x_max + 0.1
    y_axis_min = - y_max - 0.1
    y_axis_max = y_max + 0.1

    # Create layout with quadrant lines
    layout_RelDif = go.Layout(
        title=f'Decoupling between {selected_emission_RelDif} and {selected_metric} between 2011 and 2021 per Country',
        xaxis=dict(title=f'Δ{selected_metric}', range=[x_axis_min, x_axis_max]),  # Ensure all quadrants are visible
        yaxis=dict(title=f'Δ{selected_emission_RelDif}', range=[y_axis_min, y_axis_max]),  # Fix minimum y-axis value at zero
        shapes=[
            # Line for x-axis (horizontal)
            dict(
                type='line',
                x0=x_axis_min,
                y0=0,
                x1=x_axis_max,
                y1=0,
                line=dict(
                    color="grey",
                    width=0.5
                )
            ),
            # Line for y-axis (vertical)
            dict(
                type='line',
                x0=0,
                y0=y_axis_min,
                x1=0,
                y1=y_axis_max,
                line=dict(
                    color="grey",
                    width=0.5
                )
            )
        ],
        margin=dict(l=50, r=40, t=40, b=50),  # Increase left and bottom margins
        height=600  # Set a fixed height for the plot
    )

    # Create figure
    fig = go.Figure(data=Scatter_plot_RelDif, layout=layout_RelDif)

    # Plot graph
    st.plotly_chart(fig, use_container_width=True)

elif selected_option_RelDif == ':blue[Table]':
    all_countries_option = "All countries"
    unique_countries_RelDif = RelDif_data['countries'].unique()
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + list(unique_countries_RelDif), default=all_countries_option, key='Table_RelDif')
    if all_countries_option in selected_countries:
        filtered_data = RelDif_data.copy()  # Make a copy of the original DataFrame
    else:
        filtered_data = RelDif_data[RelDif_data['countries'].isin(selected_countries)]
    st.write(filtered_data)

