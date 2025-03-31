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

# Create a more focused and clean visualization of crime trends
# Focus on the key crime categories from the focuscrimes list

# Get the data for the focus crime categories
focus_crimes_data = IRH_all[IRH_all['Category'].isin(focuscrimes)]

# Create a DataFrame with yearly counts for each focus crime category
yearly_focus_crimes = focus_crimes_data.groupby(['Year', 'Category']).size().reset_index(name='Count')

# Get total crime count per year for normalization
total_yearly_crimes = IRH_all.groupby('Year').size().reset_index(name='Total')
yearly_focus_crimes = yearly_focus_crimes.merge(total_yearly_crimes, on='Year')
yearly_focus_crimes['Percentage'] = (yearly_focus_crimes['Count'] / yearly_focus_crimes['Total'] * 100).round(2)

# Create a figure with subplots - one for each crime category
fig = plt.figure(figsize=(14, 3.5*len(focuscrimes)))  # Increased height per subplot
gs = fig.add_gridspec(len(focuscrimes), 1, hspace=0.6)  # Increased spacing between subplots
axes = [fig.add_subplot(gs[i]) for i in range(len(focuscrimes))]

# Add main title with increased spacing
fig.suptitle('Trends in Key Crime Categories in San Francisco (2003-2024)', 
             fontsize=20, y=0.95)  # Increased y position

# Define a custom color palette
colors = plt.cm.viridis(np.linspace(0, 1, len(focuscrimes)))

# Create line plots for each crime category
for i, crime in enumerate(focuscrimes):
    crime_data = yearly_focus_crimes[yearly_focus_crimes['Category'] == crime]
    
    ax = axes[i]
    line = ax.plot(crime_data['Year'], crime_data['Count'], marker='o', linewidth=2.5, 
             color=colors[i], label=f'Total Incidents')
    
    ax.fill_between(crime_data['Year'], crime_data['Count'], alpha=0.2, color=colors[i])
    
    # Add percentage line on secondary axis
    ax2 = ax.twinx()
    percent_line = ax2.plot(crime_data['Year'], crime_data['Percentage'], marker='s', 
                      linewidth=1.5, linestyle='--', color='#FF5733', 
                      label='% of All Crimes')
    
    # Set y-axis labels and colors
    ax.set_ylabel('Incidents', fontsize=11)
    ax2.set_ylabel('% of All Crimes', color='#FF5733', fontsize=11)
    ax2.tick_params(axis='y', colors='#FF5733')
    ax2.set_ylim(bottom=0)
    
    # Combine legends
    lines = line + percent_line
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='upper right', fontsize=9, bbox_to_anchor=(1, 1))
    
    # Add title
    ax.set_title(f'{crime}', fontsize=14, pad=15)  # Increased padding
    ax.grid(True, alpha=0.3)
    
    # Find and annotate peaks and valleys
    # Find and annotate peaks and valleys
    if len(crime_data) > 5:
        peak_year = crime_data.loc[crime_data['Count'].idxmax()]
        valley_year = crime_data.loc[crime_data['Count'].idxmin()]
        
        # Add peak annotation with adjusted position - special case for STOLEN PROPERTY
        if crime == 'STOLEN PROPERTY':
            ax.annotate(f"High: {int(peak_year['Count'])}",
                       xy=(peak_year['Year'], peak_year['Count']),
                       xytext=(15, -25),  # Changed to point downward
                       textcoords="offset points",
                       fontsize=9,
                       ha='left',
                       arrowprops=dict(arrowstyle="->", color='black', alpha=0.6, 
                                     connectionstyle="arc3,rad=-0.2"),  # Changed arc direction
                       bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))
        else:
            ax.annotate(f"High: {int(peak_year['Count'])}",
                       xy=(peak_year['Year'], peak_year['Count']),
                       xytext=(15, 25),
                       textcoords="offset points",
                       fontsize=9,
                       ha='left',
                       arrowprops=dict(arrowstyle="->", color='black', alpha=0.6, 
                                     connectionstyle="arc3,rad=0.2"),
                       bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))
        
        # Valley annotation remains the same
        ax.annotate(f"Low: {int(valley_year['Count'])}",
                   xy=(valley_year['Year'], valley_year['Count']),
                   xytext=(-15, -25),
                   textcoords="offset points",
                   fontsize=9,
                   ha='right',
                   arrowprops=dict(arrowstyle="->", color='black', alpha=0.6, 
                                 connectionstyle="arc3,rad=-0.2"),
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7))

# Set x-axis ticks and labels
for ax in axes:
    ax.set_xticks(sorted(yearly_focus_crimes['Year'].unique())[::2])
    ax.set_xlabel("")

# Add common x-axis label
fig.text(0.5, 0.02, 'Year', ha='center', fontsize=14)

# Adjust layout
plt.tight_layout()
fig.subplots_adjust(top=0.92)  # Adjust top margin

# Save the figure
plt.savefig('improved_crime_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# Focus specifically on stolen property data instead of vehicle theft
stolen_property_data = IRH_all[IRH_all['Category'] == 'STOLEN PROPERTY'].copy()

# Clean the data - remove invalid coordinates
stolen_property_data = stolen_property_data.dropna(subset=['Latitude', 'Longitude'])

# Filter out obviously incorrect coordinates (should be in San Francisco area)
sf_bounds = {
    'lat_min': 37.70, 'lat_max': 37.85,
    'lon_min': -122.52, 'lon_max': -122.35
}

valid_coords = (
    (stolen_property_data['Latitude'] >= sf_bounds['lat_min']) & 
    (stolen_property_data['Latitude'] <= sf_bounds['lat_max']) & 
    (stolen_property_data['Longitude'] >= sf_bounds['lon_min']) & 
    (stolen_property_data['Longitude'] <= sf_bounds['lon_max'])
)

stolen_property_data = stolen_property_data[valid_coords]

# Ensure coordinates are float type
stolen_property_data.loc[:,'Latitude'] = stolen_property_data['Latitude'].astype(float)
stolen_property_data.loc[:,'Longitude'] = stolen_property_data['Longitude'].astype(float)

# Update the base map settings
stolen_property_map = folium.Map(
    location=[37.7749, -122.4194],
    zoom_start=12,
    tiles='CartoDB dark_matter',
    control_scale=True
)

# Update the title
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50%; transform: translateX(-50%);
            z-index: 9999; font-size: 18px; font-weight: bold;
            background-color: rgba(0, 0, 0, 0.7); color: white; 
            border-radius: 5px; padding: 10px; text-align: center;
            width: 400px;">
    Stolen Property Incidents in San Francisco (2003-2024)
</div>
'''
stolen_property_map.get_root().html.add_child(folium.Element(title_html))

# Update the legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px;
            z-index: 9999; font-size: 14px;
            background-color: rgba(0, 0, 0, 0.7); color: white; 
            border-radius: 5px; padding: 10px; text-align: left;">
    <div style="margin-bottom: 5px;"><strong>Stolen Property Incidents</strong></div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
        <div style="background: rgba(255, 0, 0, 0.8); width: 20px; height: 20px; margin-right: 5px;"></div>
        <span>High Concentration</span>
    </div>
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
        <div style="background: rgba(255, 255, 0, 0.8); width: 20px; height: 20px; margin-right: 5px;"></div>
        <span>Medium Concentration</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background: rgba(0, 0, 255, 0.8); width: 20px; height: 20px; margin-right: 5px;"></div>
        <span>Low Concentration</span>
    </div>
</div>
'''
stolen_property_map.get_root().html.add_child(folium.Element(legend_html))

# Group data by year
years = sorted(stolen_property_data['Year'].unique())

# Prepare heatmap data with improved normalization
heat_data = []
max_incidents_per_location = 5  # Reduced threshold for better contrast
min_incidents_for_display = 2

for year in years:
    year_data = stolen_property_data[stolen_property_data['Year'] == year]
    
    # Count incidents per location
    location_counts = year_data.groupby(['Latitude', 'Longitude']).size().reset_index(name='count')
    
    # Filter and normalize
    location_counts = location_counts[location_counts['count'] >= min_incidents_for_display]
    location_counts['normalized_count'] = (location_counts['count']
                                         .clip(upper=np.percentile(location_counts['count'], 95))
                                         .rank(pct=True))
    
    year_points = []
    for _, row in location_counts.iterrows():
        weight = int(row['normalized_count'] * max_incidents_per_location)
        if weight > 0:
            year_points.extend([[row['Latitude'], row['Longitude']]] * weight)
    
    heat_data.append(year_points)

# Create time index with incident counts
time_index = []
for year in years:
    year_count = len(stolen_property_data[stolen_property_data['Year'] == year])
    time_index.append([f"{year} ({year_count} incidents)"])

# Update heatmap parameters
heatmap_with_time = HeatMapWithTime(
    heat_data,
    index=time_index,
    auto_play=True,
    max_opacity=0.6,
    radius=15,
    gradient={
        0.2: 'blue',
        0.4: 'cyan',
        0.6: 'yellow',
        0.8: 'orange',
        1.0: 'red'
    },
    min_opacity=0.1,
    use_local_extrema=True
)

heatmap_with_time.add_to(stolen_property_map)

# Add district markers
districts = stolen_property_data.groupby('District')[['Latitude', 'Longitude']].mean().reset_index()

for _, district in districts.iterrows():
    folium.Marker(
        location=[district['Latitude'], district['Longitude']],
        popup=district['District'],
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(75, 18),
            html=f'<div style="font-size: 12pt; color: white; background-color: rgba(0, 0, 0, 0.6); padding: 5px; border-radius: 3px;">{district["District"]}</div>'
        )
    ).add_to(stolen_property_map)

# Save the map
stolen_property_map.save('sf_stolen_property_animation.html')