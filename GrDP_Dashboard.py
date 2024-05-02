import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import re

# Set seaborn theme
sns.set_theme()

# Load data
External_costs = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/ExternalCostsDetailed.csv')
External_costs_total = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/ExternalCostsTotal.csv')
External_Costs_total_per_capita = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/ExternalCostsTotalPerCapita.csv')
GrDP = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/GrDP.csv')
GrDP_per_capita = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/GrDPPerCapita.csv')
Data_for_GrDP = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/DataForCalc.csv')
Data_for_calc = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/DataForEmissions.csv')
External_Costs_Percent_GDP = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/ExternalCostsPercentGDP.csv')
Decoupling_GDP_OECD = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/Decoupling_GDP_OECD.csv')
Decoupling_POP_OECD = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/Decoupling_POP_OECD.csv')
IntensityDecouplingFactor_GDP = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/IntensityDecouplingFactor_GDP.csv')
IntensityDecouplingFactor_POP = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/IntensityDecouplingFactor_POP.csv')
RelDifference_for_decoupling = pd.read_csv('https://raw.githubusercontent.com/AntoineTrabia/Green-Domestic-Product/main/data/RelDifference_for_decoupling.csv')

#############################
##### GrDP Dashboard  ######
############################

# Title
st.title("Going beyond the GDP with the GrDP: Factoring health and environmental costs in economic success")

st.image("https://viewpointvancouver.ca/wp-content/uploads/2012/11/new-yorker-shareholder-value.jpg", caption="Source: New Yorker", use_column_width=True)
#st.image("https://dwighttowers.wordpress.com/wp-content/uploads/2011/05/polyp_cartoon_economic_growth_ecology.jpg?w=450&h=359", caption="Source: Dwighttowers", use_column_width=True)


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

st.markdown("""
With E4S, we propose a novel indicator, the Green Domestic Product (GrDP), to remedy some of the shortcomings of GDP. The GrDP is calculated by subtracting the external costs associated with producing goods and services from the standard measurement of GDP. The current scope of the GrDP includes the emissions of greenhouse gases (GHG), air pollutants, and heavy metals. The impacts covered include climate change, health issues, decrease in crops’ yields and biomass production, buildings degradation, and damages to ecosystems due to eutrophication. You can learn more about the GrDP, including a detailed description of the method used, data scources, and assumptions, on the [E4S webpage Green Domestic Product](https://e4s.center/resources/reports/green-domestic-product/). 
""")

st.write("""
This article allows you to interactively explore the pollution and external costs, GrDP, and decoupling between economic growth and environmental pollution in European countries.
""")

# Create a table of contents
toc_items = ["What is the Green Domestic Product?",
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
options = ['Evolution of GHG emissions', 'Map', 'Table']
selected_option = st.radio("Select display option:", options)

# Select GHG data 
GHG_data = Data_for_calc.loc[:,['countries', 'Year', 'Territorial GHG emissions [t]', 'Residential GHG emissions [t]', 'Footprint GHG emissions [t]', 'Transfer GHG emissions [t]']]
GHG_data['Transfer GHG emissions [t]'] *= -1
unique_countries = sorted(Data_for_calc['countries'].unique())

# Depending on the selected option, display the corresponding content
if selected_option == 'Evolution of GHG emissions':     # Plot of the evolution of GHG
    # Selection of country
    default_country = 'Switzerland'
    selected_country = st.selectbox("Select a country:", unique_countries, index=unique_countries.index(default_country))
    # Filter data based on selected country
    country_data = GHG_data[GHG_data['countries'] == selected_country]
    # Create traces for different emissions
    traces = [
        go.Scatter(x=country_data['Year'], y=country_data['Territorial GHG emissions [t]'], mode='lines', name='Territorial Emissions'),
        go.Scatter(x=country_data['Year'], y=country_data['Residential GHG emissions [t]'], mode='lines', name='Residential Emissions'),
        go.Scatter(x=country_data['Year'], y=country_data['Footprint GHG emissions [t]'], mode='lines', name='Footprint Emissions')
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
elif selected_option == 'Map':            # Map of European countries
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
        # Create map
        fig = px.choropleth(GHG_data,
                            locations='countries',
                            locationmode='country names',
                            color=column,
                            hover_name='countries',
                            animation_frame='Year',
                            title="",
                            color_continuous_scale=color_scale,
                            range_color=range_col,
                            scope='europe',
                            height=600,
                            width=800)
        # Udpdate Layout
        fig.update_coloraxes(colorbar_title=selected_scenario)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(projection_scale=1) 
        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)
    plot_map(selected_scenario)
elif selected_option == 'Table':   # Dataframe with data
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
options_AP = ['Evolution of air pollutant emissions', 'Map', 'Table']
selected_option_AP = st.radio("Select display option:", options_AP)

# Select air pollutant data 
AP_data = Data_for_calc.loc[:,['countries', 'Year', 'PM2.5 [t]',  'PM10 [t]', 'SOx [t]', 'NH3 [t]', 'NOx [t]', 'NMVOC [t]', 'As [t]', 'Cd [t]', 'Cr [t]', 'Pb [t]', 'Hg [t]', 'Ni [t]']]
AP_list = ['PM2.5',  'PM10', 'SOx', 'NH3', 'NOx', 'NMVOC', 'As', 'Cd', 'Cr', 'Pb', 'Hg', 'Ni']
default_pollutant = 'PM2.5'
unique_countries_AP = unique_countries
default_country_AP = 'Switzerland'
selected_pollutant = st.selectbox("Select a pollutant:", AP_list, index=AP_list.index(default_pollutant))
selected_pollutant_col = selected_pollutant + ' [t]'

# Depending on the selected option, display the corresponding content
if selected_option_AP == 'Evolution of air pollutant emissions':     # Plot of the evolution of air pollutant
    # Selection of country
    selected_country_AP = st.selectbox("Select a country:", unique_countries_AP, index=unique_countries_AP.index(default_country_AP), key='country_AP_selectbox')
    # Filter data based on selected country
    country_data_AP = AP_data.loc[AP_data['countries'] == selected_country_AP,['Year', selected_pollutant_col]]
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
elif selected_option_AP == 'Map':            # Map of European countries
    # Define function to plot map
    def plot_map_AP(column):
        # Create map
        fig = px.choropleth(AP_data,
                            locations='countries',
                            locationmode='country names',
                            color=column,
                            hover_name='countries',
                            animation_frame='Year',
                            title="",
                            color_continuous_scale=px.colors.sequential.Oranges,
                            range_color=(0, AP_data[selected_pollutant_col].max()),
                            scope='europe',
                            height=600,
                            width=800)
        # Udpdate Layout
        fig.update_coloraxes(colorbar_title=selected_pollutant_col)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_geos(projection_scale=1) 
        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)
    plot_map_AP(selected_pollutant_col)
elif selected_option_AP == 'Table':   # Dataframe with data
    all_countries_option = "All countries"
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + unique_countries, default=all_countries_option)
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
    
############################################
##### The GrDP of European countries  ######
###########################################   

# Section: GrDP
st.header("The GrDP of European countries")

###########################################################
##### Can we decouple economic growth and pollution ######
#########################################################

# Section: Decoupling
st.header("Can we decouple economic growth and pollution?")