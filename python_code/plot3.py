import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import Map
import contextily as ctx
from bokeh.io import output_file, save
from bokeh.palettes import Category20
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh import layouts
from datetime import datetime
from folium.plugins import HeatMapWithTime
from bokeh.palettes import brewer
from bokeh.plotting import figure, show
from bokeh.layouts import column


# Set global plot styles
plt.style.use('seaborn-v0_8')
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.family'] = 'sans-serif'

# Define focus crime categories
focuscrimes = ['WEAPON LAWS', 'PROSTITUTION', 'ROBBERY', 'BURGLARY', 'ASSAULT', 'DRUG/NARCOTIC', 'LARCENY/THEFT', 'VANDALISM', 'VEHICLE THEFT', 'STOLEN PROPERTY']
focuscrime = 'VEHICLE THEFT'
# Load and preprocess data
IRH_first = pd.read_csv('python_code/data/Police_Department_Incident_Reports__Historical_2003_to_May_2018.csv')
IRH_second = pd.read_csv('python_code/data/Police_Department_Incident_Reports__2018_to_Present_20250204.csv')

IRH_first = IRH_first[['Category', 'DayOfWeek', 'Date', 'Time', 'PdDistrict', 'location', 'X', 'Y']]
IRH_second = IRH_second[['Incident Category', 'Incident Day of Week', 'Incident Date', 'Incident Time', 'Police District', 'Point', 'Longitude', 'Latitude']]

merged_column_names = ['Category', 'DayOfWeek', 'Date', 'Time', 'District', 'PointLocation', 'Longitude', 'Latitude']
IRH_first.columns = merged_column_names
IRH_second.columns = merged_column_names

IRH_first['Category'] = IRH_first['Category'].str.upper()
IRH_first['District'] = IRH_first['District'].str.upper()
IRH_second['Category'] = IRH_second['Category'].str.upper()
IRH_second['District'] = IRH_second['District'].str.upper()

IRH_first['Date'] = pd.to_datetime(IRH_first['Date'])
IRH_second['Date'] = pd.to_datetime(IRH_second['Date'])
IRH_second = IRH_second[IRH_second['Date'] > pd.to_datetime('2018-05-15')]

category_mapping = {
    'LARCENY THEFT': 'LARCENY/THEFT', 'LARCENY/THEFT': 'LARCENY/THEFT', 'BURGLARY': 'BURGLARY',
    'MOTOR VEHICLE THEFT': 'VEHICLE THEFT', 'MOTOR VEHICLE THEFT?': 'VEHICLE THEFT', 'VEHICLE THEFT': 'VEHICLE THEFT',
    'DRUG OFFENSE': 'DRUG/NARCOTIC', 'DRUG VIOLATION': 'DRUG/NARCOTIC', 'DRUG/NARCOTIC': 'DRUG/NARCOTIC',
    'FORGERY AND COUNTERFEITING': 'FORGERY/COUNTERFEITING', 'FORGERY/COUNTERFEITING': 'FORGERY/COUNTERFEITING',
    'SEX OFFENSES, FORCIBLE': 'SEX OFFENSE', 'SEX OFFENSES, NON FORCIBLE': 'SEX OFFENSE', 'SEX OFFENSE': 'SEX OFFENSE',
    'WEAPON LAWS': 'WEAPON LAWS', 'WEAPONS CARRYING ETC': 'WEAPON LAWS', 'WEAPONS OFFENCE': 'WEAPON LAWS', 'WEAPONS OFFENSE': 'WEAPON LAWS',
    'WARRANT': 'WARRANTS', 'WARRANTS': 'WARRANTS', 'OTHER': 'OTHER', 'OTHER MISCELLANEOUS': 'OTHER', 'OTHER OFFENSES': 'OTHER',
    'HUMAN TRAFFICKING, COMMERCIAL SEX ACTS': 'HUMAN TRAFFICKING (A), COMMERCIAL SEX ACTS',
    'SUSPICIOUS': 'SUSPICIOUS OCC', 'MALICIOUS MISCHIEF': 'VANDALISM'
}
IRH_first['Category'] = IRH_first['Category'].replace(category_mapping)
IRH_second['Category'] = IRH_second['Category'].replace(category_mapping)

IRH_all = pd.concat([IRH_first, IRH_second])
IRH_all = IRH_all[(IRH_all['Date'] >= pd.to_datetime('2003-01-01')) & (IRH_all['Date'] <= pd.to_datetime('2024-12-31'))]

IRH_all['Year'] = IRH_all['Date'].dt.year
IRH_all['Month'] = IRH_all['Date'].dt.month
IRH_all['Day'] = IRH_all['Date'].dt.day
IRH_all['Hours'] = IRH_all['Time'].str[:2].astype(int)

# Create a more focused and clean visualization of crime trends
# Focus on the key crime categories from the focuscrimes list

# Set global plot styles
#plt.style.use('dark_background')
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (15, 20)
plt.rcParams['font.family'] = 'sans-serif'

data = IRH_all[IRH_all['Category'] == focuscrime]

# Aggregate the data: Count the number of crimes per district per year
crime_counts = data.groupby(['Year', 'District']).size().unstack(fill_value=0)

# Convert the aggregated data into a ColumnDataSource for Bokeh
source = ColumnDataSource(crime_counts)
# Create a figure for the stacked area chart
p = figure(title="Vehicle Theft by District over Time", x_axis_label='Year', y_axis_label='Crime Count', 
           x_range=(crime_counts.index.min(), crime_counts.index.max()), height=400)

# Create the list of stackers (columns representing different districts)
names = crime_counts.columns.tolist()

# Plot the stacked areas using varea_stack
p.varea_stack(stackers=names, x='Year', color=Category20[len(names)], legend_label=names, source=source, muted_alpha=0.2, alpha=0.7)

# Add hover tool to show information about each year and district
hover = HoverTool()
hover.tooltips = [("Year", "@Year"), ("District", "$name"), ("Crime Count", "@$name")]
p.add_tools(hover)

# Add a select widget to allow the user to pick a district
p.legend.click_policy="mute" ### assigns the click policy (you can try to use ''hide'
p.legend.location = "center"

########################################################
# This line puts the legend outside of the plot area

p.add_layout(p.legend[0], 'left')

# Show the plot
output_file("./assets/plots/sf_crime_interactive_bokeh.html")
show(p)