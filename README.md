# SF-bike-safety
Predicting high bike traffic intersections in SF

## Model Structure
We propose a deep learning model to identify areas of high bike traffic at various times of day in the city of San Francisco. We will train our Neural Network on data collected from Ford GoBike's records. The hourly_visits_by_station_daily_sf.csv file will be our main file for training and testing (see below for details on files and directories). The input and output behavior of our network is described below (based on the columns we have in the file):  

Input Columns: hour, weekday, station name    
Output: number of visits  

The anticipated usage is to check the predicted general number of people who are likely to be at a given bike station at a certain hour of a weekday or weekend. We use bike casualty data to corroborate intersections which may benefit from additional bike safety infrastructure.  

## Directories and Files  
* bikesafety-data-wrangling.ipynb - Notebook used to brainstorm model structure and create associated data files  
* bikesafety-data-wrangling.py - Notebook (identical to data wrangling notebook) saved as python file  
* hourly_visits_by_station_daily_sf.csv - Unzip the compressed file to get a CSV file with number of visits recorded for every SF station, at hourly points every day. This CSV can be directly loaded into a pandas dataframe. This was the main output of the python data wrangling notebook.  
