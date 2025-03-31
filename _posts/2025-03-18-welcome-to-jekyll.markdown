---
layout: post
title: "Crime Trends and Stolen Property in San Francisco"
date: 2025-03-31 10:33:09 +0100
categories: data-story
---

## Introduction  
San Francisco's crime data from 2003 to 2024 offers a window into the city's shifting challenges. In this we want to try to investigate the Vechicle Theft incidents from San Fransisco throughout the years, and see if we can find any interesting patterns or changes. We would also like to investigate how it correlates with what information is available about San Fransisco on the internet.

---

## Diverging Crime Trends  
![crimeoveryears](/assets/images/improved_crime_trends.png)  
***Figure 1**: The distribution of vehicle theft incidents throughout a 24-hour period.*  

The plot in Figure 1 illustrates the distribution of vehicle theft incidents throughout a 24-hour period. Here darker and larger sections represent higher crime volumes opposed to smaller and lighter sections representing low volumes. There exist a clear evening/night concentration with peak vehicle theft hours occuring between 17:00-22:00, with 18:00 being the hour with the highest frequency. The maximal volume reach approximately 12,000-14,000 incidents at this peak hour. Between 01:00-07:00 the theft rates drops significantly which is probably due to most people are sleeping at this point. Throughout the day the number of thefts remains constant with a surprising peak at noon. Why this happens is difficult to determine (måske kilder kan forklar en mulig årsag) We hypothesize that the theft patterns can be explained by their alignment with darker evening hours when vehicles are often unattended for instance after work.

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
1. San Francisco Police Department. (n.d.). *Police Department Incident Reports: Historical 2003 to May 2018*. Retrieved from https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry/about_data  
2. San Francisco Police Department. (n.d.). *Police Department Incident Reports: 2018 to Present*. Retrieved from https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/about_data