# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:42:01 2024

@author: barab
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the datasets
layoffs_warn = pd.read_csv('C:/Users/barab/Downloads/Layoffs-FAANG-WARN.csv')
layoffs_fyi = pd.read_csv('C:/Users/barab/Downloads/Layoffs-FAANG-FYI.csv')
interest_rates = pd.read_csv('C:/Users/barab/Downloads/Federal-Interest-Rates.csv')
quarterly_faang = pd.read_csv('C:/Users/barab/Downloads/Quarterly-FAANG-WRDS.csv')
annual_faang = pd.read_csv('C:/Users/barab/Downloads/Annual-FAANG-WRDS.csv')
daily_faang = pd.read_csv('C:/Users/barab/Downloads/Daily-FAANG-WRDS.csv')

# Calculate EPS and EBITDA if not already in the dataset
# Earnings Per Share (EPS)
quarterly_faang['EPS'] = quarterly_faang['niq'] / quarterly_faang['cshoq']

# Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)
quarterly_faang['EBIT'] = quarterly_faang['niq'] + quarterly_faang['xintq'] + quarterly_faang['txtq']
quarterly_faang['EBITDA'] = quarterly_faang['EBIT'] + quarterly_faang['dpq']

interest_rates['DATE'] = pd.to_datetime(interest_rates['DATE'])
layoffs_warn['Layoff Date'] = pd.to_datetime(layoffs_warn['Layoff Date'])
quarterly_faang['datadate'] = pd.to_datetime(quarterly_faang['datadate'])
daily_faang['datadate'] = pd.to_datetime(daily_faang['datadate'])

layoffs_warn['Normalized Company Name'] = layoffs_warn['Company Name'].str.upper().str.strip()
quarterly_faang['Normalized Company Name'] = quarterly_faang['conm'].str.upper().str.strip()

### Tesla ###
tesla_data = quarterly_faang[quarterly_faang['Normalized Company Name'] == 'TESLA INC']
tesla_layoffs = layoffs_warn[layoffs_warn['Normalized Company Name'] == 'TESLA']

# Plotting EPS and EBITDA over time
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot EPS on primary y-axis
ax1.set_xlabel('Date')
ax1.set_ylabel('EPS', color='black')  # Set text color to black
ax1.plot(tesla_data['datadate'], tesla_data['EPS'], color='tab:red', label='EPS')
ax1.tick_params(axis='y', labelcolor='black')  # Set ticks to black

# Instantiate a second axes that shares the same x-axis for EBITDA
ax2 = ax1.twinx()
ax2.set_ylabel('EBITDA', color='black')  # Set text color to black
ax2.plot(tesla_data['datadate'], tesla_data['EBITDA'], color='tab:blue', label='EBITDA')
ax2.tick_params(axis='y', labelcolor='black')  # Set ticks to black

# Overlay layoff dates
for layoff_date in tesla_layoffs['Layoff Date']:
    plt.axvline(x=layoff_date, color='grey', linestyle='--', label='Layoff Date' if 'Layoff Date' not in plt.gca().get_legend_handles_labels()[1] else "")

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

fig.tight_layout()  # Adjust layout to make room for labels
plt.title('Financial Performance Over Time for Tesla')
plt.show()

### Microsoft ###
microsoft_data = quarterly_faang[quarterly_faang['Normalized Company Name'] == 'MICROSOFT CORP']
microsoft_layoffs = layoffs_warn[layoffs_warn['Normalized Company Name'] == 'MICROSOFT']

# Plotting EPS and EBITDA over time
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot EPS on primary y-axis
ax1.set_xlabel('Date')
ax1.set_ylabel('EPS', color='black')  # Set text color to black
ax1.plot(microsoft_data['datadate'], microsoft_data['EPS'], color='tab:red', label='EPS')
ax1.tick_params(axis='y', labelcolor='black')  # Set ticks to black

# Instantiate a second axes that shares the same x-axis for EBITDA
ax2 = ax1.twinx()
ax2.set_ylabel('EBITDA', color='black')  # Set text color to black
ax2.plot(microsoft_data['datadate'], microsoft_data['EBITDA'], color='tab:blue', label='EBITDA')
ax2.tick_params(axis='y', labelcolor='black')  # Set ticks to black

# Overlay layoff dates
for layoff_date in microsoft_layoffs['Layoff Date']:
    plt.axvline(x=layoff_date, color='grey', linestyle='--', label='Layoff Date' if 'Layoff Date' not in plt.gca().get_legend_handles_labels()[1] else "")

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

fig.tight_layout()  # Adjust layout to make room for labels
plt.title('Financial Performance Over Time for Microsoft')
plt.show()

### Meta ###
meta_data = quarterly_faang[quarterly_faang['Normalized Company Name'] == 'META PLATFORMS INC']
meta_layoffs = layoffs_warn[layoffs_warn['Normalized Company Name'] == 'META']

# Plotting EPS and EBITDA over time
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot EPS on primary y-axis
ax1.set_xlabel('Date')
ax1.set_ylabel('EPS', color='black')  # Set text color to black
ax1.plot(meta_data['datadate'], meta_data['EPS'], color='tab:red', label='EPS')
ax1.tick_params(axis='y', labelcolor='black')  # Set ticks to black

# Instantiate a second axes that shares the same x-axis for EBITDA
ax2 = ax1.twinx()
ax2.set_ylabel('EBITDA', color='black')  # Set text color to black
ax2.plot(meta_data['datadate'], meta_data['EBITDA'], color='tab:blue', label='EBITDA')
ax2.tick_params(axis='y', labelcolor='black')  # Set ticks to black

# Overlay layoff dates
for layoff_date in meta_layoffs['Layoff Date']:
    plt.axvline(x=layoff_date, color='grey', linestyle='--', label='Layoff Date' if 'Layoff Date' not in plt.gca().get_legend_handles_labels()[1] else "")

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

fig.tight_layout()  # Adjust layout to make room for labels
plt.title('Financial Performance Over Time for Meta')
plt.show()

### Overall ###
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Assuming quarterly_faang and layoffs_warn are already loaded and prepared
# Normalize company names if not already done
quarterly_faang['Normalized Company Name'] = quarterly_faang['conm'].str.upper().str.strip()
layoffs_warn['Normalized Company Name'] = layoffs_warn['Company Name'].str.upper().str.strip()

# Convert dates to datetime if not already done
quarterly_faang['datadate'] = pd.to_datetime(quarterly_faang['datadate'])
layoffs_warn['Layoff Date'] = pd.to_datetime(layoffs_warn['Layoff Date'])

# Filter data to start from 2020
quarterly_faang = quarterly_faang[quarterly_faang['datadate'] >= pd.Timestamp('2020-01-01')]
layoffs_warn = layoffs_warn[layoffs_warn['Layoff Date'] >= pd.Timestamp('2020-01-01')]

# Group data by date and calculate mean EPS and EBITDA
grouped_data = quarterly_faang.groupby('datadate').agg({'EPS': 'mean', 'EBITDA': 'mean'}).reset_index()

# Plotting
fig, ax1 = plt.subplots(figsize=(14, 7))

# EPS on primary y-axis
ax1.set_xlabel('Date')
ax1.set_ylabel('EPS', color='black')  # Set text color to black for the label
ax1.plot(grouped_data['datadate'], grouped_data['EPS'], color='tab:red', label='Average EPS')
ax1.tick_params(axis='y', colors='black')  # Set ticks to black

# EBITDA on secondary y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('EBITDA', color='black')  # Set text color to black for the label
ax2.plot(grouped_data['datadate'], grouped_data['EBITDA'], color='tab:blue', label='Average EBITDA')
ax2.tick_params(axis='y', colors='black')  # Set ticks to black

# Layoff information - simple count of layoffs per month/year as an area plot
layoff_counts = layoffs_warn['Layoff Date'].dt.to_period('M').value_counts().sort_index()
layoff_dates = layoff_counts.index.to_timestamp()  # Convert periods back to timestamps for plotting
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.fill_between(layoff_dates, 0, layoff_counts.values, color='grey', alpha=0.3, label='Layoffs')
ax3.set_ylabel('Number of Layoffs', color='black')
ax3.tick_params(axis='y', colors='black')

# Legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax2.legend(lines + lines2 + lines3, labels + labels2 + labels3, loc='upper left')

plt.title('Sector Financial Performance and Layoffs Over Time Since 2020')
plt.show()
