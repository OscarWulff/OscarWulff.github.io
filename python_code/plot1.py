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
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['font.family'] = 'sans-serif'

data = IRH_all[IRH_all['Category'] == focuscrime]
category_data_hourly = pd.DataFrame(data.groupby(['Hours'])['Hours'].count()).rename(columns={'Hours':'Count'}).reset_index()

N = len(category_data_hourly)
theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
radii = category_data_hourly['Count']
width = 2 * np.pi / N

# Plot the polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
fig.patch.set_facecolor('#262626')  # Set figure background
ax.set_facecolor('#262626')  # Set axes background

bars = ax.bar(
    theta, radii, width=width, 
    color=plt.cm.Blues(radii / max(radii)),  # Gradient based on frequency
    edgecolor='black', alpha=0.75, linewidth=1.2
)

# Formatting
#ax.set_title(f"Vechicle Theft", fontsize=14, pad=40)
ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))  # Reduce tick clutter
ax.set_xticklabels([f'{x}:00' for x in range(0,24,1)], fontsize=10, color='white')
ax.set_theta_offset(np.pi / 2)  # Offset the starting angle by 90 degrees
ax.set_theta_direction(-1)  # Clockwise direction

ax.tick_params(axis='y', labelsize=8, labelcolor='white')  # Make labels smaller and grey
ax.set_rlabel_position(88)
ax.set_ylabel("Number of Crimes", rotation=0, color='white', fontsize=12)
ax.yaxis.set_label_coords(0.8, 0.47)

ax.yaxis.grid(color='lightgrey', linestyle='--', linewidth=0.5, alpha=0.5)

fig.suptitle("Occurrences of Vechicle Theft per hour", fontsize=16, fontweight='bold', color='white')
# Save the figure
plt.savefig('assets/images/improved_crime_trends.png', dpi=300, bbox_inches='tight')
plt.close()
