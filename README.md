# SF-bike-safety

Bike sharing platforms are becoming increasingly common alternatives to public transportation in cities, improving accessibility to areas not reachable by bus, train, or tram. While this can be beneficial for improving city connectivity, it also increases the likelihood of biker related accidents and vehicle collisions, especially in areas where protected bike lanes and safety infrastructure are not already in place. We compare machine learning models to predict biker density at road intersections in the city of San Francisco, using publicly available trip data from the city's most widely used bikeshare service, Ford GoBike, evaluating our model performance by monitoring mean squared error. Alongside our predictive models we develop a heatmap visualization application to display our predictions, providing an additional mode of interaction for users to access the forecasted information. The intended usage of our work is to predict areas of highest biker density at different times so that drivers and bikers can experience improved shared road safety. The deployment of our models can also inform city planning and alternative public transportation development. https://ieeexplore.ieee.org/document/9033019

## Model Structure
We propose a deep learning model to identify areas of high bike traffic at various times of day in the city of San Francisco. We will train our Neural Network on data collected from Ford GoBike's records. The hourly_visits_by_station_daily_sf.csv file will be our main file for training and testing (see below for details on files and directories). The input and output behavior of our network is described below (based on the columns we have in the file):  

Input Columns: hour, weekday, station name    
Output: number of visits  

The anticipated usage is to check the predicted general number of people who are likely to be at a given bike station at a certain hour of a weekday or weekend. We use bike casualty data to corroborate intersections which may benefit from additional bike safety infrastructure.  

## Directories and Files  
* bikesafety-data-wrangling.ipynb - Notebook used to brainstorm model structure and create associated data files  
* bikesafety-data-wrangling.py - Notebook (identical to data wrangling notebook) saved as python file  
* hourly_visits_by_station_daily_sf.csv - Unzip the compressed file to get a CSV file with number of visits recorded for every SF station, at hourly points every day. This CSV can be directly loaded into a pandas dataframe. This was the main output of the python data wrangling notebook.  
* station_first_dates.json - Keys are station names and values are the first date on which there was recorded activity at that station. We can use this value as an indication of new stations being opened over time.   
