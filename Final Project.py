# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:01:43 2024

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

# Calculate EPS and EBITDA
# Earnings Per Share (EPS)
quarterly_faang['EPS'] = quarterly_faang['niq'] / quarterly_faang['cshoq']

# Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)
quarterly_faang['EBIT'] = quarterly_faang['niq'] + quarterly_faang['xintq'] + quarterly_faang['txtq']
quarterly_faang['EBITDA'] = quarterly_faang['EBIT'] + quarterly_faang['dpq']

interest_rates['DATE'] = pd.to_datetime(interest_rates['DATE'])
layoffs_warn['Layoff Date'] = pd.to_datetime(layoffs_warn['Layoff Date'])
quarterly_faang['datadate'] = pd.to_datetime(quarterly_faang['datadate'])
daily_faang['datadate'] = pd.to_datetime(daily_faang['datadate'])


### FINANCIAL METRICS PRE AND POST LAYOFFS ###
# Earnings Per Share (EPS)
quarterly_faang['EPS'] = quarterly_faang['niq'] / quarterly_faang['cshoq']

# Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)
quarterly_faang['EBIT'] = quarterly_faang['niq'] + quarterly_faang['xintq'] + quarterly_faang['txtq']
quarterly_faang['EBITDA'] = quarterly_faang['EBIT'] + quarterly_faang['dpq']

quarterly_faang['Operating Margin'] = quarterly_faang['oibdpq'] / quarterly_faang['revtq']
quarterly_faang['Debt to Equity Ratio'] = quarterly_faang['ltq'] / quarterly_faang['teqq']
quarterly_faang['ROA'] = quarterly_faang['niq'] / quarterly_faang['actq']
quarterly_faang['ROE'] = quarterly_faang['niq'] / quarterly_faang['teqq']
quarterly_faang['Free Cash Flow'] = quarterly_faang['oancfy'] - quarterly_faang['capxy']
quarterly_faang['Current Ratio'] = quarterly_faang['actq'] / quarterly_faang['lctq']

from scipy.stats.mstats import winsorize

# Winsorize the financial ratios at the 5th and 95th percentiles
financial_ratios = ['EPS', 'EBITDA', 'Operating Margin', 'Debt to Equity Ratio', 
                    'ROA', 'ROE', 'Free Cash Flow', 'Current Ratio']

# Applying winsorization to each financial ratio column
for ratio in financial_ratios:
    quarterly_faang[ratio] = winsorize(quarterly_faang[ratio], limits=[0.05, 0.05])

### Improvements in financial metrics after layoffs ###
# Convert dates to datetime for accurate sorting and manipulation
layoffs_warn['Layoff Date'] = pd.to_datetime(layoffs_warn['Layoff Date'])
quarterly_faang['datadate'] = pd.to_datetime(quarterly_faang['datadate'])

### For all companies except Apple ###
# Normalize company names
layoffs_warn['Normalized Company Name'] = layoffs_warn['Company Name'].str.upper().str.strip()
quarterly_faang['Normalized Company Name'] = quarterly_faang['conm'].str.upper().str.strip()

# Apply common names normalization for both datasets
common_names = {
    'MICROSOFT CORP': 'MICROSOFT',
    'AMAZON.COM INC': 'AMAZON',
    'NETFLIX INC': 'NETFLIX',
    'ALPHABET INC': 'GOOGLE',
    'META PLATFORMS INC': 'META',
    'TESLA INC': 'TESLA' 
    }

layoffs_warn['Normalized Company Name'] = layoffs_warn['Normalized Company Name'].apply(
    lambda x: common_names.get(x, x)
)
quarterly_faang['Normalized Company Name'] = quarterly_faang['Normalized Company Name'].apply(
    lambda x: common_names.get(x, x)
)

# Get unique company names from one of the datasets after normalization
unique_companies = layoffs_warn['Normalized Company Name'].unique()

# Dictionary to store results
results = {}

# Identify the year with the most layoffs for each company
layoffs_by_company_and_year = layoffs_warn.groupby(['Normalized Company Name', 'Year']).size().reset_index(name='Layoff Count')
year_of_most_layoffs = layoffs_by_company_and_year.loc[layoffs_by_company_and_year.groupby('Normalized Company Name')['Layoff Count'].idxmax()]

# Calculate metrics for the identified year
for _, row in year_of_most_layoffs.iterrows():
    company, layoff_year = row['Normalized Company Name'], row['Year']
    company_data = quarterly_faang[quarterly_faang['Normalized Company Name'] == company]
    
    # Pre-layoff metrics are from quarters before the identified year
    pre_layoff_data = company_data[company_data['datadate'].dt.year < layoff_year]
    # Post-layoff metrics are from quarters during and after the identified year
    post_layoff_data = company_data[company_data['datadate'].dt.year >= layoff_year]
    
    pre_eps = pre_layoff_data['EPS'].mean()
    post_eps = post_layoff_data['EPS'].mean()
    pre_ebitda = pre_layoff_data['EBITDA'].mean()
    post_ebitda = post_layoff_data['EBITDA'].mean()
    pre_operatingmargin = pre_layoff_data['Operating Margin'].mean()
    post_operatingmargin = post_layoff_data['Operating Margin'].mean()
    pre_debttoequity = pre_layoff_data['Debt to Equity Ratio'].mean()
    post_debttoequity = post_layoff_data['Debt to Equity Ratio'].mean()
    pre_roa = pre_layoff_data['ROA'].mean()
    post_roa = post_layoff_data['ROA'].mean()
    pre_roe = pre_layoff_data['ROE'].mean()
    post_roe = post_layoff_data['ROE'].mean()
    pre_freecashflow = pre_layoff_data['Free Cash Flow'].mean()
    post_freecashflow = post_layoff_data['Free Cash Flow'].mean()
    pre_currentratio = pre_layoff_data['Current Ratio'].mean()
    post_currentratio = post_layoff_data['Current Ratio'].mean()

    # Store results
    results[company] = {
        'Year of Most Layoffs': layoff_year,
        'Average EPS Before Layoffs': pre_eps,
        'Average EPS After Layoffs': post_eps,
        'Average EBITDA Before Layoffs': pre_ebitda,
        'Average EBITDA After Layoffs': post_ebitda,
        'Average Operating Margin Before Layoffs':pre_operatingmargin,
        'Average Operating Margin After Layoffs':post_operatingmargin,
        'Average Debt to Equity Before Layoffs':pre_debttoequity,
        'Average Debt to Equity After Layoffs':post_debttoequity,
        'Average ROA Before Layoffs':pre_roa,
        'Average ROA After Layoffs':post_roa,
        'Average ROE Before Layoffs':pre_roe,
        'Average ROE After Layoffs':post_roe,
        'Average Free Cash Flow Before Layoffs':pre_freecashflow,
        'Average Free Cash Flow After Layoffs':post_freecashflow,
        'Average Current Ratio Before Layoffs':pre_currentratio,
        'Average Current Ratio After Layoffs':post_currentratio
    }

# Output the results
for company, metrics in results.items():
    print(f"Results for {company}:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print("\n")
    

### OVERALL MARKET REACTION TO LAYOFFS ###
## BY COMPANY ##
import pandas as pd
import matplotlib.pyplot as plt

# Load data
# Assuming 'quarterly_faang' is already loaded and contains stock prices with 'prccq' representing the closing price
# Ensure datetime conversion
quarterly_faang['datadate'] = pd.to_datetime(quarterly_faang['datadate'])

# Assuming layoffs_warn is already loaded and it contains the layoff dates with 'Ticker' as the company identifier
layoffs_warn['Layoff Date'] = pd.to_datetime(layoffs_warn['Layoff Date'])

# Choose a company ticker symbol to analyze
company_ticker = 'META'  

# Get the company's stock price data and calculate returns
company_prices = quarterly_faang[quarterly_faang['tic'] == company_ticker].copy()
company_prices.sort_values('datadate', inplace=True)
company_prices['Returns'] = company_prices['prccq'].pct_change()

# Get the layoff dates for the chosen company
company_layoffs = layoffs_warn[layoffs_warn['Ticker'] == company_ticker]

# Plot the stock returns
plt.figure(figsize=(14, 7))
plt.plot(company_prices['datadate'], company_prices['Returns'], label='Quarterly Returns')

# Create a legend entry for layoff dates
# We use a dummy plot here with no data (empty lists) just for the legend entry
plt.plot([], [], color='red', linestyle='--', linewidth=1, label='Layoff Announcements')

# Plot each layoff event on the same graph
for layoff_date in company_layoffs['Layoff Date']:
    plt.axvline(x=layoff_date, color='red', linestyle='--', linewidth=1)

# Enhance the graph with title, labels, and legend
plt.title(f'Stock Market Reaction to Layoffs for {company_ticker}')
plt.xlabel('Date')
plt.ylabel('Quarterly Returns')
plt.legend()
plt.grid(True)
plt.show()

## OVERALL ##
# Filter data from 2020 onwards
quarterly_faang = quarterly_faang[quarterly_faang['datadate'].dt.year >= 2020]
layoffs_warn = layoffs_warn[layoffs_warn['Layoff Date'].dt.year >= 2020]

# Verify 'datadate' and 'prccq' exist in the dataframe
if 'datadate' not in quarterly_faang.columns or 'prccq' not in quarterly_faang.columns:
    raise KeyError("The 'datadate' and/or 'prccq' columns are missing from quarterly_faang dataframe")

# Calculate returns for each ticker symbol, then calculate the average return per date
quarterly_faang['Returns'] = quarterly_faang.groupby('tic')['prccq'].pct_change()
average_returns_by_date = quarterly_faang.groupby('datadate')['Returns'].mean()

# Aggregate layoffs for all companies by date
all_company_layoffs = layoffs_warn.groupby('Layoff Date')['Ticker'].size()

# Plot the aggregate stock returns
plt.figure(figsize=(14, 7))
plt.plot(average_returns_by_date.index, average_returns_by_date.values, label='Average Quarterly Returns', color='black')

# Plot layoff dates for all companies
for layoff_date in all_company_layoffs.index:
    plt.axvline(x=layoff_date, color='red', linestyle='--', linewidth=1)

# Create a custom legend
plt.legend(['Average Quarterly Returns', 'Layoff Announcements'], loc='best')

# Enhance the graph with title, labels, and legend
plt.title('Overall Market Reaction to Layoffs Since 2020')
plt.xlabel('Date')
plt.ylabel('Aggregate Quarterly Returns')
plt.grid(True)
plt.show()


### COMPARING EPS AND EBITDA ###
## BY COMPANY ##
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

## OVERALL ##
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


### INTEREST RATES AND LAYOFFS ###
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
