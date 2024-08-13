#!/usr/bin/env python
# coding: utf-8

# This is the script for getting data from the Census American Community Survey API

# In[1]:


import requests
import pandas as pd
# Replace with your Census API key
API_KEY = 'You Enter Your API Key Here'

# Base URL for the API (ACS 5-Year Estimates)
BASE_URL = 'https://api.census.gov/data/2020/acs/acs5'

# Function to fetch data from the Census API and save it to a CSV file
def fetch_and_save_data(params, filename):
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print(f"Error: {response.status_code}")

# 1. Population by Age Group
params_age = {
    'get': 'NAME,B01001_001E,B01001_002E,B01001_026E',  # Total, Male, Female
    'for': 'state:*',
    'key': API_KEY
}
fetch_and_save_data(params_age, 'population_by_age.csv')

# 2. Race and Ethnicity
params_race = {
    'get': 'NAME,B02001_001E,B02001_002E,B02001_003E,B02001_005E,B03002_012E',  # Total, White, Black, Asian, Hispanic
    'for': 'state:*',
    'key': API_KEY
}
fetch_and_save_data(params_race, 'race_and_ethnicity.csv')

# 3. Educational Attainment
params_education = {
    'get': 'NAME,B15003_001E,B15003_017E,B15003_018E,B15003_021E,B15003_022E',  # Total, High School Grad, Some College, Bachelor's, Graduate/Professional
    'for': 'state:*',
    'key': API_KEY
}
fetch_and_save_data(params_education, 'educational_attainment.csv')

# 4. Median Household Income
params_income = {
    'get': 'NAME,B19013_001E',  # Median Household Income
    'for': 'state:*',
    'key': API_KEY
}
fetch_and_save_data(params_income, 'median_household_income.csv')


# In[3]:


import pandas as pd
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



# Base URL template for the ACS 1-Year Estimates API
BASE_URL_TEMPLATE = 'https://api.census.gov/data/{year}/acs/acs1'

# Create a session with retries
session = requests.Session()
retry = Retry(
    total=5,  # Total number of retries
    backoff_factor=1,  # Wait 1, 2, 4, 8, 16 seconds between retries
    status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Function to fetch data from the Census API and save it to a CSV file
def fetch_and_save_data(params, year, filename):
    base_url = BASE_URL_TEMPLATE.format(year=year)
    try:
        response = session.get(base_url, params=params)
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()

            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            df['Year'] = year  # Add the year column

            # Append or create the file
            if os.path.exists(filename):
                df.to_csv(filename, mode='a', header=False, index=False)
            else:
                df.to_csv(filename, index=False)

            print(f"Data for {year} saved to {filename}")
        else:
            print(f"Error {response.status_code} for year {year}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for year {year}: {e}")

# Years to collect data for
years = list(range(2005, 2020))  # Collect from 2005 to 2019

# 1. Population by Age Group
params_age = {
    'get': 'NAME,B01001_001E,B01001_002E,B01001_026E',  # Total, Male, Female
    'for': 'state:*',
    'key': API_KEY
}
for year in years:
    fetch_and_save_data(params_age, year, 'population_by_age_historical_1year.csv')

# 2. Race and Ethnicity
params_race = {
    'get': 'NAME,B02001_001E,B02001_002E,B02001_003E,B02001_005E,B03002_012E',  # Total, White, Black, Asian, Hispanic
    'for': 'state:*',
    'key': API_KEY
}
for year in years:
    fetch_and_save_data(params_race, year, 'race_and_ethnicity_historical_1year.csv')

# 3. Educational Attainment
params_education = {
    'get': 'NAME,B15003_001E,B15003_017E,B15003_018E,B15003_021E,B15003_022E',  # Total, High School Grad, Some College, Bachelor's, Graduate/Professional
    'for': 'state:*',
    'key': API_KEY
}
for year in years:
    fetch_and_save_data(params_education, year, 'educational_attainment_historical_1year.csv')

# 4. Median Household Income
params_income = {
    'get': 'NAME,B19013_001E',  # Median Household Income
    'for': 'state:*',
    'key': API_KEY
}
for year in years:
    fetch_and_save_data(params_income, year, 'median_household_income_historical_1year.csv')


