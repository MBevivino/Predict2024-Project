#!/usr/bin/env python
# coding: utf-8

# This script will serve all purposes related to data collection regarding polling data. This includes federal polls, state polls and so on. 

# In[4]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests


# ## Data Entry
# Below is the code for a simple program for entering polling data. It will ask the user for information about the polls, like candidate info and whether or not it is a nationwide or a state poll. 

# In[ ]:


import pandas as pd
import os
from datetime import datetime

def get_poll_data():
    polls = []

    while True:
        poll = {}

        # Determine if it's a federal or state poll
        poll_type = input("Is this a Federal or State poll? (Enter 'federal' or 'state'): ").strip().lower()
        if poll_type == 'federal':
            poll['Type'] = 'Federal'
            poll['Race'] = input("Enter the race (e.g., 'Presidential', 'Senate', 'House'): ").strip()
        elif poll_type == 'state':
            poll['Type'] = 'State'
            poll['State'] = input("Enter the state (e.g., 'Arizona', 'Texas'): ").strip()
            poll['Race'] = input("Enter the race (e.g., 'Governor', 'Senate', 'House'): ").strip()
        else:
            print("Invalid input. Please enter 'federal' or 'state'.")
            continue

        # Common poll data for both types
        poll['Pollster'] = input("Enter the name of the polling organization (Pollster): ").strip()
        poll['Date'] = input("Enter the date of the poll (e.g., '2024-08-10'): ").strip()
        poll['Sample Size'] = input("Enter the sample size: ").strip()
        poll['Margin of Error'] = input("Enter the margin of error (e.g., '±3.0%'): ").strip()
        
        # Candidate results
        candidates = input("Enter the candidates and their percentages (e.g., 'Candidate1 48%, Candidate2 45%'): ").strip()
        poll['Results'] = candidates

        # Save poll data to list
        polls.append(poll)

        # Ask if the user wants to enter another poll
        another = input("Do you want to enter another poll? (yes/no): ").strip().lower()
        if another != 'yes':
            break

    return polls

def save_to_csv(polls, filename='polls_dataset.csv'):
    # Check if file exists
    if os.path.exists(filename):
        print(f"File '{filename}' already exists.")
        action = input("Do you want to (a)ppend data, (o)verwrite the file, (b)ackup the existing file, or (c)ancel? ").strip().lower()
        if action == 'a':
            # Append to existing file
            df_existing = pd.read_csv(filename)
            df_new = pd.DataFrame(polls)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(filename, index=False)
            print(f"Data appended to {filename}")
        elif action == 'o':
            # Overwrite the file
            df = pd.DataFrame(polls)
            df.to_csv(filename, index=False)
            print(f"File '{filename}' has been overwritten.")
        elif action == 'b':
            # Backup the existing file
            backup_filename = f"{filename.split('.')[0]}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
            os.rename(filename, backup_filename)
            df = pd.DataFrame(polls)
            df.to_csv(filename, index=False)
            print(f"Existing file backed up as '{backup_filename}'. New data saved to '{filename}'.")
        else:
            print("Operation cancelled.")
    else:
        # Save new file if it doesn't exist
        df = pd.DataFrame(polls)
        df.to_csv(filename, index=False)
        print(f"Dataset saved to {filename}")

if __name__ == "__main__":
    # Get the polling data
    poll_data = get_poll_data()

    # Save to CSV
    save_to_csv(poll_data)


