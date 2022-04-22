# This document is created to highlight the steps involved to do the BOL ETL assignment

# Requirements & Tools
- Pycharm (Python version 3.7)

Python Libraries-
requests
pandas as pd
logging
traceback
argparse
json
json_normalize
datetime, timedelta


# Provided input -

Web link for API to fetch Amsterdam weather data in json  format
http://api.weatherapi.com/v1/history.json?key=8c644742fcb74af688d95601220601&q=Amsterdam

For this project, I have used json to parse the data from the external API


# Command to run the script:
1. python Assignment2.py

### When run using the above command-
The script will by default run for the current date and save the desired output 
in a csv file. 

2. python Assignment2.py --startDate 2022-04-19 --endDate 2021-04-21 

### When run using the above command-
The script will bypass the default values and run for the provided input range. This can be helpful for automation or 
to run the script for adhoc dates. It can save multiple files in csv format as per requirement.

