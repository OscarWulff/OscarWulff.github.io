---
layout: post
title: "Tracking Crime in San Francisco: Two Key Patterns"
date: 2025-03-18 10:33:09 +0100
categories: data-story
---

## Introduction  
San Francisco's crime data tells a story of urban life across two decades. Using official police reports from 2003-2024, we examine how different offenses have evolved and where stolen property incidents cluster most intensely.  

But one anomaly stood out—stolen property reports displayed unusual patterns, particularly in areas with low overall crime rates. Was this due to an organized fencing operation, misreporting, or something else? I decided to investigate further.  

---

## Diverging Crime Trends  
![crimeoveryears](/assets/images/improved_crime_trends.png)  
*Fig 1: Yearly trends for 10 major crime categories (solid line = count, dashed = % of total crimes)*  

Key observations from the time series:  
- **Category Variation**: Each crime type shows unique fluctuations rather than moving in unison  
- **Percentage vs. Count**: Some crimes (like LARCENY/THEFT) show different stories when viewed as counts versus percentages of total crimes  
- **Notable Peaks**: Multiple categories show their highest points between 2012-2015  
- **Recent Declines**: Most categories display downward trends post-2020  

The dual-axis visualization reveals that a crime's raw count doesn't always match its relative prevalence—important context for policy decisions.  

---

## Stolen Property Hotspots  
<iframe src="/assets/plots/sf_stolen_property_animation.html" width="100%" height="500px"></iframe>  
*Fig 2: Geographic concentration of stolen property reports over time (darker = more reports)*  

The animated heatmap shows:  
- **Persistent Zones**: Certain areas maintain high activity across all years  
- **District Variations**: Clear boundaries between high/low incident areas  
- **Temporal Shifts**: Some neighborhoods show changing patterns, particularly after 2015  
- **Data Density**: The downtown core shows the most intense clustering  

One unexpected finding was the emergence of stolen property clusters in historically low-crime neighborhoods. Could this indicate an organized network using these areas for storage or resale? Further research into pawn shop activity and police reports from those zones might shed light on the trend.  

---

## When Do Crimes Happen?  
<iframe src="/assets/plots/sf_crime_interactive_bokeh.html" width="100%" height="500px"></iframe>  
*Fig 3: Explore hourly patterns by crime type and year (interactive).*

Notable finding: Robberies peak at... [Compare to SF Nightlife Economic Report 2023].

---

## Conclusion  
Key takeaways:  
- Crime trends vary significantly across categories, with unique peaks and declines.  
- Stolen property incidents show distinct geographic shifts, potentially pointing to organized crime.  
- Temporal patterns suggest strong links between robbery spikes and nightlife activity.  
- Future investigations should incorporate external datasets (pawn shop records, socioeconomic data) for a fuller picture.  
