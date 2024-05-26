# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:10:37 2024

@author: barab
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
layoffs_warn = pd.read_csv('C:/Users/barab/Downloads/Layoffs-FAANG-WARN.csv')
layoffs_fyi = pd.read_csv('C:/Users/barab/Downloads/Layoffs-FAANG-FYI.csv')
interest_rates = pd.read_csv('C:/Users/barab/Downloads/Federal-Interest-Rates.csv')
quarterly_faang = pd.read_csv('C:/Users/barab/Downloads/Quarterly-FAANG-WRDS.csv')
annual_faang = pd.read_csv('C:/Users/barab/Downloads/Annual-FAANG-WRDS.csv')
daily_faang = pd.read_csv('C:/Users/barab/Downloads/Daily-FAANG-WRDS.csv')

# Convert date columns to datetime for accurate sorting and merging
layoffs_warn['Layoff Date'] = pd.to_datetime(layoffs_warn['Layoff Date'])
interest_rates['DATE'] = pd.to_datetime(interest_rates['DATE'])

# Perform an asof merge to find the closest interest rate date to each layoff date
layoffs_interest_merged = pd.merge_asof(layoffs_warn.sort_values('Layoff Date'), 
                                        interest_rates.sort_values('DATE'), 
                                        left_on='Layoff Date', 
                                        right_on='DATE', 
                                        direction='nearest')  # Matches the closest interest rate date to each layoff

# Filter the merged data to start from January 1, 2019
filtered_data = layoffs_interest_merged[layoffs_interest_merged['Layoff Date'] >= pd.Timestamp('2019-01-01')]

# Plotting to visualize the relationship
plt.figure(figsize=(10, 6))

# First plot (layoffs)
ax1 = plt.gca()  # Get current axes
line1 = ax1.plot(filtered_data['Layoff Date'], filtered_data['Employees Laid Off'], label='Number of Layoffs', color='blue')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Layoffs')
ax1.tick_params(axis='y')

# Second plot (interest rates) on a twin axis
ax2 = ax1.twinx()
line2 = ax2.plot(filtered_data['Layoff Date'], filtered_data['FEDFUNDS'], label='Interest Rate', color='red', linestyle='--')
ax2.set_ylabel('Interest Rate')
ax2.tick_params(axis='y')

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

plt.title('General Interest Rate Trends and Layoffs from 2019 Onwards')
plt.show()
