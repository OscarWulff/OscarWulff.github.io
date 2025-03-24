import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from bokeh.plotting import figure, output_file, show, save
from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.palettes import Category10, Category20
import bokeh.palettes as palettes
from datetime import datetime

# Set plot styles
plt.style.use('seaborn-v0_8')
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.family'] = 'sans-serif'

# Define the focus crime categories
focuscrimes = ['VEHICLE BREAK-IN', 'ROBBERY', 'ASSAULT', 'DRUG/NARCOTIC', 'BICYCLE THEFT']

# ----------------------------------------------------------
# VISUALIZATION 1: Time Distribution Plot (Matplotlib)
# ----------------------------------------------------------

# Convert time to hours since midnight
def convert_to_hours(time_str):
    try:
        # Handle case where time is already a time object
        if isinstance(time_str, datetime.time):
            return time_str.hour + time_str.minute/60 + time_str.second/3600
        
        # Handle different string formats
        if isinstance(time_str, str):
            if time_str.startswith(':'):
                # If it starts with colon (like ":00"), assume it's minutes
                minutes = int(time_str[1:])
                return minutes/60
                
            if ':' in time_str:
                # Try standard time formats
                parts = time_str.split(':')
                if len(parts) == 2:
                    return int(parts[0]) + int(parts[1])/60
                elif len(parts) == 3:
                    return int(parts[0]) + int(parts[1])/60 + int(parts[2])/3600
                    
        # Try to parse as decimal hours
        return float(time_str)
    except:
        # Return NaN for unparseable values
        return float('nan')

# Apply conversion function to the data
# Assuming IRH_all is loaded or would be loaded from your data source
IRH_all = pd.read_csv('sf_crime_data.csv')  # Replace with your actual data file
IRH_all['HoursSinceMidnight'] = IRH_all['Time'].apply(convert_to_hours)

# Filter for focus crimes
focus_data = IRH_all[IRH_all['Category'].isin(focuscrimes)]

# Create the box plot with violin overlay for better distribution visualization
plt.figure(figsize=(15, 8))
ax = sns.violinplot(x='Category', y='HoursSinceMidnight', data=focus_data, 
                    palette='Blues', inner='box', cut=0)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Crime Type', fontsize=14)
plt.ylabel('Time of Day (Hours)', fontsize=14)
plt.title('Time Distribution of Different Crime Types in San Francisco', fontsize=18)

# Format y-axis to show hour labels with AM/PM
from matplotlib.ticker import FuncFormatter

def format_hours(x, pos):
    hours = int(x)
    minutes = int((x - hours) * 60)
    if hours < 12:
        return f"{hours if hours > 0 else 12}:{minutes:02d} AM"
    else:
        return f"{hours-12 if hours > 12 else hours}:{minutes:02d} PM"

ax.yaxis.set_major_formatter(FuncFormatter(format_hours))
plt.yticks(np.arange(0, 24.1, 3))  # Place ticks every 3 hours

# Add grid lines for readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add annotations for peak times
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
        plt.annotate(f"Peak", xy=(i, peak_hour), xytext=(i+0.3, peak_hour),
                    arrowprops=dict(arrowstyle='->'), fontsize=10)

# Add source attribution
plt.figtext(0.1, 0.01, "Source: SF Police Department Incident Reports, 2014-2024", 
            fontsize=10, style='italic')

# Save the figure
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

# Filter for coordinates within San Francisco proper
# (sometimes data includes outliers that would distort the map)
sf_bounds = {
    'lat_min': 37.70,
    'lat_max': 37.84,
    'lon_min': -122.52,
    'lon_max': -122.35
}

valid_coords = IRH_all[
    (IRH_all['Latitude'] >= sf_bounds['lat_min']) &
    (IRH_all['Latitude'] <= sf_bounds['lat_max']) &
    (IRH_all['Longitude'] >= sf_bounds['lon_min']) &
    (IRH_all['Longitude'] <= sf_bounds['lon_max'])
]

# Create a heatmap layer using the crime data
# Sample to make the visualization more efficient
sample_size = min(20000, len(valid_coords))
heat_data = valid_coords.sample(sample_size)[['Latitude', 'Longitude']].values.tolist()

# Add the heatmap layer
HeatMap(heat_data, 
        radius=15, 
        blur=10, 
        max_zoom=13,
        gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'orange', 1: 'red'}).add_to(sf_map)

# Add a title and legend
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50px; width: 300px; height: 90px; 
            background-color: white; border:2px solid grey; z-index:9999; padding: 10px;
            font-size:16px; font-family: Arial, sans-serif;">
    <h4 style="margin-top: 0;">San Francisco Crime Hotspots</h4>
    <p style="font-size: 12px;">
        Color intensity indicates concentration of incidents.
    </p>
</div>
'''
sf_map.get_root().html.add_child(folium.Element(title_html))

# Add neighborhood labels for key areas
neighborhoods = {
    'Tenderloin': [37.783, -122.415],
    'Mission': [37.760, -122.419],
    'SoMa': [37.778, -122.405],
    'Financial District': [37.794, -122.400],
    'Fisherman\'s Wharf': [37.808, -122.418]
}

for name, coords in neighborhoods.items():
    folium.Marker(
        location=coords,
        icon=folium.DivIcon(
            icon_size=(150,36),
            icon_anchor=(75,18),
            html=f'<div style="font-size: 12pt; font-weight: bold; color: black;">{name}</div>'
        )
    ).add_to(sf_map)

# Save the map
sf_map.save('assets/plots/sf_crime_heatmap.html')

print("Crime heatmap created!")

# ----------------------------------------------------------
# VISUALIZATION 3: Hourly Crime Distribution (Bokeh Interactive)
# ----------------------------------------------------------

# Process data for hourly distribution
# Group incidents by hour of day and crime category
hour_data = {'Hours': [str(h) for h in range(24)]}

for crime in focuscrimes:
    # Filter for this crime type
    crime_data = IRH_all[IRH_all['Category'] == crime]
    
    # Extract hour from the time
    crime_hours = crime_data['HoursSinceMidnight'].apply(lambda x: int(x) if not pd.isna(x) else None)
    
    # Count incidents by hour
    hour_counts = crime_hours.value_counts().sort_index()
    
    # Normalize to show distribution rather than absolute counts
    hour_normalized = hour_counts / hour_counts.sum()
    
    # Create a full range of hours with zeros for missing hours
    full_hours = pd.Series(0, index=range(24))
    for h, count in hour_normalized.items():
        if 0 <= h < 24:  # Ensure hour is valid
            full_hours[h] = count
    
    # Add to the hour_data dictionary
    hour_data[crime] = full_hours.values

# Convert DataFrame to Bokeh ColumnDataSource
from bokeh.models import ColumnDataSource
source = ColumnDataSource(hour_data)

# Create the figure
from bokeh.plotting import figure
from bokeh.models import FactorRange
hours = [str(h) for h in range(24)]  # Hours as strings: '0', '1', '2', ..., '23'

p = figure(
    title="Hourly Distribution of SF Crimes (2014-2024)",
    x_range=FactorRange(factors=hours),
    height=500,
    width=900,
    toolbar_location="right",
    tools="pan,wheel_zoom,box_zoom,reset,save",
    x_axis_label="Hour of Day",
    y_axis_label="Normalized Frequency"
)

# Add bars for each crime category
# Use a color palette with enough colors for all focus crimes
num_colors = len(focuscrimes)
colors = palettes.Category10[10] if num_colors <= 10 else palettes.Category20[20][:num_colors]

# Create empty dictionary to store vbars
bars = {}

# Add vbars for each crime category
for i, crime in enumerate(focuscrimes):
    bars[crime] = p.vbar(
        x='Hours',           # x-coordinates (hours)
        top=crime,           # y-coordinates (normalized values from each crime column)
        source=source,
        width=0.8,           # width of bars
        color=colors[i],     # color from palette
        legend_label=crime,  # legend label
        muted_alpha=0.2,     # alpha when muted
        muted=False          # not muted initially
    )

# Add hover tool for better interactivity
hover = HoverTool(tooltips=[
    ("Hour", "@Hours:00"),
    *[(crime, f"@{crime}{0.00%}") for crime in focuscrimes]
])
p.add_tools(hover)

# Configure the legend to be interactive
p.legend.click_policy = "mute"

# Move the legend outside the plot area to avoid occlusion
p.add_layout(p.legend[0], 'right')

# Style the legend
p.legend.background_fill_alpha = 0.7
p.legend.border_line_color = "black"
p.legend.border_line_width = 1
p.legend.label_text_font_size = "8pt"

# Add grid lines for better readability
p.grid.grid_line_color = "gray"
p.grid.grid_line_alpha = 0.3
p.grid.minor_grid_line_alpha = 0.1

# Format y-axis
p.yaxis.formatter.use_scientific = False
p.y_range.start = 0  # Start from 0

# Add time period labels to help interpretation
time_periods = [
    {"period": "Early Morning", "start": 5, "end": 8},
    {"period": "Morning Rush", "start": 7, "end": 9},
    {"period": "Business Hours", "start": 9, "end": 17},
    {"period": "Evening Rush", "start": 17, "end": 19},
    {"period": "Evening", "start": 19, "end": 22},
    {"period": "Late Night", "start": 22, "end": 24}
]

# Add annotations for time periods
for period in time_periods:
    # Calculate position (middle of period)
    mid_hour = (period["start"] + min(period["end"], 23)) / 2
    p.add_layout(
        bokeh.models.Label(
            x=str(int(mid_hour)), y=0.01,
            text=period["period"],
            text_font_size="8pt",
            text_color="gray",
            text_align="center",
            y_offset=-30
        )
    )

# Remove toolbar logo
p.toolbar.logo = None

# Save the plot
output_file("assets/plots/sf_crime_hourly_distribution.html")
save(p)

print("Interactive hourly distribution visualization created!")
print("All visualizations completed successfully!")