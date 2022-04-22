# import libraries
import requests
import pandas as pd
import logging as logger
import traceback
import argparse
import json
from pandas import json_normalize
from datetime import datetime, timedelta

"""
This  script is used to fetch the Weather data from an external API and store as csv file
"""


try:
    # get dynamic variables for startDate and endDate
    # Default value - startDate = endDate = current_date
    # these values can be passed dynamically if the requirement is to run the script for multiple days at a time
    # or to run this script for any particular day other than the current day

    parser = argparse.ArgumentParser(description='Weather data')
    parser.add_argument("--startDate", default=datetime.now().date())
    parser.add_argument("--endDate",  default=datetime.now().date())


    # parse dynamic arguments/take default
    args = parser.parse_args()
    startDate = args.startDate
    if type(startDate) == str:
        # This block is entered when startDate is fetched dynamically
        #
        if (datetime.strptime(startDate, '%Y-%m-%d')< datetime.strptime(str(datetime.now().date()),'%Y-%m-%d') - timedelta(days=7)):
            startDate = (datetime.strptime(str(datetime.now().date()),'%Y-%m-%d') - timedelta(days=7)).date()
        else:
            startDate = datetime.strptime(startDate, '%Y-%m-%d').date()

    endDate = args.endDate
    if type(endDate) == str:
        # This block is entered when endDate is fetched dynamically
        endDate = datetime.strptime(endDate, '%Y-%m-%d').date()
        if endDate<startDate:
            startDate = endDate
            print("Start date was greater than end date so it is replaced with end date")


except Exception as ex:
    logger.error('Unexpected error: ' + traceback.format_exc())
    logger.error(ex.message)


# This is the main block from where code execution will start
if __name__ == '__main__':
    final_df = pd.DataFrame()
    while str(startDate) <= str(endDate):
        # api link to fetch exchange rates
        api_link = 'http://api.weatherapi.com/v1/history.json?key=8c644742fcb74af688d95601220601&q=Amsterdam&dt={date}'.format(date=str(startDate))

        # get the weather data from the api
        json_data = requests.get(api_link).content
        # print(json_data)

        # Use json_normalize() to convert JSON to DataFrame
        dict = json.loads(json_data)
        df2 = json_normalize(dict)

        # normalize nested json data and add to the main dataframe
        forecast_day = json_normalize(df2['forecast.forecastday'])
        forecast_day = forecast_day[0].apply(pd.Series)

        forecast_day_hour = json_normalize(forecast_day['hour'])
        forecast_day_hour = forecast_day_hour[0].apply(pd.Series)

        # COncat all columns od dataset
        df = pd.concat([df2.drop('forecast.forecastday', axis=1), forecast_day], axis=1)
        df.columns=df.columns.str.replace('.', '_')

        # Add date wise data to final dataset
        if final_df.empty:
            final_df = df
            final_df.columns = df.columns
        else:
            final_df = final_df.append(df)

        startDate += timedelta(days=1)

        # Write weather data to csv
        final_df.to_csv('amsterdam_weather_data.csv', index =0)