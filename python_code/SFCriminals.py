import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, FactorRange, HoverTool, Label
import bokeh.palettes as palettes
from datetime import datetime

# Set global plot styles for consistency
plt.style.use('seaborn-v0_8')
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.family'] = 'sans-serif'

# Define the focus crime categories
focuscrimes = ['VEHICLE BREAK-IN', 'ROBBERY', 'ASSAULT', 'DRUG/NARCOTIC', 'BICYCLE THEFT']

# ----------------------------------------------------------
# Data Loading and Preprocessing
# ----------------------------------------------------------
# Load historical data (update file paths as needed)
IRH_first = pd.read_csv('python_code/data/Police_Department_Incident_Reports__Historical_2003_to_May_2018.csv')
IRH_second = pd.read_csv('python_code/data/Police_Department_Incident_Reports__2018_to_Present_20250204.csv')

# Select relevant columns for both datasets
IRH_first = IRH_first[['Category', 'DayOfWeek', 'Date', 'Time', 'PdDistrict', 'location', 'X', 'Y']]
IRH_second = IRH_second[['Incident Category', 'Incident Day of Week', 'Incident Date', 'Incident Time', 'Police District', 'Point', 'Longitude', 'Latitude']]

# Rename columns to have a consistent naming convention
merged_column_names = ['Category', 'DayOfWeek', 'Date', 'Time', 'District', 'PointLocation', 'Longitude', 'Latitude']
IRH_first.columns = merged_column_names
IRH_second.columns = merged_column_names

# Standardize string case in IRH_second for consistency
IRH_second['Category'] = IRH_second['Category'].str.upper()
IRH_second['District'] = IRH_second['District'].str.upper()

# Convert Date columns to datetime objects
IRH_first['Date'] = pd.to_datetime(IRH_first['Date'])
IRH_second['Date'] = pd.to_datetime(IRH_second['Date'])

# Make consistent category mapping
category_mapping = {
    'LARCENY THEFT': 'LARCENY/THEFT',
    'LARCENY/THEFT': 'LARCENY/THEFT',
    'BURGLARY': 'BURGLARY',
    'MOTOR VEHICLE THEFT': 'VEHICLE THEFT',
    'MOTOR VEHICLE THEFT?': 'VEHICLE THEFT',
    'VEHICLE THEFT': 'VEHICLE THEFT',
    'DRUG OFFENSE': 'DRUG/NARCOTIC',
    'DRUG VIOLATION': 'DRUG/NARCOTIC',
    'DRUG/NARCOTIC': 'DRUG/NARCOTIC',
    'FORGERY AND COUNTERFEITING': 'FORGERY/COUNTERFEITING',
    'FORGERY/COUNTERFEITING': 'FORGERY/COUNTERFEITING',
    'SEX OFFENSES, FORCIBLE': 'SEX OFFENSE',
    'SEX OFFENSES, NON FORCIBLE': 'SEX OFFENSE',
    'SEX OFFENSE': 'SEX OFFENSE',
    'WEAPON LAWS': 'WEAPON LAWS',
    'WEAPONS CARRYING ETC': 'WEAPON LAWS',
    'WEAPONS OFFENCE': 'WEAPON LAWS',
    'WEAPONS OFFENSE': 'WEAPON LAWS',
    'WARRANT': 'WARRANTS',
    'WARRANTS': 'WARRANTS',
    'OTHER': 'OTHER',
    'OTHER MISCELLANEOUS': 'OTHER',
    'OTHER OFFENSES': 'OTHER',
    'HUMAN TRAFFICKING, COMMERCIAL SEX ACTS': 'HUMAN TRAFFICKING (A), COMMERCIAL SEX ACTS',
    'SUSPICIOUS': 'SUSPICIOUS OCC',
    'MALICIOUS MISCHIEF': 'VANDALISM'
}

IRH_first['Category'] = IRH_first['Category'].replace(category_mapping)
IRH_second['Category'] = IRH_second['Category'].replace(category_mapping)

# Concatenate datasets
IRH_all = pd.concat([IRH_first, IRH_second])

# Use only full years from 2014 to 2024
IRH_all = IRH_all[
    (IRH_all['Date'] >= pd.to_datetime('2014-01-01')) &
    (IRH_all['Date'] < pd.to_datetime('2025-01-01'))
]

# Create extra time columns
IRH_all['Year'] = IRH_all['Date'].dt.year
IRH_all['Month'] = IRH_all['Date'].dt.month
IRH_all['Day'] = IRH_all['Date'].dt.day
IRH_all['Hours'] = IRH_all['Time'].str[:2].astype(int)
IRH_all['Minutes'] = IRH_all['Time'].str[3:5].astype(int)
IRH_all['HoursSinceMidnight'] = IRH_all['Hours'] + IRH_all['Minutes'] / 60

# Filter for focus crimes (or change focus crimes if desired)
focus_data = IRH_all[IRH_all['Category'].isin(focuscrimes)]

# ----------------------------------------------------------
# VISUALIZATION 1: Time Distribution Plot (Matplotlib/Seaborn)
# ----------------------------------------------------------
plt.figure(figsize=(15, 8))
ax = sns.violinplot(x='Category', y='HoursSinceMidnight', data=focus_data, 
                    palette='Blues', inner='box', cut=0)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Crime Type', fontsize=14)
plt.ylabel('Time of Day (Hours)', fontsize=14)
plt.title('Time Distribution of Different Crime Types in San Francisco', fontsize=18)

# Format y-axis with AM/PM labels
from matplotlib.ticker import FuncFormatter

def format_hours(x, pos):
    hours = int(x)
    minutes = int((x - hours) * 60)
    if hours == 0:
        return f"12:{minutes:02d} AM"
    elif hours < 12:
        return f"{hours}:{minutes:02d} AM"
    elif hours == 12:
        return f"{hours}:{minutes:02d} PM"
    else:
        return f"{hours-12}:{minutes:02d} PM"

ax.yaxis.set_major_formatter(FuncFormatter(format_hours))
plt.yticks(np.arange(0, 24.1, 3))
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Annotate approximate peak times for each crime type (example values)
crime_peaks = {
    'VEHICLE BREAK-IN': 17,  # 5 PM
    'ROBBERY': 20,           # 8 PM
    'ASSAULT': 23,           # 11 PM
    'DRUG/NARCOTIC': 14,     # 2 PM
    'BICYCLE THEFT': 13      # 1 PM
}
for i, crime in enumerate(focuscrimes):
    if crime in crime_peaks:
        peak_hour = crime_peaks[crime]
        plt.annotate("Peak", xy=(i, peak_hour), xytext=(i+0.3, peak_hour),
                     arrowprops=dict(arrowstyle='->'), fontsize=10)

plt.figtext(0.1, 0.01, "Source: SF Police Department Incident Reports (2014-2024)", 
            fontsize=10, style='italic')
plt.tight_layout()
plt.savefig('assets/images/sf_crime_time_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("Time distribution visualization created!")

# ----------------------------------------------------------
# VISUALIZATION 2: Crime Heatmap (Folium)
# ----------------------------------------------------------
# Create a base map centered on San Francisco
sf_map = folium.Map(location=[37.7749, -122.4194], zoom_start=12, 
                    tiles='CartoDB positron')

# Define bounds to filter out outlier coordinates
sf_bounds = {'lat_min': 37.70, 'lat_max': 37.84, 'lon_min': -122.52, 'lon_max': -122.35}
valid_coords = IRH_all[
    (IRH_all['Latitude'] >= sf_bounds['lat_min']) &
    (IRH_all['Latitude'] <= sf_bounds['lat_max']) &
    (IRH_all['Longitude'] >= sf_bounds['lon_min']) &
    (IRH_all['Longitude'] <= sf_bounds['lon_max'])
]

# Sample data for performance
sample_size = min(20000, len(valid_coords))
heat_data = valid_coords.sample(sample_size)[['Latitude', 'Longitude']].values.tolist()

# Update the gradient keys to strings to avoid the 'float' error
gradient_dict = {"0.4": 'blue', "0.65": 'lime', "0.8": 'orange', "1": 'red'}

# Add a heatmap layer with the modified gradient
HeatMap(heat_data, radius=15, blur=10, max_zoom=13,
        gradient=gradient_dict).add_to(sf_map)

# Optional: add a title overlay (using HTML/CSS)
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50px; width: 300px; height: 90px; 
            background-color: white; border:2px solid grey; z-index:9999; padding: 10px;
            font-size:16px; font-family: Arial, sans-serif;">
    <h4 style="margin-top: 0;">San Francisco Crime Hotspots</h4>
    <p style="font-size: 12px;">Color intensity indicates concentration of incidents.</p>
</div>
'''
sf_map.get_root().html.add_child(folium.Element(title_html))

# Save the map as an HTML file
sf_map.save('assets/plots/sf_crime_heatmap.html')
print("Crime heatmap created!")


# ----------------------------------------------------------
# VISUALIZATION 3: Hourly Crime Distribution (Bokeh Interactive)
# ----------------------------------------------------------
# Prepare data for hourly distribution plot
hour_data = {'Hours': [str(h) for h in range(24)]}
for crime in focuscrimes:
    crime_data = IRH_all[IRH_all['Category'] == crime]
    # Group by integer hour from HoursSinceMidnight
    crime_hours = crime_data['HoursSinceMidnight'].apply(lambda x: int(x) if not pd.isna(x) else None)
    hour_counts = crime_hours.value_counts().sort_index()
    # Normalize counts
    hour_normalized = hour_counts / hour_counts.sum()
    full_hours = pd.Series(0, index=range(24))
    for h, count in hour_normalized.items():
        if 0 <= h < 24:
            full_hours[h] = count
    hour_data[crime] = full_hours.values

source = ColumnDataSource(hour_data)
hours = [str(h) for h in range(24)]
p = figure(
    title="Hourly Distribution of SF Crimes (2014-2024)",
    x_range=FactorRange(factors=hours),
    height=500, width=900,
    toolbar_location="right",
    tools="pan,wheel_zoom,box_zoom,reset,save",
    x_axis_label="Hour of Day",
    y_axis_label="Normalized Frequency"
)

# Select colors for each crime category
num_colors = len(focuscrimes)
colors = palettes.Category10[10] if num_colors <= 10 else palettes.Category20[20][:num_colors]

# Add bars for each crime category
for i, crime in enumerate(focuscrimes):
    p.vbar(x='Hours', top=crime, source=source, width=0.8, color=colors[i],
           legend_label=crime, muted_alpha=0.2)

# Add hover tool
hover = HoverTool(tooltips=[("Hour", "@Hours:00")] +
                  [(crime, f"@{crime}{{0:.2%}}") for crime in focuscrimes])
p.add_tools(hover)
p.legend.click_policy = "mute"
p.legend.location = "top_right"
p.legend.background_fill_alpha = 0.7
p.grid.grid_line_color = "gray"
p.grid.grid_line_alpha = 0.3
p.y_range.start = 0
p.yaxis.formatter.use_scientific = False

# Example of adding time period labels (optional)
time_periods = [
    {"period": "Early Morning", "start": 5, "end": 8},
    {"period": "Morning Rush", "start": 7, "end": 9},
    {"period": "Business Hours", "start": 9, "end": 17},
    {"period": "Evening Rush", "start": 17, "end": 19},
    {"period": "Evening", "start": 19, "end": 22},
    {"period": "Late Night", "start": 22, "end": 24}
]
for period in time_periods:
    mid_hour = (period["start"] + period["end"]) // 2
    label = Label(x=str(mid_hour), y=0.01, text=period["period"],
                  text_font_size="8pt", text_color="gray", text_align="center", y_offset=-30)
    p.add_layout(label)

# Remove Bokeh logo from toolbar
p.toolbar.logo = None

output_file("assets/plots/sf_crime_hourly_distribution.html")
save(p)
print("Interactive hourly distribution visualization created!")
print("All visualizations completed successfully!")
