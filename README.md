# Integration and Visualisation of Olympic Data

## Overview

This project focuses on the **integration and visualisation of Olympic data** from multiple sources. The goal is to gain insights into Olympic events, athletes, and trends through effective data processing and interactive visual representation using a web-based dashboard.

## Data Sources

We collected data from a variety of sources, including:

- Open-source Olympic datasets
- Web-scraped information from official and unofficial Olympic-related websites

These datasets were integrated, cleaned, and structured for analysis using Python-based tools.

## Data Processing

We used the following Python libraries for data integration and transformation:

- **Pandas**: for merging, filtering, and transforming data tables
- **NumPy**: for numerical operations and efficient array handling

Key steps included:

- Calculating total medals by summing individual medal counts
- Filtering incomplete entries (e.g., missing age or sport)
- Grouping and aggregating data for specific visualisation requirements
- Categorising sports into thematic groups like ball sports, water sports, and others

## Visualisation

The core of this project is an interactive **Dash** dashboard powered by **Plotly** visualisations. The dashboard includes:

- **Bubble Map**: Olympic Medals by Country and Year  
- **Box and Whisker Plot**: Age Distribution of Athletes by Sport  
- **Bar/Line Graph**: Average Height of Athletes by Sport and Gender  
- **Heatmap**: Medal Distribution by Age and Sport  
- **Line Graph**: Medals Comparison by Gender and Sport  
- **Radar Chart**: Medal Distribution by Sport Type  

These visualisations allow users to explore patterns in athlete demographics, country performances, and historical trends. Interactive filters (by year, country, and gender) enable dynamic exploration of the data.

## Goals

- Demonstrate skills in data integration, filtering, and enrichment
- Provide a clean and engaging interface for users to interact with Olympic data
- Use data visualisation to highlight meaningful trends and insights across Olympic history

---

*This project combines data engineering, data analysis, and front-end development to tell the story of the Olympic Games through interactive visualisations.*
