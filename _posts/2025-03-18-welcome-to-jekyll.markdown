---
layout: post
title: "Tracking Crime in San Francisco: Two Key Patterns"
date: 2025-03-18 10:33:09 +0100
categories: data-story
---

## Introduction  
San Francisco's crime data from 2003 to 2024 offers a window into the city's shifting challenges. In this we want to try to investigate the crime data from San Fransisco throughout the years, and see if we can find any interesting patterns or changes  we can talk about and see if it correlates with what we can find about San Fransisco on the internet.

---

## Diverging Crime Trends  
![crimeoveryears](/assets/images/improved_crime_trends.png)  
*Fig 1: Yearly trends for 10 major crime categories (solid line = count, dashed = % of total crimes)*  

The time series analysis of 10 key crime categories wherre we have the highest number of that crime done in the corresponding year and also the lowest year. Moreover we have also both the Total incidents and then also the percentages of total crimes. We can see multiple patterns and interesting things based on this plot for our focus crimes.
- **Different Crime Categories, Different Patterns**  
  While some crimes, like weapon laws, are pretty steady with some shifts, others, such as prostitution, rise and fall sharply due to social factors and changes in time. (reference)  

- **Crime Numbers and % of total crimes**  
  The total number of crimes can be misleading without context. **Assault**, for example, have very stable counts of incidents but % of all crimes still fluctates a bit. Which also gives an interesting view of both how many incidents there are and how much they constitute to the total amount of crimes throughout all the 10 focus crimes.

- **Peaks**  
  All Crimes except Stolen Property either peaks before 2010 or after 2016 which shows an indication that most crimes in San Francisco has happened in the early 2000's or closer till today based on this crime type we look at. The only crime that does not follow this pattern is Stolen Property which peaks right in the middle which is 2013 in this case.

- **Investigation of Stolen Property**  
  Also unlike other crimes, **stolen property reports raised to more than the double from 2008 to 2013**. This is very interesting since most of the other crimes are pretty steady or falling in this time area. So this we want to dig deeper into and try to understand and see more about the stolen property. This also leads to our Heatmap where we have made an Heatmap movie over the Stolen Property crime year by year in San Fransisco to get a better understanding of this.

---

---

## Stolen Property Hotspots  
<iframe src="/assets/plots/sf_stolen_property_animation.html" width="100%" height="500px"></iframe>  
*Fig 2: Geographic concentration of stolen property reports over time (darker = more reports)*  

The heatmap video offers a closer look at where stolen property crimes are most concentrated and if the year has anything to do with in which part it happens:
- **Clusters**: Whereas city centers understandably register high levels of activity which in this case are mostly Tenderloin, Sotuhern, Mission and Northern, several neighborhoods which are not necessarily expected to have high crime show close clusters of reports of missing property.
- **What happens in around 2013**: Around 2013 the crimes clusters a lot more than before and almost all crimes this year is in one of the 4 areas mentioned before which is very interesting since this also is the year with most stolen properties. This shows that just because stolen properties are spread more out does not mean it correlates which how many stolen properties is happening the current year.
- **What the Hotspots Tell Us**: The stolen property map shows these crimes cluster in specific areas rather than spreading evenly as also mentioned before. This suggests that there probably are organized operations or local factors like pawn shop density since a lot of the stolen properties appear the same places.

Combined with the timeline chart, stolen property emerges as unique - while other crimes follow expected patterns, this category moves to its own rhythm than the rest of the crimes which is very interesting.

---

## When Do Crimes Happen?  
<iframe src="/assets/plots/sf_crime_interactive_bokeh.html" width="100%" height="500px"></iframe>  
*Fig 3: Explore hourly patterns by crime type and year (interactive).*  



---

## Conclusion  
**Key takeaways:**  
Missing

**Further reading:**  

**References:**  

