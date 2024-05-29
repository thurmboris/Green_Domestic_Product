#################################################
####### Green Domestic Product Web App #########
################################################

#############################################################################
# How to run locally?
# Open a console, change directory to python script location, execute: 
#        "streamlit run GrDP_Dashboard.py"
###
# How to automatically update local web app when script is edited?
# Open a console, change directory to python script location, execute:
#         "python GrDP_watchdog_script.py"
############################################################################

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import re

# Load data
Emissions = pd.read_csv('https://raw.githubusercontent.com/thurmboris/Green_Domestic_Product/main/data/final/Emissions.csv')
External_costs = pd.read_csv('https://raw.githubusercontent.com/thurmboris/Green_Domestic_Product/main/data/final/ExternalCosts.csv')
GrDP = pd.read_csv('https://raw.githubusercontent.com/thurmboris/Green_Domestic_Product/main/data/final/GrDP.csv')
Decoupling_OECD = pd.read_csv('https://raw.githubusercontent.com/thurmboris/Green_Domestic_Product/main/data/final/Decoupling_OECD_Indicator.csv')
Decoupling_Intensity_Factor = pd.read_csv('https://raw.githubusercontent.com/thurmboris/Green_Domestic_Product/main/data/final/Decoupling_Intensity_Factor.csv')
Decoupling_Relative_Difference = pd.read_csv('https://raw.githubusercontent.com/thurmboris/Green_Domestic_Product/main/data/final/Decoupling_Relative_Difference.csv')

# Define the custom CSS
custom_css = """
<style>
.stApp {
    background-color: #333333; /* Black background color */
    color: #FFFFFF; /* White text color */
}

.stMarkdown, .stText, .stWrite {
    color: #FFFFFF; /* Ensure other texts remain white */
}

.stTitle {
    color: white; /* White color for the title */
}

h1 {
    color: #1E90FF; /* Dodger Blue for main titles */
    text-align: left; /* Titles alignment */
}

h2, h3 {
    color: #87CEFA; /* Light Sky Blue for subtitles */
    text-align: left; /* Titles alignment */
}

h4, h5, h6 {
    color: #B0E0E6; /* Powder Blue for smaller titles */
}

/* Target blockquote element and its pseudo-element */
blockquote {
    border-left: 1px solid #FFFFFF; /* Change the color of the blockquote line */
    color: #FFFFFF; /* Ensure text inside blockquote is white */
}

blockquote:before {
    background-color: #FFFFFF; /* Ensure pseudo-element is also white */
}

.stSelectbox > label {
    color: #FFFFFF;
}

.stMultiselect > label {
    color: #FFFFFF;
}

.stRadio > label {
    color: #FFFFFF;
}

.main > div {
            padding-left: 0rem;
            padding-right: 0rem;
        }

/* Ensure code blocks or any preformatted text is also clear */
code, pre {
    background-color: #444444; /* Slightly lighter grey for code blocks */
    color: #FFFFFF; /* White text for code */
}

/* Style for hyperlinks */
a, .stMarkdown a {
    color: #B0E0E6; /* Powder Blue for hyperlinks */
    text-decoration: none; /* Remove underline from links */
}

a:hover, .stMarkdown a:hover {
    color: #87CEFA; /* Light Sky Blue when hovered */
    text-decoration: underline; /* Underline links on hover */
}

/* Style for tooltip */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted #005DC4; /* Powder Blue dotted underline */
  color: #B0E0E6; /* Powder Blue text color for the main body of text */
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 400px; 
  background-color: #333333; /* Match background color */
  color: #B0E0E6; /* Powder Blue text color */
  text-align: center;
  border-radius: 5px;
  padding: 10px; /* Increase padding for better readability */
  position: absolute;
  z-index: 1;
  bottom: 125%; /* Position the tooltip above the text */
  left: 50%;
  transform: translateX(-50%); /* Center the tooltip */
  opacity: 0;
  transition: opacity 0.3s;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #005DC4; /* Powder Blue border */
  font-size: 0.9em; /* Reduce font size to 90% of the main body text size */
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}

/* Sidebar table of contents */
.stSidebar, .stSidebar .sidebar-content {
    background-color: #222222; /* Dark background color */
    color: #FFFFFF; /* White text color */
}

.stSidebar .sidebar-content a {
    color: #87CEFA; /* Powder Blue for hyperlinks */
}

.stSidebar .sidebar-content a:hover {
    color: #87CEFA; /* Light Sky Blue when hovered */
}

</style>
"""

# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Create a table of contents
toc_items = ["Why the Green Domestic Product?",
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

#############################
##### GrDP Dashboard  ######
############################

# Title
st.title("Going beyond the GDP with the GrDP")

st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: 0px; padding-top: 5px; color: #1E90FF'> Factoring health and environmental costs in economic success </h2>", unsafe_allow_html=True)

st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)  # Add big spacing

st.image("https://viewpointvancouver.ca/wp-content/uploads/2012/11/new-yorker-shareholder-value.jpg", caption="Source: New Yorker", use_column_width=True)
#st.image("https://dwighttowers.wordpress.com/wp-content/uploads/2011/05/polyp_cartoon_economic_growth_ecology.jpg?w=450&h=359", caption="Source: Dwighttowers", use_column_width=True)

##########################
##### Abstract ######
#########################

# Introduction paragraph

st.markdown("""
At [Enterprise for Society (E4S)](https://e4s.center/), we propose a shift beyond the Gross Domestic Product (GDP) towards a more comprehensive indicator: the Green Domestic Product (GrDP). The idea behind the GrDP is to extend the scope of the GDP by integrating the depletion of natural, social, and human capital. Concretely, the GrDP is defined as the GDP minus the external costs associated with economic activities, including the costs related to the emissions of greenhouse gases (GHG), air pollutants, and heavy metals.
Our research underscores three key findings:

1. In Europe, the gap between GDP and GrDP is narrowing, indicating that the economy is growing while external costs due to pollution are decreasing.

2. Pollution costs persist at significant levels throughout Europe, ranging from approximately 5% of GDP in Switzerland and Nordic countries to over 30% in Eastern European nations.

3. While there are glimpses of decoupling between economic growth and pollution, the pace of decarbonisation remains insufficient to achieve our goal of net zero GHG emissions by 2050.
""")

#st.write("""
#Our decisions are heavily influenced by what we know and by what we measure. Therefore, flawed measurements can skew our judgment and lead to distorted decisions. With GrDP, which accounts for economic, environmental, and social dimensions, our aim is to empower individuals, particularly policymakers, to make more informed and sustainable choices. This approach transcends the traditional dichotomy between fostering economic growth and protecting the environment, offering a path towards sustainable prosperity and well-being.
#""")

st.write("""
This article allows you to interactively explore these results and visualize the pollution and external costs, GrDP, and decoupling between economic growth and environmental pollution in European countries.
""")

##########################
##### Introduction ######
#########################

# Introduction paragraph
st.header("Why the Green Domestic Product?")

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
- Territorial Emissions: accounts for all emissions from residents and non-residents inside a country. The National Emission Inventory follows the Intergovernmental Panel on Climate Change (IPCC) guidelines and is used as a basis for setting GHGs reduction targets in the context of international agreements such as the Kyoto Protocol and the Paris Agreement. Data source: European Environment Agency (EEA), via [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/env_air_gge__custom_11586061/default/table?lang=en) 
- Residential Emissions: accounts for all emissions resulting from the activities of a country’s residents, including the ones abroad. Data source: [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/env_ac_ainah_r2__custom_11586096/default/table?lang=en) 
- Transfer Emissions: emissions generated by the production of goods and services that are imported minus the emissions generated by the production of goods and services that are exported, as calculated in the [Global Carbon Atlas](https://globalcarbonatlas.org/emissions/carbon-emissions/). 
- Footprint Emissions: sum of the residential and transfer emissions. These emissions are often called "consumption-based" since emissions are allocated according to where they were consumed, rather than where they were produced with territorial emissions reporting.
""")

# Option to select graph
options = [':blue[Evolution of GHG emissions]', ':blue[Map]', ':blue[Table]']
selected_option = st.radio("Select display option", options)

# Select GHG data 
GHG_data = Emissions.loc[:,['countries', 'Year', 'Territorial GHG emissions [t]', 'Residential GHG emissions [t]', 'Footprint GHG emissions [t]', 'Transfer GHG emissions [t]']]
GHG_data['Transfer GHG emissions [t]'] *= -1
GHG_data = GHG_data.sort_values(by=['countries', 'Year'])
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
    
elif selected_option == ':blue[Map]':            # Map of European countries
    # Display map functionality
    selected_scenario = st.selectbox("Select Scenario:", GHG_data.columns[2:])
    # Define function to plot map
    def plot_map(column):
        # Visualization options
        if  selected_scenario == 'Transfer GHG emissions [t]':
            color_scale = px.colors.diverging.RdYlGn_r  # Green for negative, red for positive
            range_col = (-GHG_data['Transfer GHG emissions [t]'].max(), GHG_data['Transfer GHG emissions [t]'].max())     # Range to fix the legend independently of years
            legend_title = 'Transfer GHG<br>emissions [t]'
        elif selected_scenario == 'Territorial GHG emissions [t]':
            color_scale = px.colors.sequential.Oranges  # Shades of orange
            range_col = (0, GHG_data['Territorial GHG emissions [t]'].max())
            legend_title = 'Territorial GHG<br>emissions [t]'
        elif selected_scenario == 'Residential GHG emissions [t]':
            color_scale = px.colors.sequential.Oranges  # Shades of orange
            range_col = (0, GHG_data['Residential GHG emissions [t]'].max())
            legend_title = 'Residential GHG<br>emissions [t]'
        elif selected_scenario == 'Footprint GHG emissions [t]':
            color_scale = px.colors.sequential.Oranges  # Shades of orange
            range_col = (0, GHG_data['Footprint GHG emissions [t]'].max())
            legend_title = 'Footprint GHG<br>emissions [t]'    
        fig = px.choropleth(
            GHG_data,
            locations='countries',
            locationmode='country names',
            color=column,
            hover_name='countries',
            animation_frame='Year',  # Assuming 'Year' is the column name
            title="",
            color_continuous_scale=color_scale,
            range_color=range_col,
            scope='europe',
            height=600,
            width=800
        )  
        # Update Layout
        fig.update_coloraxes(colorbar_title=legend_title)
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(
                projection_scale=1.7,  # Adjust this value to zoom in or out
                center=dict(lat=55, lon=10)  # Center on mainland Europe
            ),
            updatemenus=[{
                'x': 0.1,
                'xanchor': 'right',
                'y': 0.1,
                'yanchor': 'top'
            }],
            sliders=[{
                'steps': [{
                    'args': [[frame.name], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 300}}],
                    'label': frame.name,
                    'method': 'animate'
                } for frame in fig.frames],
                'active': len(fig.frames) - 1,  # Set the slider to the latest year
                'x': 0.1,
                'y': 0.1,
                'len': 0.9,
                'transition': {'duration': 300, 'easing': 'cubic-in-out'}
            }]            
        )
        fig.update_traces(z=fig.frames[-1].data[0].z, hovertemplate=fig.frames[-1].data[0].hovertemplate)
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

Data source: European Environment Agency (EEA), via [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/ENV_AIR_EMIS__custom_11586313/default/table?lang=en)
""")

# Option to select graph
options_AP = [':blue[Evolution of air pollutant emissions]', ':blue[Map]', ':blue[Table]']
selected_option_AP = st.radio("Select display option:", options_AP)

# Select air pollutant data 
AP_data = Emissions.loc[:, ['countries', 'Year', 'PM2.5 [t]',  'PM10 [t]', 'SOx [t]', 'NH3 [t]', 'NOx [t]', 'NMVOC [t]', 'As [t]', 'Cd [t]', 'Cr [t]', 'Pb [t]', 'Hg [t]', 'Ni [t]']]
AP_list = ['PM2.5',  'PM10', 'SOx', 'NH3', 'NOx', 'NMVOC', 'As', 'Cd', 'Cr', 'Pb', 'Hg', 'Ni']
unique_countries_AP = unique_countries
AP_data = AP_data.loc[AP_data.countries.isin(unique_countries_AP)]
AP_data = AP_data.sort_values(by=['countries', 'Year'])
default_country_AP = 'Switzerland'

# Select pollutant
default_pollutant = 'PM2.5'
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
    # Define function to plot map
    def plot_map_AP(column):
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
            range_color=(0, AP_data[selected_pollutant_col].max()),
            scope='europe',
            height=600,
            width=800
        )     
        # Update Layout
        fig.update_coloraxes(colorbar_title=selected_pollutant_col)
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(
                projection_scale=1.7,  # Adjust this value to zoom in or out
                center=dict(lat=55, lon=10)  # Center on mainland Europe
            ),
            updatemenus=[{
                'x': 0.1,
                'xanchor': 'right',
                'y': 0.1,
                'yanchor': 'top'
            }],
            sliders=[{
                'steps': [{
                    'args': [[frame.name], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 300}}],
                    'label': frame.name,
                    'method': 'animate'
                } for frame in fig.frames],
                'active': len(fig.frames) - 1,  # Set the slider to the latest year
                'x': 0.1,
                'y': 0.1,
                'len': 0.9,
                'transition': {'duration': 300, 'easing': 'cubic-in-out'}
            }]            
        )
        fig.update_traces(z=fig.frames[-1].data[0].z, hovertemplate=fig.frames[-1].data[0].hovertemplate)
        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)
    # Plot map
    plot_map_AP(selected_pollutant_col)
    
elif selected_option_AP == ':blue[Table]':   # Dataframe with data
    all_countries_option = "All countries"
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + unique_countries_AP, default=all_countries_option, key='table_air_pol')
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

# Select External Costs data and rename columns
EC_data = External_costs.loc[:, ['countries', 
                                 'Year',
                                 'GHG: Territorial & Low scenario [Euro]',
                                 'GHG: Territorial & Central scenario [Euro]',
                                 'GHG: Territorial & High scenario [Euro]',
                                 'GHG: Residential & Low scenario [Euro]',
                                 'GHG: Residential & Central scenario [Euro]',
                                 'GHG: Residential & High scenario [Euro]',
                                 'GHG: Footprint & Low scenario [Euro]',
                                 'GHG: Footprint & Central scenario [Euro]',
                                 'GHG: Footprint & High scenario [Euro]',
                                 'Air Pollutants - VOLY [Euro]',
                                 'Air Pollutants - VSL [Euro]',
                                 'Heavy Metals (Total) [Euro]',
                                 'External costs (Territorial & Low GHG with VOLY) scenario [Euro]',
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
                                 '(Footprint & High GHG with VSL) scenario [%]'
                                ]]
EC_list = ['Territorial GHG emissions, Low carbon cost, VOLY valuation', 
           'Territorial GHG emissions, Low carbon cost, VSL valuation', 
           'Territorial GHG emissions, Central carbon cost, VOLY valuation', 
           'Territorial GHG emissions, Central carbon cost, VSL valuation', 
           'Territorial GHG emissions, High carbon cost, VOLY valuation', 
           'Territorial GHG emissions, High carbon cost, VSL valuation',
           'Residential GHG emissions, Low carbon cost, VOLY valuation', 
           'Residential GHG emissions, Low carbon cost, VSL valuation', 
           'Residential GHG emissions, Central carbon cost, VOLY valuation', 
           'Residential GHG emissions, Central carbon cost, VSL valuation', 
           'Residential GHG emissions, High carbon cost, VOLY valuation', 
           'Residential GHG emissions, High carbon cost, VSL valuation',
           'Footprint GHG emissions, Low carbon cost, VOLY valuation', 
           'Footprint GHG emissions, Low carbon cost, VSL valuation', 
           'Footprint GHG emissions, Central carbon cost, VOLY valuation', 
           'Footprint GHG emissions, Central carbon cost, VSL valuation', 
           'Footprint GHG emissions, High carbon cost, VOLY valuation', 
           'Footprint GHG emissions, High carbon cost, VSL valuation']
new_column_names = ['External costs ('+item+') [Euro]' for item in EC_list]+['External costs ('+item+') [% of GDP]' for item in EC_list]
EC_data = EC_data.rename(columns=dict(zip(EC_data.columns[14:], new_column_names)))
EC_data = EC_data.sort_values(by=['countries', 'Year'])

# Default scenarios
unique_countries_EC = unique_countries
default_country_EC = 'Switzerland'

# Depending on the selected option, display the corresponding content
if selected_option_EC == ':blue[Evolution of external costs]':  # Plot of the evolution of external cost by type of pollutant
    # Selection of country
    selected_country_EC = st.selectbox("Select a country:", unique_countries_EC, index=unique_countries_EC.index(default_country_EC), key='country_EC_selectbox')  
    # Create three columns for the selectboxes
    col1, col2, col3 = st.columns(3)
    with col1:
        ghg_report = st.selectbox("Select GHG reporting:", ['Territorial', 'Residential', 'Footprint'], index=0)
    with col2:
        carbon_cost = st.selectbox("Select cost of carbon:", ['Low', 'Central', 'High'], index=1)
    with col3:
        valuation_method = st.selectbox("Select valuation method:", ['VSL', 'VOLY'], index=0)
    # Define function to plot external costs
    def plot_area_chart(country, ghg_report, carbon_cost, valuation_method):
        # Construct column names based on selected options
        ghg_column = f"GHG: {ghg_report} & {carbon_cost} scenario [Euro]"
        airpol_column = f"Air Pollutants - {valuation_method} [Euro]"        
        # Select columns according to scenario
        AreaChart = EC_data.loc[(EC_data["countries"] == country), 
                                ["Year", ghg_column, airpol_column, 'Heavy Metals (Total) [Euro]']]        
        # Rename columns
        AreaChart = AreaChart.rename(columns={
            ghg_column: 'GHG',
            airpol_column: 'Air Pollutants',
            'Heavy Metals (Total) [Euro]': 'Heavy Metals'
        })
        # Find the first year with data for GHG emissions
        first_year = AreaChart.dropna(subset=['GHG']).iloc[0]['Year']
        # Melt the dataframe for Plotly Express
        AreaChart_melted = AreaChart.melt(id_vars='Year', 
                                          value_vars=['GHG', 'Air Pollutants', 'Heavy Metals'], 
                                          var_name='Pollutant', 
                                          value_name='Cost')        
        # Create the stacked area chart
        fig = px.area(AreaChart_melted, x='Year', y='Cost', color='Pollutant', 
                      labels={'Cost': 'External Costs [Euro]', 'Year': 'Year'},
                      title=f"Evolution of external costs per group of pollutants in {country}, in Euros")        
        # Update layout 
        fig.update_layout(legend=dict(title='Pollutant'),
                          xaxis=dict(title='Year', range=[first_year, AreaChart['Year'].max()]),
                          yaxis=dict(title='External Costs [Euro]', rangemode='tozero'))        
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
    # Plot the stacked area chart based on the selected options
    plot_area_chart(selected_country_EC, ghg_report, carbon_cost, valuation_method)
    
elif selected_option_EC == ':blue[Map]':  # Map of European countries
    # Selection of metric
    selected_metric = st.selectbox("Select metric:", ['% of GDP', 'Euro'], key="radio_metric_EC")
    # Selection of GHG reporting, Carbon cost, and Valuation method
    col1, col2, col3 = st.columns(3)
    with col1:
        ghg_report = st.selectbox("Select GHG reporting:", ['Territorial', 'Residential', 'Footprint'], index=0, key="map_ghg_report")
    with col2:
        carbon_cost = st.selectbox("Select cost of carbon:", ['Low', 'Central', 'High'], index=1, key="map_carbon_cost")
    with col3:
        valuation_method = st.selectbox("Select valuation method:", ['VSL', 'VOLY'], index=0, key="map_valuation_method")
    # Construct the scenario string based on the selected options
    selected_scenario_EC = f'{ghg_report} GHG emissions, {carbon_cost} carbon cost, {valuation_method} valuation'
    if selected_metric == 'Euro':
        selected_scenario_col_EC = 'External costs (' + selected_scenario_EC + ') [Euro]'
        title_EC = 'External costs<br>[Euro]'
    else:
        selected_scenario_col_EC = 'External costs (' + selected_scenario_EC + ') [% of GDP]'
        title_EC = 'External costs<br>[% of GDP]'
    # Define function to plot map
    def plot_map_EC(column):
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
        # Update Layout
        fig.update_coloraxes(colorbar_title=title_EC)
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(
                projection_scale=1.7,  # Adjust this value to zoom in or out
                center=dict(lat=55, lon=10)  # Center on mainland Europe
            ),
            updatemenus=[{
                'x': 0.1,
                'xanchor': 'right',
                'y': 0.1,
                'yanchor': 'top'
            }],
            sliders=[{
                'steps': [{
                    'args': [[frame.name], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 300}}],
                    'label': frame.name,
                    'method': 'animate'
                } for frame in fig.frames],
                'active': len(fig.frames) - 1,  # Set the slider to the latest year
                'x': 0.1,
                'y': 0.1,
                'len': 0.9,
                'transition': {'duration': 300, 'easing': 'cubic-in-out'}
            }]            
        )
        fig.update_traces(z=fig.frames[-1].data[0].z, hovertemplate=fig.frames[-1].data[0].hovertemplate)
        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)       
    # Plot the map
    plot_map_EC(selected_scenario_col_EC)
    
elif selected_option_EC == ':blue[Table]':  # Dataframe with data
    all_countries_option = "All countries"
    selected_countries = st.multiselect("Select countries:", [all_countries_option] + unique_countries_EC, default=all_countries_option, key='table_EC')
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
The GrDP is defined as the GDP minus the external costs associated with economic activities:
$$
\mathrm{GrDP} = \mathrm{GDP} - \mathrm{External \; Costs} 
$$
""")

st.write("""
This interactive chart illustrates the evolution of GrDP and GDP in European countries, based on the various reporting methods and externalities pricing techniques introduced earlier.
""")

options_GrDP = [':blue[Evolution of GDP and GrDP]', ':blue[Map]', ':blue[Table]']
selected_option_GrDP = st.radio("Select display option:", options_GrDP, key="radio_grdp")

# Select GrDP and GDP data 
GrDP_data = GrDP.loc[:, ['countries', 'Year', 'GDP [Euro]', 'GDP per capita [Euro]',
                         'GrDP (Territorial & Low GHG with VOLY) scenario [Euro]',
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
                         'GrDP (Footprint & High GHG with VSL) scenario [Euro]', 
                         'GrDP per capita (Territorial & Low GHG with VOLY) scenario [Euro]',
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
GrDP_data = GrDP_data.sort_values(by=['countries', 'Year'])

# Country list
unique_countries_GrDP = sorted(GrDP_data['countries'].unique())
default_country_GrDP = 'Switzerland'

# Depending on the selected option, display the corresponding content
if selected_option_GrDP == ':blue[Evolution of GDP and GrDP]':     # Plot of the evolution of GDP and GrDP
    # Selection of country
    selected_country_GrDP = st.selectbox("Select a country:", unique_countries_GrDP, index=unique_countries_GrDP.index(default_country_GrDP), key='country_GrDP_selectbox')
    # Option to select between 'Total' and 'Per capita'
    selected_metric = st.selectbox("Select metric:", ['Total', 'Per capita'], key="radio_metric_GrDP")
    # Select scenarios
    col1, col2, col3 = st.columns(3)
    with col1:
        ghg_report = st.selectbox("Select GHG reporting:", ['Territorial', 'Residential', 'Footprint'], index=0, key='ghg_GrDP_selectbox')
    with col2:
        carbon_cost = st.selectbox("Select cost of carbon:", ['Low', 'Central', 'High'], index=1, key='carbon-cost_GrDP_selectbox')
    with col3:
        valuation_method = st.selectbox("Select valuation method:", ['VSL', 'VOLY'], index=0, key='valuation_GrDP_selectbox')
    # Select data and define graph layout
    if selected_metric == 'Total':
        selected_GrDP_col = f'GrDP ({ghg_report} & {carbon_cost} GHG with {valuation_method}) scenario [Euro]'
        selected_GDP_col = 'GDP [Euro]'
        # Create layout
        layout_GrDP = go.Layout(
            title=f'GDP and GrDP ({ghg_report} emissions, {carbon_cost} carbon cost, {valuation_method} valuation) of {selected_country_GrDP}',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Euro', rangemode='tozero'),  # Fix minimum y-axis value at zero
            margin=dict(l=40, r=40, t=40, b=30))
    else:
        selected_GrDP_col = f'GrDP per capita ({ghg_report} & {carbon_cost} GHG with {valuation_method}) scenario [Euro]'
        selected_GDP_col = 'GDP per capita [Euro]'
        # Create layout
        layout_GrDP = go.Layout(
            title=f'GDP and GrDP per capita ({ghg_report} emissions, {carbon_cost} carbon cost, {valuation_method} valuation) of {selected_country_GrDP}',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Euro', rangemode='tozero'), 
            margin=dict(l=40, r=40, t=40, b=30)
        )       
    # Filter data based on selected country
    country_data_GrDP = GrDP_data.loc[GrDP_data['countries'] == selected_country_GrDP]
    # Create traces for different emissions
    traces_GrDP = [
        go.Scatter(x=country_data_GrDP['Year'], y=country_data_GrDP[selected_GDP_col], mode='lines', name='GDP'),
        go.Scatter(x=country_data_GrDP['Year'], y=country_data_GrDP[selected_GrDP_col], mode='lines', name='GrDP')
    ]
    # Plot graph
    st.plotly_chart({'data': traces_GrDP, 'layout': layout_GrDP}, use_container_width=True)
    
elif selected_option_GrDP == ':blue[Map]': # Map of European countries
    # Option to select between 'Total' and 'Per capita'
    selected_metric = st.selectbox("Select metric:", ['Total', 'Per capita'], index=1, key="radio_metric_GrDP")
    # Select scenarios
    col1, col2, col3 = st.columns(3)
    with col1:
        ghg_report = st.selectbox("Select GHG reporting:", ['Territorial', 'Residential', 'Footprint'], index=0, key='ghg_map-GrDP_selectbox')
    with col2:
        carbon_cost = st.selectbox("Select cost of carbon:", ['Low', 'Central', 'High'], index=1, key='carbon-cost_map-GrDP_selectbox')
    with col3:
        valuation_method = st.selectbox("Select valuation method:", ['VSL', 'VOLY'], index=0, key='valuation_map-GrDP_selectbox')
    # Select data and define graph layout    
    if selected_metric == 'Total':
        selected_GrDP_col = f'GrDP ({ghg_report} & {carbon_cost} GHG with {valuation_method}) scenario [Euro]'
        title_GrDP = 'GrDP [Euro]'
    else:
        selected_GrDP_col = f'GrDP per capita ({ghg_report} & {carbon_cost} GHG with {valuation_method}) scenario [Euro]'
        title_GrDP = 'GrDP per capita [Euro]'
    # Define function to plot map
    def plot_map_GrDP(column):
        # Create a custom color scale
        min_value = GrDP_data[column].min()
        max_value = GrDP_data[column].max()        
        if min_value < 0 and max_value > 0:
            zero_position = abs(min_value) / (max_value - min_value)
            custom_color_scale = [
                (0.0, "red"),    # most negative
                (zero_position, "white"),   # zero
                (1.0, "blue")    # most positive
            ]
        elif min_value >= 0:
            custom_color_scale = [
                (0.0, "white"),
                (1.0, "blue")
            ]
        else:
            custom_color_scale = [
                (0.0, "red"),
                (1.0, "white")
            ]       
        # Create map
        fig = px.choropleth(GrDP_data,
                            locations='countries',
                            locationmode='country names',
                            color=column,
                            hover_name='countries',
                            animation_frame='Year',
                            title="",
                            color_continuous_scale=custom_color_scale, #px.colors.sequential.Blues,
                            range_color=[GrDP_data[column].min(), GrDP_data[column].max()],
                            scope='europe',
                            height=600,
                            width=800)      
        # Update Layout
        fig.update_coloraxes(colorbar_title=title_GrDP)
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(
                projection_scale=1.7,  # Adjust this value to zoom in or out
                center=dict(lat=55, lon=10)  # Center on mainland Europe
            ),
            updatemenus=[{
                'x': 0.1,
                'xanchor': 'right',
                'y': 0.1,
                'yanchor': 'top'
            }],
            sliders=[{
                'steps': [{
                    'args': [[frame.name], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 300}}],
                    'label': frame.name,
                    'method': 'animate'
                } for frame in fig.frames],
                'active': len(fig.frames) - 1,  # Set the slider to the latest year
                'x': 0.1,
                'y': 0.1,
                'len': 0.9,
                'transition': {'duration': 300, 'easing': 'cubic-in-out'}
            }]            
        )
        fig.update_traces(z=fig.frames[-1].data[0].z, hovertemplate=fig.frames[-1].data[0].hovertemplate)
        # Display plotly chart
        st.plotly_chart(fig, use_container_width=True)
    # Plot map    
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

st.write('##### What is decoupling ?')

st.markdown("""
Decoupling refers to an economy that grows without increasing the pressure on the environment. We generally distinguish between absolute and relative decoupling:
- Absolute decoupling occurs when the pollution is decreasing while the economy is growing
- Relative decoupling occurs when the pollution is increasing at a slower rate than the economy

The following chart illustrates the decoupling between the emissions of various pollutants and economic growth (represented by GDP) or population, between 2011 and 2021. We use two indicators to evaluate decoupling: the OECD Decoupling Factor and the Intensity of Decoupling Factor.
""")

st.write('##### OECD Decoupling Factor')

st.write("""
The [OECD Decoupling Factor](https://one.oecd.org/document/sg/sd(2002)1/final/en/pdf) is the decrease rate of the ratio between the emissions of a given pollutant over the GDP (or population). More precisely, it is defined as:
""")
st.latex(r"D = 1- \frac{(\mathrm{Emissions/GDP})_{2021}}{(\mathrm{Emissions/GDP})_{2011}}")

st.markdown("""
The indicator can be interpreted as follows:
- **When D is negative, there is no decoupling**: when D<0, the ratio Emissions/GDP is greater in 2021 than in 2011, and thus the environmental pressure increased;
- **When D is positive, decoupling - relative or absolute - occurs**: when  D>0, the ratio Emissions/GDP decreased between 2011 and 2021. In the best case, D is equal to one, meaning that the emissions are zero in 2021.
""")

st.write('##### Intensity of Decoupling Factor')

st.markdown("""
The Intensity of Decoupling Factor compares the growth rate of the emissions of a given pollutant with the economic (or population) growth rate. With <span class="tooltip">$gE$ the growth rate of the emissions of a given pollutant<span class="tooltiptext">$gE=(E_{2021}-E_{2011})/E_{2011}$</span></span> 
and <span class="tooltip">$gGDP$ the economic growth rate<span class="tooltiptext">$gGDP=(GDP_{2021}-GDP_{2011})/GDP_{2011}$</span></span>, 
the Intensity of Decoupling Factor is defined as:
""", unsafe_allow_html=True)
st.latex(r"IF = - gE/gGDP")

st.markdown("""
This indicator allows to distinguish between relative and absolute decoupling. In a period of economic growth:
- **When IF< -1, there is no decoupling**: the growth rate of the emissions is greater than the economic growth rate;
- **When -1<IF<0, relative decoupling occurs**: the growth rate of the emissions is positive, but smaller than the economic growth rate;
- **When IF is positive, absolute decoupling occurs**: the emissions decreased between 2011 and 2021
""")

###########################################
###### Decoupling indicators charts #######
###########################################

options_Decoupling = [':blue[Country comparison]', ':blue[Table]']
selected_option_Decoupling = st.radio("Select display option:", options_Decoupling, key="radio_Decoupling")

# Select indicator
selected_indicator = st.selectbox("Select an indicator:", ['OECD Decoupling Factor', 'Intensity of Decoupling Factor'], index=0)

# Select data
if selected_indicator == 'OECD Decoupling Factor':
    Decoupling_OECD_data = Decoupling_OECD.loc[:, ['countries', 'Year', 
                                                       'Territorial GHG emissions_GDP',
                                                       'Residential GHG emissions_GDP', 
                                                       'Footprint GHG emissions_GDP', 
                                                       'Air Pollutants Emissions_GDP',
                                                       'PM2.5_GDP', 
                                                       'PM10_GDP',
                                                       'NOx_GDP',
                                                       'SOx_GDP', 
                                                       'NH3_GDP',  
                                                       'NMVOC_GDP',
                                                       'Heavy Metals Emissions_GDP',
                                                       'As_GDP', 
                                                       'Pb_GDP', 
                                                       'Cd_GDP', 
                                                       'Hg_GDP', 
                                                       'Cr_GDP', 
                                                       'Ni_GDP', 
                                                       'Territorial GHG emissions_Population',
                                                       'Residential GHG emissions_Population',
                                                       'Footprint GHG emissions_Population',
                                                       'Air Pollutants Emissions_Population',
                                                       'PM2.5_Population',
                                                       'PM10_Population',
                                                       'NOx_Population',
                                                       'SOx_Population',
                                                       'NH3_Population',
                                                       'NMVOC_Population',
                                                       'Heavy Metals Emissions_Population',
                                                       'As_Population',
                                                       'Pb_Population',
                                                       'Cd_Population',
                                                       'Hg_Population',
                                                       'Cr_Population',
                                                       'Ni_Population'
                                                      ]]
    Decoupling_OECD_data = Decoupling_OECD_data.sort_values(by=['countries', 'Year'])
elif selected_indicator == 'Intensity of Decoupling Factor':
    Decoupling_IF_data = Decoupling_Intensity_Factor.loc[:, ['countries', 'Year', 
                                                             'Territorial GHG emissions_GDP',
                                                             'Residential GHG emissions_GDP', 
                                                             'Footprint GHG emissions_GDP', 
                                                             'Air Pollutants Emissions_GDP',
                                                             'PM2.5_GDP', 
                                                             'PM10_GDP',
                                                             'NOx_GDP',
                                                             'SOx_GDP', 
                                                             'NH3_GDP',
                                                             'NMVOC_GDP',
                                                             'Heavy Metals Emissions_GDP',
                                                             'As_GDP', 
                                                             'Pb_GDP',
                                                             'Cd_GDP', 
                                                             'Hg_GDP', 
                                                             'Cr_GDP', 
                                                             'Ni_GDP',
                                                             'Territorial GHG emissions_Population',
                                                             'Residential GHG emissions_Population',
                                                             'Footprint GHG emissions_Population',
                                                             'Air Pollutants Emissions_Population',
                                                             'PM2.5_Population',
                                                             'PM10_Population',
                                                             'NOx_Population',
                                                             'SOx_Population',
                                                             'NH3_Population',
                                                             'NMVOC_Population',
                                                             'Heavy Metals Emissions_Population',
                                                             'As_Population',
                                                             'Pb_Population',
                                                             'Cd_Population',
                                                             'Hg_Population',
                                                             'Cr_Population',
                                                             'Ni_Population'
                                                            ]]
    Decoupling_IF_data = Decoupling_IF_data.sort_values(by=['countries', 'Year'])    

# List of pollutants
Emissions_list = ['Territorial GHG emissions',
                      'Residential GHG emissions',
                      'Footprint GHG emissions',
                      'Air Pollutants Emissions', 
                      'PM2.5', 'PM10','NOx', 
                      'SOx', 'NH3', 'NMVOC',
                      'Heavy Metals Emissions',
                      'As', 'Pb', 'Cd', 
                      'Hg', 'Cr', 'Ni'
                     ]    
default_emission_decoupling = 'Territorial GHG emissions'    
    
if selected_option_Decoupling == ':blue[Country comparison]':
    # Select indicator
    col1, col2 = st.columns(2)
    with col1:
        selected_emission_decoupling = st.selectbox("Select a pollutant:", Emissions_list, index=Emissions_list.index(default_emission_decoupling))
    with col2:
        selected_metric = st.selectbox("Select quantity:", ['GDP', 'Population'], key="dropdown_quantity_decoupling")
    selected_Decoupling_col = selected_emission_decoupling + '_' + selected_metric
    # Filter data based on selected indicator and emission type
    if selected_indicator == 'OECD Decoupling Factor':
        data_decoupling = Decoupling_OECD_data.loc[
            Decoupling_OECD_data['Year'] == 2021, ['countries', selected_Decoupling_col]
        ]
    elif selected_indicator == 'Intensity of Decoupling Factor':
        data_decoupling = Decoupling_IF_data.loc[
            Decoupling_IF_data['Year'] == 2021, ['countries', selected_Decoupling_col]
        ]
    # Sort the data by the selected decoupling column in descending order
    data_decoupling = data_decoupling.sort_values(by=selected_Decoupling_col, ascending=True)
    # Create traces for different emissions
    Bar_plot_decoupling = [
        go.Bar(x=data_decoupling[selected_Decoupling_col], y=data_decoupling['countries'], name=selected_emission_decoupling, orientation='h')
    ]
    # Create layout
    layout_decoupling = go.Layout(
        title=f'{selected_indicator} of {selected_emission_decoupling} with {selected_metric} between 2011 and 2021',
        xaxis_title=f'{selected_indicator} of {selected_emission_decoupling} with {selected_metric}',
        yaxis_title='Country',
        xaxis=dict(rangemode='tozero'),  # Fix minimum x-axis value at zero
        margin=dict(l=50, r=40, t=40, b=50),  # Increase left and bottom margins
        height=600,  # Set a fixed height for the plot
        yaxis=dict(automargin=True)  # Automatically adjust margins to fit labels
    )
    # Plot graph
    st.plotly_chart({'data': Bar_plot_decoupling, 'layout': layout_decoupling}, use_container_width=True)

elif selected_option_Decoupling == ':blue[Table]': 
    all_countries_option = "All countries"
    if selected_indicator == 'OECD Decoupling Factor':
        unique_countries_OECD = sorted(Decoupling_OECD_data['countries'].unique())
        selected_countries = st.multiselect("Select countries:", [all_countries_option] + list(unique_countries_OECD), default=all_countries_option, key='Table_OECD')
        if all_countries_option in selected_countries:
            filtered_data = Decoupling_OECD_data.copy()  # Make a copy of the original DataFrame
        else:
            filtered_data = Decoupling_OECD_data[Decoupling_OECD_data['countries'].isin(selected_countries)]
        st.write(filtered_data)
    elif selected_indicator == 'Intensity of Decoupling Factor':
        unique_countries_IF = sorted(Decoupling_IF_data['countries'].unique())
        selected_countries = st.multiselect("Select countries:", [all_countries_option] + list(unique_countries_IF), default=all_countries_option, key='Table_IF')
        if all_countries_option in selected_countries:
            filtered_data = Decoupling_IF_data.copy()  # Make a copy of the original DataFrame
        else:
            filtered_data = Decoupling_IF_data[Decoupling_IF_data['countries'].isin(selected_countries)]
        st.write(filtered_data)

    
#################################################################
######### Decoupling: Scatter Plot of growth rates ##############
#################################################################

st.markdown("""
To further explore the various degrees of decoupling, the following chart plots the growth rate of emissions with respect to the growth rate of GDP (or population), between 2011 and 2021, for European countries.
Authors from the literature, e.g., <span class="tooltip">Vehmas et al. (2003)<span class="tooltiptext">Vehmas, J., Malaska, P., et al. (2003). Europe in the global battle of sustainability: Rebound strikes back? Advanced Sustainability Analysis. Publications of the Turku School of Economics and Business Administration, series discussion and working papers, 7, 2003.</span></span> and [Tapio (2005)](https://www.sciencedirect.com/science/article/pii/S0967070X05000028) constructed a framework to distinguish different aspects of decoupling: 
- Coupling occurs when emissions and GDP grow at a similar rate. More specifically, there is less than 20% variation between the emissions and GDP growth rates (0.8<gE/gDP<1.2). We differentiate:
    - **Expansive Coupling**: Emissions and GDP increase at a similar rate;
    - **Recessive Coupling**: Emissions and GDP decrease at a similar rate;
- Decoupling occurs when emissions grow at a significantly slower rate than GDP:
    - **Strong Decoupling**: Emissions decrease (gE<0) and GDP increases (gGDP>0), i.e., absolute decoupling occurs;
    - **Weak Decoupling**: Emissions and GDP both increase, but the rise in emissions is significantly smaller than the GDP growth (gE>0, gGDP>0, gE/gGDP<0.8). This is a case of relative decoupling;
    - **Recessive Decoupling**: Emissions and GDP both decrease, but the reduction in emissions is significantly greater than the economic contraction (gE<0, gGDP<0, gE/gGDP>1.2);
- Finally, the worst case scenario is negative decoupling, when emissions grow at a significantly faster rate than GDP:
    - **Expansive Negative Decoupling**: Emissions and GDP both increase, but emissions grow at a signigicantly faster rate than GDP (gE>0, gGDP>0, gE/gGDP>1.2);
    - **Strong Negative Decoupling**: Emissions increase although GDP decreases (gE>0, gGDP<0;
    - **Weak Negative Decoupling**: Emissions and GDP both decrease, but the reduction in emissions is significantly smaller than the economic contraction (gE<0, gGDP<0, gE/gGDP<0.8).
""", unsafe_allow_html=True)

# Define color for each decoupling category
color_mapping = {
    'darkmagenta': 'Expansive coupling',            # Deep Magenta
    'deeppink': 'Recessive coupling',               # Gold
    'darkgreen': 'Strong decoupling',               # Dark Green
    'royalblue': 'Weak decoupling',                 # Royal Blue 
    'darkviolet': 'Recessive decoupling',           # Dark Violet
    'darkorange': 'Expansive negative decoupling',  # Dark orange
    'darkred': 'Strong negative decoupling',        # Dark Red 
    'gold': 'Weak negative decoupling',             # Dark Pink 
    'grey': 'Zero emissions in 2011'                # Grey
}
df_color_mapping = pd.DataFrame(list(color_mapping.items()), columns=['Color', 'Category']) # Convert the dictionary to a DataFrame
category_to_color = df_color_mapping.set_index('Category')['Color'].to_dict()   # Create a reverse mapping from category to color for easy lookup
# Function to apply color to data
def get_color(row, metric_col):
    if row[metric_col] > 0 and row[selected_RelDif_col] > 0:
        if row[selected_RelDif_col] / row[metric_col] > 1.2:
            return category_to_color['Expansive negative decoupling']
        elif row[selected_RelDif_col] / row[metric_col] < 0.8:
            return category_to_color['Weak decoupling']
        else:
            return category_to_color['Expansive coupling']
    elif row[metric_col] > 0 and row[selected_RelDif_col] < 0:
        return category_to_color['Strong decoupling']
    elif row[metric_col] < 0 and row[selected_RelDif_col] < 0:
        if row[selected_RelDif_col] / row[metric_col] > 1.2:
            return category_to_color['Recessive decoupling']
        elif row[selected_RelDif_col] / row[metric_col] < 0.8:
            return category_to_color['Weak negative decoupling']
        else:
            return category_to_color['Recessive coupling']
    elif row[metric_col] < 0 and row[selected_RelDif_col] > 0:
        return category_to_color['Strong negative decoupling']
    else:
        return category_to_color['Zero emissions in 2011']

# Select chart
options_RelDif = [':blue[Scatter plot]', ':blue[Table]']
selected_option_RelDif = st.radio("Select display option:", options_RelDif, key="radio_RelDif")

# Select data
RelDif_data = Decoupling_Relative_Difference.loc[:, [
    'countries', 'Year', 
    'Territorial GHG emissions',
    'Residential GHG emissions',
    'Footprint GHG emissions',
    'Air Pollutants Emissions',
    'PM2.5', 'PM10', 'NOx',
    'SOx', 'NH3', 'NMVOC',
    'Heavy Metals Emissions',
    'As', 'Pb', 'Cd', 
    'Hg', 'Cr', 'Ni', 
    'GDP', 'Population'
    ]]
RelDif_data = RelDif_data.sort_values(by=['countries', 'Year'])
RelDif_data.loc[:, ~RelDif_data.columns.isin(['countries', 'Year'])] *= 100   # Multiply all values by 100 to obtain percentages

# Emissions list
Emissions_list = [
    'Territorial GHG emissions', 
    'Residential GHG emissions',
    'Footprint GHG emissions',
    'Air Pollutants Emissions',
    'PM2.5', 'PM10', 'NOx',
    'SOx', 'NH3', 'NMVOC',
    'Heavy Metals Emissions', 
    'As', 'Pb', 'Cd', 
    'Hg', 'Cr', 'Ni'
    ]
default_emission_RelDif = 'Territorial GHG emissions'

# Depending on the selected option, display the corresponding content
if selected_option_RelDif == ':blue[Scatter plot]':
    # Select indicator
    col1, col2 = st.columns(2)
    with col1:
        selected_emission_RelDif = st.selectbox("Select a pollutant:", Emissions_list, index=Emissions_list.index(default_emission_RelDif), key="emission_rel_diff_selectbox")
    with col2:
        selected_metric = st.selectbox("Select quantity:", ['GDP', 'Population'], key="dropdown_quantity_RelDif")
    selected_RelDif_col = selected_emission_RelDif   
    # Filter data based on selected emission type
    data_rel_dif = RelDif_data.loc[RelDif_data['Year'] == 2021, ['countries', 'GDP', 'Population', selected_RelDif_col]]
    data_rel_dif['color'] = data_rel_dif.apply(lambda row: get_color(row, selected_metric), axis=1)
    unique_colors = data_rel_dif['color'].unique()
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
    # Create layout with quadrant lines
    x_min = min(data_rel_dif[selected_metric])
    x_max = max(data_rel_dif[selected_metric])
    y_min = min(data_rel_dif[selected_RelDif_col])
    y_max = max(data_rel_dif[selected_RelDif_col])
    xy_max = max(x_max, y_max)+10
    xy_min = min(x_min, y_min)-10
    layout_RelDif = go.Layout(
        title=f'Growth of {selected_emission_RelDif} and {selected_metric} between 2011 and 2021 per Country',
        xaxis=dict(title=f'Growth of {selected_metric} [%]', range=[xy_min, xy_max]),  
        yaxis=dict(title=f'Growth of {selected_emission_RelDif} [%]', range=[xy_min, xy_max]),  
        shapes=[
            # Line for x-axis (horizontal)
            dict(
                type='line',
                x0=xy_min,
                y0=0,
                x1=xy_max,
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
                y0=xy_min,
                x1=0,
                y1=xy_max,
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

    
#######################################
######### Final section ##############
######################################

    
 # Define the final markdown message with custom CSS for styling
final_markdown = """
<hr style="border: none; border-top: 1px solid white; margin-top: 30px; margin-bottom: 30px;" />

<div style="background-color: #444444; padding: 20px; border-radius: 10px;">
<p style="color: powderblue; font-size: 16px;">
<strong>Article written by <a href="https://e4s.center/about-e4s/people/boris-thurm/" style="color: lightblue;">Boris Thurm</a> and Antoine Trabia</strong>
</p>
<p style="color: powderblue; font-size: 14px;">
You are free to download, modify, and share the visualizations and data behind this work in any medium, provided the original data sources and authors are credited. This article can be cited as: 
</p>
<p style="color: powderblue; font-size: 14px;">
"Boris Thurm and Antoine Trabia (2024) - Going beyond the GDP with the GrDP: Factoring health and environmental costs in economic success. Retrieved from: 'https://green-dp.streamlit.app/' [Online Resource]"
</p>
<p style="color: powderblue; font-size: 14px;">
For any inquiry or suggestions, please contact Boris Thurm at <a href="mailto:boris.thurm@epfl.ch" style="color: lightblue;">boris.thurm@epfl.ch</a>.
</p>
</div>
"""
st.markdown(final_markdown, unsafe_allow_html=True)   