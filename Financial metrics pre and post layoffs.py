# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:41:07 2024

@author: barab
"""

import pandas as pd
import matplotlib.pyplot as plt

layoffs_warn = pd.read_csv('C:/Users/barab/Downloads/Layoffs-FAANG-WARN.csv')
layoffs_fyi = pd.read_csv('C:/Users/barab/Downloads/Layoffs-FAANG-FYI.csv')
interest_rates = pd.read_csv('C:/Users/barab/Downloads/Federal-Interest-Rates.csv')
quarterly_faang = pd.read_csv('C:/Users/barab/Downloads/Quarterly-FAANG-WRDS.csv')
annual_faang = pd.read_csv('C:/Users/barab/Downloads/Annual-FAANG-WRDS.csv')
daily_faang = pd.read_csv('C:/Users/barab/Downloads/Daily-FAANG-WRDS.csv')

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
    


