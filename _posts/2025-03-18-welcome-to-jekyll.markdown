---
layout: post
title: "Tracking Crime in San Francisco: Two Key Patterns"
date: 2025-03-18 10:33:09 +0100
categories: data-story
---

## Introduction  
San Francisco's crime data from 2003 to 2024 offers a window into the city's shifting challenges. While many crime categories follow gradual trends, stolen property incidents experienced a remarkable surge between 2008 and 2013. This anomaly raises questions about underlying factors and how these patterns relate to where crimes are reported.

---

## Diverging Crime Trends  
![crimeoveryears](/assets/images/improved_crime_trends.png)  
*Fig 1: Yearly trends for 10 major crime categories (solid line = count, dashed = % of total crimes)*  

The time series analysis of 10 key crime categories reveals several important patterns:  
- **Category Variation**: Each crime type follows its own trajectory. For instance, while overall trends for violent crimes and property offenses show gradual shifts, their rates of change differ considerably.  
- **Percentage vs. Count**: The dual-axis presentation highlights that raw incident counts and their share of total crimes can tell different stories. Some categories, such as LARCENY/THEFT, maintain high counts but vary in relative importance over time.  
- **Notable Peaks and Declines**: Many offenses reach their zenith between 2012 and 2015, followed by a decline in the post-2020 period.  
- **Stolen Property Anomaly**: Among all categories, stolen property is distinct. Its count rises dramatically from 2008 to 2013—a surge that stands out against otherwise stable or declining trends. This raises intriguing questions: Could economic factors, reporting practices, or even emerging criminal networks have driven this increase? Such a deviation warrants deeper spatial analysis to see if these trends correspond with geographic patterns.

---

## Stolen Property Hotspots  
<iframe src="/assets/plots/sf_stolen_property_animation.html" width="100%" height="500px"></iframe>  
*Fig 2: Geographic concentration of stolen property reports over time (darker = more reports)*  

The animated heatmap offers a closer look at where stolen property incidents are most concentrated:  
- **Unexpected Clusters**: While downtown areas naturally exhibit high activity, several neighborhoods not typically known for high crime rates show dense clusters of stolen property reports.  
- **Temporal Shifts**: The hotspots evolve over time, with notable changes after 2013. This suggests that the surge observed in Fig 1 might be tied to specific local factors or transient criminal trends during that period.  
- **Interpreting the Surge**: The spatial distribution hints at possible organized networks or shifts in local socioeconomic conditions influencing where stolen goods are reported. It’s possible that areas with rising pawn shop activity or relaxed enforcement may have inadvertently become hubs for these incidents.

Together, the time series in Fig 1 and the spatial analysis in Fig 2 build a compelling narrative: while most crime categories follow predictable patterns, the unique trajectory of stolen property calls for targeted investigation.

---

## When Do Crimes Happen?  
<iframe src="/assets/plots/sf_crime_interactive_bokeh.html" width="100%" height="500px"></iframe>  
*Fig 3: Explore hourly patterns by crime type and year (interactive).*  

This interactive visualization allows you to dive into the temporal dynamics of crime on an hourly basis. Notable findings include:  
- **Peak Activity**: For example, robberies consistently peak during late-night hours—an observation that aligns with trends reported in the SF Nightlife Economic Report 2023.  
- **Crime Type Variations**: Different offenses show distinct temporal patterns, suggesting that factors like nightlife, public transportation schedules, and law enforcement shifts play a role in shaping when crimes occur.

---

## Conclusion  
**Key takeaways:**  
- **Distinct Temporal Trends**: While most crime categories show steady or declining trends over recent years, stolen property incidents experienced a dramatic surge from 2008 to 2013.  
- **Spatial Insights**: The heatmap uncovers unexpected clusters of stolen property reports, hinting at localized factors such as organized criminal activity or shifts in socioeconomic conditions.  
- **Temporal Dynamics**: Hourly analysis reveals that crime patterns are influenced by a mix of environmental and social factors, with certain offenses peaking at predictable times.  
- **Implications for Policy and Future Research**: Understanding these patterns can guide targeted interventions. Further investigation using additional data sources—such as pawn shop records, economic indicators, or detailed enforcement actions—could provide deeper insights into the drivers behind these trends.

**Further reading:**  

