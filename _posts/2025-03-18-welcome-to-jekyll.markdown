---
layout: post
title: "The Rhythm of Crime: Temporal Patterns in San Francisco"
date: 2025-03-24 10:00:00 +0100
categories: data visualization
---

# **The Rhythm of Crime: Temporal Patterns in San Francisco** 📊

San Francisco's crime landscape ebbs and flows with the city's daily pulse. In this analysis, we'll explore how different types of crime follow distinct temporal patterns throughout the day and across neighborhoods, revealing insights about urban safety that might not be immediately apparent from raw statistics.

---

## **Introduction to the Dataset**

The San Francisco Police Department maintains a detailed Incident Report dataset that captures reported crime across the city. Our analysis focuses on data from 2014 to 2024, examining how crime patterns have evolved over time and throughout each day.

Each incident in the dataset includes:
- Crime category
- Date and time of occurrence
- Geographic coordinates
- Police district and neighborhood information

For this analysis, we've focused on five major street crime categories that significantly impact residents' and visitors' daily experiences in the city.

---

## **📈 The Daily Crime Cycle**

Different crimes follow different schedules. By examining when various offenses occur throughout the day, we can better understand the rhythm of criminal activity in San Francisco.

![Daily Distribution of Crime Types](/assets/images/sf_crime_time_distribution.png)

The visualization above reveals several distinct patterns:

- **Vehicle break-ins** peak sharply in the late afternoon and early evening (3-7pm), coinciding with when tourists and commuters are most likely to leave valuables in parked cars.
- **Robberies** cluster during evening hours (6-10pm) when streets may be less crowded but still have potential victims.
- **Assaults** increase throughout the day, peaking in the late evening hours (9pm-2am), correlating with nightlife activities.
- **Drug-related incidents** show the most consistent distribution throughout the day, reflecting the ongoing nature of drug trafficking and use.
- **Bicycle theft** primarily occurs during working hours when bikes are often left secured but unattended.

These patterns suggest different intervention strategies might be effective depending on the time of day and type of crime.

---

## **🗺️ Mapping Crime Across the City**

Crime in San Francisco isn't distributed evenly. The map below shows where incidents concentrate across different neighborhoods.

<iframe src="/assets/plots/sf_crime_heatmap.html" width="100%" height="500px"></iframe>

This map reveals several notable hotspots:

- The **Tenderloin** and parts of **SoMa** show the highest concentration of incidents, particularly for drug-related crimes and assaults.
- **Union Square** and the surrounding shopping district experience elevated levels of theft and robbery.
- The **Mission District** shows consistent activity across multiple crime categories, with particular concentration along Mission Street and near BART stations.
- **Tourist areas** like Fisherman's Wharf and Lombard Street show spikes in vehicle break-ins and property crime.

The clustering of incidents around transit hubs and commercial corridors highlights how urban mobility patterns influence crime opportunity.

---

## **⏱ Crime Trends Through Time**

How have crime patterns evolved over the past decade? The interactive visualization below allows you to explore trends for different crime categories over time.

<iframe src="/assets/plots/sf_crime_hourly_distribution.html" width="125%" height="500px"></iframe>

This hourly distribution reveals several key insights:

- **Morning commute** (7-9am) sees a notable increase in bicycle theft and vehicle break-ins, likely targeting commuters.
- **Lunch hour** (12-2pm) shows spikes in theft and shoplifting in commercial districts.
- **Evening rush** (5-7pm) experiences elevated levels of robbery and assault.
- **Late night** (10pm-2am) shows the highest concentration of violent crime, particularly in entertainment districts.

When comparing these patterns across different years, we can observe how the COVID-19 pandemic dramatically altered crime trends in 2020-2021, with some categories returning to pre-pandemic patterns by 2022, while others established new patterns.

---

## **Key Takeaways**

Our analysis of San Francisco crime data reveals several important patterns:

1. **Temporal signatures**: Different crime categories follow distinct daily patterns that reflect opportunity structures and human activity cycles.

2. **Geographic concentration**: Crime clusters in predictable ways around specific urban features like transit hubs, commercial areas, and entertainment districts.

3. **Evolving patterns**: The city's crime landscape has changed over the past decade, with significant disruption during the pandemic period that continues to influence current trends.

These insights can help inform both personal safety decisions and public policy. For residents and visitors, understanding when and where different types of crime are most likely to occur can help guide daily routines and precautions. For city officials and law enforcement, these patterns suggest where and when to focus resources for maximum impact.

---

## **Methodology Notes**

Our analysis used Python with the following libraries:
- Pandas and NumPy for data processing
- Matplotlib and Seaborn for static visualizations
- Folium for mapping
- Bokeh for interactive visualizations

The hourly crime distribution visualization normalizes crime counts within each category to better highlight temporal patterns across crime types with different total volumes.

Data Source: [San Francisco Police Department Incident Reports](https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783)