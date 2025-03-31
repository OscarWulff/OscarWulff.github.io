---
layout: post
title: "Investigation of Vehicle Theft in San Francisco"
date: 2025-03-31 10:33:09 +0100
categories: data-story
---

## Introduction  
San Francisco's crime data from 2003 to 2024 offers a window into the city's shifting challenges. In this project we want to try to investigate the Vehicle Theft incidents from San Francisco throughout the years, and see if we can find any interesting patterns or changes. We would also like to investigate how it correlates with what information is available about San Francisco on the internet.
---

## When Cars Are Most at Risk  
![crimeoveryears](/assets/images/improved_crime_trends.png)  
***Figure 1**: The distribution of vehicle theft incidents throughout a 24-hour period.*  

The plot in Figure 1 illustrates the distribution of vehicle theft incidents throughout a 24-hour period. Here darker and larger sections represent higher crime volumes opposed to smaller and lighter sections representing low volumes. There exist a clear evening/night concentration with peak vehicle theft hours occuring between 17:00-22:00, with 18:00 being the hour with the highest frequency. The maximal volume reach approximately 12,000-14,000 incidents at this peak hour. Between 01:00-07:00 the theft rates drops significantly which is probably due to most people are sleeping at this point. Throughout the day the number of thefts remains constant with a surprising peak at noon. Why this happens is difficult to determine. We hypothesize that the theft patterns can be explained by their alignment with darker evening hours when vehicles are often unattended for instance after work.

---

## Vehicle Theft Hotspots  
<iframe src="/assets/plots/sf_stolen_property_animation.html" width="100%" height="500px"></iframe>  
***Figure 2**: Geographic concentration of vehicle theft reports over time (darker = more reports)*  

The heatmap video offers a closer look at where vehicle crimes are most concentrated and if the year has anything to do with in which part it happens:
- **Clusters**: Whereas city centers understandably register high levels of activity which in this case are all the big city centers, several neighborhoods which are not necessarily expected to have high crime show close clusters of reports of vehicle theft which shows that it happens in all areas of San Francisco.
- **Changes throughout the years**: We can see that from 2005 to 2006 the incidents fall of a lot which also can be seen as there are a lot less hotspots on the map in 2006 and afterwards. The incidents falls from 18097 to 7263 which is a due to the anti theft for cars being improved a lot in those years, and moreover as the article says the police also gave anti theft devices in that year[1].
- **What the Hotspots Tell Us**: The vehicle theft map shows these crimes cluster in specific areas rather than spreading evenly, as also mentioned before. This suggests that there are likely organized operations or local factors, like the proximity of car dealerships or high-traffic areas, since many of the stolen vehicles appear in the same locations.

---

## The Changing Crime Landscape 
<iframe src="/assets/plots/lineplot.html" width="100%" height="500px"></iframe>  
***Figure 3**: Stacked Area Chart of the number of vehicle theft incidents across time per district.*  

The line plot above visualizes the annual trend in vehicle theft incidents from 2003 to 2024 across the districts. As such we can now uncover both geographical and temporal patterns of the vehicle crimes in San Fransisco.

- **2003-2005: Peak Years**  
  Vehicle theft incidents were at their highest, in 2003-2005. This was also what we concluded based on the heatmap. This period aligns with a lack of strong anti-theft technology in cars and potentially weaker enforcement policies. 
  
- **Crimes by District**  
  We can also see throughout all the years that the crimes in the different district does not change that much but seems very steady. We can see that Tenderloin is the district with least vehicle thefts and Bayview is the district with most vehicle thefts. This pattern correlates with socioeconomic factors as Bayview-Hunters Point has been characterized as a lower-income neighborhood historically [2].
  
- **Upward Trend**
  In the most recent years, there seem to be an increase in the number of vehicle theft. There are many ways to reduce and stop this trends. There are several ways to stop this trend, including improved security devices, increased police presence, and societal changes. A former Apple product designer called Mark Rober took a more... well creative approach by deploying glitter bombs to surprise and shame thieves [3]. The fear of encountering one might have played a role in last year’s decline!
  
---

## Conclusion  
Our website provides an analysis of the spatial and temporal patterns of vehicle theft in the San Fransisco area during the period from 2003 to 2024. Through the three visualizations we have illustrated and interpreted the data from the San Fransisco Police Department [4][5], extracting insights into trends of vehicle theft.

**References:**  
1. Breitler, A. 2007. *Vehicle thefts dropped in 2006*. The Record. Retrieved from https://eu.recordnet.com/story/news/crime/2007/04/25/vehicle-thefts-dropped-in-2006/52914690007/
2. Florida & Johnson, R & S. 04-01-2013. *Class-Divided Cities: San Francisco Edition*. Bloomberg. Retrieved from https://www.bloomberg.com/news/articles/2013-04-01/class-divided-cities-san-francisco-edition
3. Bindman, A. 12-24-2023. *San Francisco car thieves exposed, humiliated by 'glitter bombs'*. SFGATE. Retrieved from https://www.sfgate.com/local/article/glitter-bomb-san-francisco-car-break-ins-18549602.php
4. San Francisco Police Department. (n.d.). *Police Department Incident Reports: Historical 2003 to May 2018*. Retrieved from https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry/about_data  
5. San Francisco Police Department. (n.d.). *Police Department Incident Reports: 2018 to Present*. Retrieved from https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/about_data