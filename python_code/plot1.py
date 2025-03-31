import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import Map
import contextily as ctx
from bokeh.io import output_file, save
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh import layouts
from datetime import datetime
from folium.plugins import HeatMapWithTime

# Set global plot styles to light mode
plt.style.use('seaborn-v0_8-white')  # Light background style
sns.set_style("whitegrid")  # White background with grid lines
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.facecolor'] = 'white'  # White axes background
plt.rcParams['figure.facecolor'] = 'white'  # White figure background

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

# Set plot size and style for polar plot
plt.rcParams['figure.figsize'] = (10, 10)

data = IRH_all[IRH_all['Category'] == focuscrime]
category_data_hourly = pd.DataFrame(data.groupby(['Hours'])['Hours'].count()).rename(columns={'Hours':'Count'}).reset_index()

N = len(category_data_hourly)
theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
radii = category_data_hourly['Count']
width = 2 * np.pi / N

# Create polar plot with light mode styling
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
fig.patch.set_facecolor('white')  # White figure background
ax.set_facecolor('white')  # White axes background

# Plot bars with solid blue color (like original but with light mode compatibility)
bars = ax.bar(
    theta, radii, width=width, 
    color='#1f77b4',  # Standard matplotlib blue
    edgecolor='black',  # Black edges for definition
    alpha=0.75,  # Slight transparency
    linewidth=1.2  # Edge line width
)

# Formatting (same structure as original but with dark text)
ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
ax.set_xticklabels([f'{x}:00' for x in range(0,24,1)], fontsize=10, color='black')
ax.set_theta_offset(np.pi / 2)  # Offset starting angle
ax.set_theta_direction(-1)  # Clockwise direction

# Axis labels and ticks (black for light mode)
ax.tick_params(axis='y', labelsize=8, labelcolor='black')
ax.set_rlabel_position(88)
ax.set_ylabel("Number of Crimes", rotation=0, color='black', fontsize=12)
ax.yaxis.set_label_coords(0.8, 0.47)

# Grid lines (visible but subtle)
ax.yaxis.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax.xaxis.grid(color='lightgray', linestyle='-', linewidth=0.5, alpha=0.3)

# Title (black for light mode)
fig.suptitle("Occurrences of Vehicle Theft per hour", 
             fontsize=16, fontweight='bold', color='black')

# Save with white background
plt.savefig('assets/images/improved_crime_trends_light.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()