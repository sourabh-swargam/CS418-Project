# -*- coding: utf-8 -*-
"""Time Series Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iHgThGX8AOOZT_N2hjY-aheP9W69J_T2

## Objective
Our goal was to "analyse and forecast the energy usage in an urban city".

## Data
The source of the data is the following link: [LINK](https://data.world/houston/houston-electricity-bills)

There are 4 files, they are:
1. July 2011 to June 2012 excel file - 57,430 rows and 24 columns
2. May 2012 to April 2013 excel file - 65,806 rows and 24 columns
3. July 2012 to June 2013 excel file - 66,776 rows and 24 columns
4. July 2013 to June 2014 excel file - 67,838 rows and 24 columns

The data tables contain information regarding the building address, location, service number, billing dates, total amount due. 

The plan is to go through and clean the data tables individually and make them consistent. Once that is done the next step is to merge the cleaned data tables. After merging the tables one important check is to search for duplicates since there is an overlap of dates it is highly likely that there will be duplicates.

Description of each column 
1. Reliant Contract No: A unique identifier for each contract. 
2. Service Address: Address for the service location
3. Meter No: Meter number for the service location.
4. ESID: Electric Service Identifier for the service location.
5. Business Area: Business area code for the service location.
6. Cost Center: Cost center code for the service location.
7. Fund: Fund code for the service location.
8. Bill Type: Type of bill (e.g. "T" for "Total", "P" for "Partial", etc.). 
9. Bill Date: Date the bill was generated. 
10. Read Date: Date the meter was read. 
11. Due Date: Due date for the bill. 
12. Meter Read: Meter reading for the service location. 
13. Base Cost: TBase cost for the service. 
14. T&D Discretionary: Transmission and Distribution Discretionary charge for the service. 
15. T&D Charges: Transmission and Distribution charge for the service. 
16. Current Due: Current due amount for the service.
17. Index Charge: Index charge for the service. 
18. Total Due: Total due amount for the service. 
19. Franchise Fee: Franchise fee for the service. 
20. Voucher Date: Date the voucher was issued for the service. 
21. Billed Demand: Billed demand for the service in KVA. 
22. kWh Usage: Kilowatt-hour usage for the service. 
23. Nodal Cu Charge:  Nodal Cu Charge for the service. 
24. Adder Charge:  Adder Charge for the service.

Statistical Data Type of Each Column 
1. Reliant Contract No: integer (ratio)
2. Service Address: string (nominal)
3. Meter No: integer (nominal)
4. ESID: integer (nominal)
5. Business Area: integer (ratio))
6. Cost Center: integer (ratio)
7. Fund: integer (ratio)
8. Bill Type: string (nominal)
9. Bill Date: date (nominal)
10. Read Date: date (nominal)
11. Due Date: date (nominal)
12. Meter Read: integer (ratio)
13. Base Cost: float (nominal)
14. T&D Discretionary: float (nominal)
15. T&D Charges: float (nominal)
16. Current Due: float (nominal)
17. Index Charge: float (nominal)
18. Total Due: float (nominal)
19. Franchise Fee: float (nominal)
20. Voucher Date: date (nominal)
21. Billed Demand (KVA): integer (nominal)
22. kWh Usage: integer (nominal)
23. Nodal Cu Charge: float (nominal)
24. Adder Charge: float (nominal)

## Problem
The key issue in generating electricity is to determine how much capacity to generate in order to meet future demand. 

Electricity usage forecasting involves predicting the demand for electricity over a specific eriod. This process has several uses, including energy procurement, where it helps suppliers purchase the right amount of energy to ensure a steady supply.

The advancement of smart infrastructure and integration of distributed renewable power has raised future supply, demand, and pricing uncertainties. This unpredictability has increased interest in price prediction and energy analysis.

## Research Question
I worked on the following research question: \
Previous electricity usage data can be used for predicting the usage for future (Time-Series)

## Import Statements
"""

# !pip install xlrd

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, f1_score

pd.options.display.max_columns=25

"""## Mount colab file to drive"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# Insert, change the directory 
import sys
sys.path.insert(0,'/content/drive/MyDrive/CS418-Project-main')
# %cd /content/drive/MyDrive/CS418-Project-main

"""## Data FY 2012 - Hyndavi"""

data_2012 = pd.read_excel('houston-houston-electricity-bills/coh-fy2012-ee-bills-july2011-june2012.xls')
orig_shape_2012 = data_2012.shape[0]

data_2012.shape

data_2012.head(5)

"""### Checking Nulls"""

data_2012.isna().sum()

"""### Checking Adjustment ($) column"""

data_2012['Adjustment ($)'].value_counts(dropna=False)

"""The column does not have any relevant information based on the above reported values. Electing to drop the column."""

data_2012.drop(columns=['Adjustment ($)'], inplace=True)

"""### Checking Unique Number of Customers

There are quite a few columns in the dataset that signify relating to a unique person/house/business. Checking the unique counts of such columns.
"""

check_unique_columns = ['Reliant Contract No', 'Service Address ', 'Meter No', 
                        'ESID', 'Business Area', 'Cost Center',]

for col in check_unique_columns:
    print(f'Number of Unique Values in {col}: {data_2012[col].nunique()}')

"""Based on the above reported values and further research online:

ESID signifies a unique ID provided to each customer subscribed to the electricity board. It would be best to choose ESID and Service Address columns going forward as these would provide number of unique customers and the areas (streets) where higher usage of electricity occurs.

Business Area signifies a grouping a number of buildings which covers a certain area. This would be useful usage patterns grouped by certain zones in the city.

### Checking Bill Type
"""

data_2012['Bill Type'].value_counts(dropna=False)

"""Bill Type could signify the type of the connection given. Since commercial, residential and government spaces would have different type of pricing and needs this column could be capturing that information."""

data_2012['Service Address '].nunique(), data_2012['Meter No'].nunique(), data_2012['ESID'].nunique()

"""The next 3 columns are: Bill Date, Read Date and Due Date. Of these it would be best to choose the Bill date across all the data files to keep the data consistent.

### Electricity Usage Statistics
"""

data_2012[['Meter Read', 'Billed Demand ', 'kWh Usage']].describe()

"""There are 3 columns that denote the amount of electricity: Meter Read, Billed Demand, kWh Usage.

Using kWh Usage as a standard unit of measurement.
"""

data_2012[[
    'Base Cost ($)', 'T&D Discretionary ($)', 'T&D Charges ($)', 
    'Current Due ($)', 'Total Due ($)', 'Franchise Fee ($)', 
    'Nodal Cu Charge ($)', 'Reliability Unit Charge ($)'
     ]].describe()

"""Reliability Unit Charge does not contain any useful information. Electing to drop that column.

The columns other than Current Due or Total Due are adding up the value present in these two columns. Going forward choosing the column Total Due ($). 
Based on the above statistics the columns Current Due and Total Due represent the same value.

### Selecting and Filtering Columns
"""

data_2012.columns

"""Based on the above analysis of the dataset choosing the following columns:

1. ESID
2. Business Area
3. Service Address 
3. Bill Type
4. Bill Date
5. Total Due ($)
6. kWh Usage
"""

data_2012 = data_2012[[
    'ESID', 'Business Area', 'Service Address ', 'Bill Type',
    'Bill Date', 'Total Due ($)', 'kWh Usage'
]]

rename_cols = {
    'ESID': 'esid',
    'Business Area': 'business_area',
    'Service Address ': 'service_address',
    'Bill Type': 'bill_type',
    'Bill Date': 'bill_date',
    'Total Due ($)': 'total_due',
    'kWh Usage': 'kwh_usage'
}

data_2012_main = data_2012.rename(columns=rename_cols)

"""Checking for Nulls again and dtypes"""

data_2012_main.isna().sum()

data_2012_main.dtypes

data_2012_main.shape

zscore_2012 = stats.zscore(data_2012_main[['total_due', 'kwh_usage']])

zscore_2012

"""Each zscore value signifies how many standard deviations away an individual value is from the mean. This is a good indicator to finding outliers in the dataframe.

Usually z-score=3 is considered as a cut-off value to set the limit. Therefore, any z-score greater than +3 or less than -3 is considered as outlier which is pretty much similar to standard deviation method
"""

data_2012_main = data_2012_main[(np.abs(zscore_2012) < 3).all(axis=1)]

data_2012_main.shape

"""The number of rows has decreased from 57,430 to 57,025. So 405 rows were outliers based on the data."""

data_2012_main.head(5)

orig_shape_2012 - data_2012_main.shape[0]

data_2012_main.to_csv('electricity_usage_data_2012.csv', index=False)

"""The trend graph of both the cost and energy usage is the same as the value of cost = energy usage times the cost per unit.

# Merging the data

Load all the data from the files, which were cleaned and pre-processed by all the team members.
"""

data_2012_main = pd.read_csv('electricity_usage_data_2012.csv')
data_2013_main = pd.read_csv('electricity_usage_data_2013.csv')
data_2013_2_main = pd.read_csv('electricity_usage_data_2013_2.csv')
data_2014_main = pd.read_csv('electricity_usage_data_2014.csv')

"""Before merging the data, removing the outliers to make the series non-sensitive to outliers."""

# Remove outliers in data
zscore_2012 = stats.zscore(data_2012_main[['total_due', 'kwh_usage']])
print('data_2012_main shape before removing outliers: {}'.format(data_2012_main.shape))
data_2012_main = data_2012_main[(np.abs(zscore_2012) < 3).all(axis=1)]
print('data_2012_main shape after removing outliers: {}'.format(data_2012_main.shape), '\n')

zscore_2013 = stats.zscore(data_2013_main[['total_due', 'kwh_usage']])
print('data_2013_main shape before removing outliers: {}'.format(data_2013_main.shape))
data_2013_main = data_2013_main[(np.abs(zscore_2013) < 3).all(axis=1)]
print('data_2013_main shape after removing outliers: {}'.format(data_2013_main.shape), '\n')

zscore_2013_2 = stats.zscore(data_2013_2_main[['total_due', 'kwh_usage']])
print('data_2013_2_main shape before removing outliers: {}'.format(data_2013_2_main.shape))
data_2013_2_main = data_2013_2_main[(np.abs(zscore_2013_2) < 3).all(axis=1)]
print('data_2013_2_main shape after removing outliers: {}'.format(data_2013_2_main.shape), '\n')

zscore_2014 = stats.zscore(data_2014_main[['total_due', 'kwh_usage']])
print('data_2014_main shape before removing outliers: {}'.format(data_2014_main.shape))
data_2014_main = data_2014_main[(np.abs(zscore_2014) < 3).all(axis=1)]
print('data_2014_main shape after removing outliers: {}'.format(data_2014_main.shape), '\n')

"""Verify the data to check nulls, duplicate rows, and save final data into csv file"""

df_list = [data_2012_main, data_2013_main, data_2013_2_main, data_2014_main]

data = pd.concat(df_list)
print('data.shape', data.shape, '\n')

# Checking nulls in the data
print('Nulls in the data:\n', data.isna().sum(), '\n')

# Checking for duplicate rows
dup_rows_index = data.duplicated(subset=['esid', 'business_area', 'service_address', 'bill_date'])
print('duplicate rows', (dup_rows_index).sum(), '\n')

# Removing the duplicates
data_main = data[~(dup_rows_index)]
print('data_main.shape', data_main.shape, '\n')
# last result - data_main.shape (190848, 7) 

# saving into csv files
data_main.to_csv('Electricity_Usage_Data.csv', index=False)

"""# Time-Series - Hyndavi

Proposed Models:
1. VAR - can model multiple time series variables simultaneously and capture complex relationships between multiple time series variables. But this model can be sensitive to the number of lags used in the model.
2. ARIMA - Can capture the autocorrelation and trends in the time series data as well as seasonality. But it may not perform well with long term forecasting and requires turning to make it optimal
3. LSTM - can model complex relationships between time series data such as non-stationary and non-linear time series data. But it requires a lot of computational resources compared to the other models.
"""

!pip install pmdarima

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
from pmdarima.arima import auto_arima
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
from tqdm import tqdm_notebook
from itertools import product
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import math 
from statistics import mean
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

"""# Prepocessing data for Model"""

plt.rcParams.update({'font.size': 12})

data_df = pd.read_csv('Electricity_Usage_Data.csv')
address_enc = LabelEncoder()
bill_type_enc = LabelEncoder()

data_df['bill_date']=pd.to_datetime(data_df['bill_date'])
data_df['address_enc'] = address_enc.fit_transform(data_df['service_address'])
data_df['bill_type_enc'] = bill_type_enc.fit_transform(data_df['bill_type'])
data_df['year'] = data_df['bill_date'].apply(lambda x: x.year)
data_df['month'] = data_df['bill_date'].apply(lambda x: x.month)
data_df['year_month'] = data_df['bill_date'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
data_df['week'] = data_df.apply(lambda row: row['bill_date'].week+52*(int(row['year'])-2011),axis=1)

data_df.head()

data_df['year'].value_counts()
# old values - 2013    68916, 2012    62397, 2014    33023, 2011    26512
# new values - 2013    68403, 2012    61784, 2014    32827, 2011    25957

data_df['week'].value_counts()

# df = data_df[['year_month', 'kwh_usage']]
# df = df.groupby(by=['year_month']).mean()

df = data_df[['kwh_usage', 'week']]
df = df.groupby(by=['week']).mean()

plt.figure(figsize=(35, 7))

plt.grid()
plt.plot(df)

plt.title('Average Weekly Consumption of Electricity', fontsize=25)
plt.xlabel('Week', fontsize=20)
plt.ylabel('Kwh Usage', fontsize=20)

plt.tight_layout()

"""## Check whether the series is stationary?
Stationary time series is the one whose satistical properties(mean, var, etc.) donot change over time. \

We need to perform additional check to find - 

*   if the series is stationary?
*   if there is a seasonality?
*   is the target variable correlated?

We'll use Dickey-Fuller test to check if the series is stationary and make it stationary if not.

### **Rolling Statistics Method**
"""

rolling_mean = df.rolling(2).mean()
rolling_std = df.rolling(2).std()

plt.figure(figsize=(35, 8))
plt.grid()

plt.plot(df, color="blue",label="Original Usage")
plt.plot(rolling_mean, color="red", label="Rolling Mean")
plt.plot(rolling_std, color="black", label = "Rolling Standard Deviation")

plt.title('Electricity Time Series, Rolling Mean, Standard Deviation', fontsize=25)
plt.xlabel('Week', fontsize=20)
plt.ylabel('Energy Usage in Kwh', fontsize=20)

plt.legend(loc="upper left")
plt.tight_layout()

"""We see that statistics are not constant over the time, but to confirm we'll perform additional statistical test using augmented Dickey-Fuller method.

### **Augmented Dickey-Fuller Test:**
H0 = Null-hypothesis => It has unit root, the series is non-stationary \
H1 = Alternate-hypothesis => No unit root, the series is stationary

If p-value < critical value [0.05] -> We reject the null-hypothesis H0 \
If p-value > critical value [0.05] -> We fail to reject null-hypothesis H0
"""

from statsmodels.tsa.stattools import adfuller

def aug_dickey_fuller_test(df):
  adft = adfuller(df, autolag="AIC")
  output_df = pd.DataFrame({"Values":[adft[0],adft[1],adft[2],adft[3], adft[4]['1%'], adft[4]['5%'], adft[4]['10%']], 
                            "Metric":["Test Statistics","p-value","No. of lags used","Number of observations used", "critical value (1%)", "critical value (5%)", "critical value (10%)"]})
  print(output_df)

aug_dickey_fuller_test(df)

"""### Dickey-Fuller Test Result:

As (Test Statistics -1.83 > -2.88 critical value (5%)), p-value > 0.05, we fail to reject the null-hypothesis, and thus the time series is non-stationary.

## Make the time series stationary
"""

# First we'll perform differencing on the data to see if it becomes stationary
diff_df = df.diff()

plt.figure(figsize=(32, 8))
plt.grid()
plt.plot(diff_df)

plt.title('Electricity Usage after Differencing', fontsize=25)
plt.xlabel('Week', fontsize=20)
plt.ylabel('Kwh Usage', fontsize=20)

plt.tight_layout()

# Confirm with the dickey-fuller test
aug_dickey_fuller_test(diff_df.dropna())

"""Here, (Test Statistics = -4.55 <  critical value (5%) of -2.88), p-value is < 0.05 so we reject the null hypothesis and accept the alternate hypothesis, hence considers the **time series is stationary** for order difference of 1 (d).

# Model 1 - ARIMA - AutoRegressive Integrated Moving Average
"""

# Drop the index and do the sampling/ Split with the index column
# month wise data
# train_data = df.loc['2011-07':'2013-07']
# test_data = df.loc['2013-07':]

# week wise data split
train_data = df.loc['0':'160']
test_data = df.loc['160':]

plt.figure(figsize=(35, 7))
plt.grid()

plt.plot(train_data, c='blue', label='Train kwh_usage')
plt.plot(test_data, c='orange', label='Test kwh_usage')
plt.legend(loc='upper left', prop={'size':20})

plt.title('Average Weekly Consumption of Electricity for Train, Test data', fontsize=25)
plt.xlabel('Week', fontsize=20)
plt.ylabel('Kwh Usage', fontsize=20)

plt.tight_layout()

# Finding p - AR model lags, and q - MA lags
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, ax = plt.subplots(2, figsize=(12, 6))
ax[0] = plot_acf(df.diff().dropna(), ax=ax[0], lags=40)
ax[1] = plot_pacf(df.diff().dropna(), ax=ax[1], lags=40)

# ax[2] = plot_acf(df.diff().dropna(), ax=ax[2])
# ax[3] = plot_pacf(df.diff().dropna(), ax=ax[3])

plt.tight_layout()

"""Based on above pacf and acf plots, it is confusing to get the p, q values so we'll figure it out using auto_arima function available in pmdarima module. The series was made stationary with help of 1st order differencing, so d = 1.  """

# Find the order of the ARIMA model
order_df = auto_arima(df, trace=True, suppress_warnings=True)
order_df.summary()

# With the optimised (p, d, q) based on the above pacf, differencing, and acf plots
# With the optimised (p, d, q) based on the above auto_arima results, we also know (d=1) which is identified while making the series stationary
model = ARIMA(train_data, order=(3, 1, 3)).fit()

# Prediction
# monthly
# pred = pd.DataFrame(model.predict(start=len(train_data)-1,end=(len(df)-1)), index=test_data.index)
# weekly
pred = model.predict(start=len(train_data)-1,end=(len(df)-1))

# Evaluation
# monthy evaluation
# print('Mean Absolute Error: %.2f' % mean_absolute_error(test_data, pred))
# print('Root Mean Squared Error: %.2f' % np.sqrt(mean_squared_error(test_data, pred)))
# weekly evaluation
print('Mean Absolute Error: %.2f' % mean_absolute_error(test_data['kwh_usage'].values, pred))
print('Root Mean Squared Error: %.2f' % np.sqrt(mean_squared_error(test_data['kwh_usage'], pred)))
# test_data.mean(), np.sqrt(test_data.var())

# Model Summary
model.summary()

pred = pd.Series(list(pred.values), index=list(test_data.index))

plt.figure(figsize=(35, 8))
plt.grid()

plt.plot(train_data, label = 'Train kwh_usage')
plt.plot(test_data, label = 'Test kwh_usage')
plt.plot(pred, label = 'Predicted kwh_usage')

plt.title('Weekly Electricity Usage Forecasting', fontsize=25)
plt.xlabel('Week', fontsize=20)
plt.ylabel('Average Energy Usage Consumption in Kwh', fontsize=20)
plt.legend(loc='upper left', prop={'size': 20})
plt.tight_layout()

"""# VAR Model 2 - Vector AutoRegressive"""

# week wise data
var_df = data_df[['week', 'total_due', 'kwh_usage']]
group_df = var_df.groupby(['week']).mean()
group_df.head()

fig, axes = plt.subplots(nrows=2, ncols=1, dpi=120, figsize=(20,6))
for i, ax in enumerate(axes.flatten()):
    # data = var_df['bill_date', var_df.columns[i]].groupby('bill_date').mean()
    data = group_df[group_df.columns[i]]
    ax.plot(data, color='blue', linewidth=1)
    
    # Decorations
    ax.set_title(group_df.columns[i])
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.spines["top"].set_alpha(0)
    ax.tick_params(labelsize=6)

plt.tight_layout();

print('kwh_usage augmented dickey-fuller test:')
aug_dickey_fuller_test(group_df['kwh_usage'])
print('\n')
print('total_due augmented dickey-fuller test:')
aug_dickey_fuller_test(group_df['total_due'])

# Perform one order differecing and see if it becomes stationary and confirm with the dickey-fuller test
print('kwh_usage adf test on diff data:')
aug_dickey_fuller_test(group_df['kwh_usage'].diff().dropna())
print('\n')
print('total_due adf test on diff data:')
aug_dickey_fuller_test(group_df['total_due'].diff().dropna())

"""One order differencing of kwh_usage, total_due made the series stationary"""

print('kwh_usage causes total_due?\n')
print('------------------')
granger_1 = grangercausalitytests(group_df[['kwh_usage', 'total_due']], 4)

print('\n total_due causes kwh_usage?\n')
print('------------------')
granger_2 = grangercausalitytests(group_df[['total_due', 'kwh_usage']], 4)

# month wise split
# train_data = pd.DataFrame(final_df.loc['2011-07-01':'2013-12-31'])
# test_data =  pd.DataFrame(final_df['2014-01-01':])

# week wise data split
train_data = group_df.loc['0':'160']
test_data = group_df.loc['160':]

print(test_data.shape, train_data.shape, train_data.head())

model = VAR(train_data)

order = model.select_order(maxlags=20)
print(order.summary())

"""Based on the above results, the minimum vaues of AIC, FPE are observed at lag-13, so the lag to be choosen is 13."""

var_model = VARMAX(train_data, order=(13, 0), enforce_stationarity= True)
fitted_model = var_model.fit(disp=False)
print(fitted_model.summary())

pred = fitted_model.get_prediction(start=len(train_data)-1,end=len(group_df)-1)
predictions = pred.predicted_mean

predictions.columns=['total_due', 'kwh_usage']
predictions.index = test_data.index

# test_vs_pred = pd.concat([test_data, predictions], axis=1)

plt.figure(figsize=(20, 6))
plt.plot(train_data['kwh_usage'], label = 'Train kwh_usage')
plt.plot(train_data['total_due'], label = 'Train total_due')
plt.plot(test_data['kwh_usage'], label = 'Test kwh_usage')
plt.plot(test_data['total_due'], label = 'Test total_due')
plt.plot(predictions['kwh_usage'], label = 'Predicted kwh_usage')
plt.plot(predictions['total_due'], label = 'Predicted total_due')

plt.legend(loc='upper left')
plt.title('Weekly Electricity Usage Forecasting', fontsize=20)
plt.xlabel('Week', fontsize=15)
plt.ylabel('Average Energy Usage Consumption in Kwh', fontsize=15)
plt.tight_layout()
# indx = test_data.index.strftime("%Y-%m-%d").tolist()
# plt.xticks(indx, rotation=90)

# Calculating the root mean squared error
rmse_kwh_usage = math.sqrt(mean_squared_error(predictions['kwh_usage'],test_data['kwh_usage']))
print('Mean value of kwh_usage is : {}. Root Mean Squared Error is :{}'.format(mean(test_data['kwh_usage']), rmse_kwh_usage))

rmse_total_due = math.sqrt(mean_squared_error(predictions['total_due'],test_data['total_due']))
print('Mean value of total_due is : {}. Root Mean Squared Error is :{}'.format(mean(test_data['total_due']), rmse_total_due))

"""# LSTM Model"""

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.seasonal import seasonal_decompose
from keras.preprocessing.sequence import TimeseriesGenerator

# plt.rcParams.update({'font.size': 12})
# lstm = pd.read_csv('Electricity_Usage_Data.csv', index_col='bill_date', parse_dates=True)

# address_enc = LabelEncoder()
# bill_type_enc = LabelEncoder()

# lstm['address_enc'] = address_enc.fit_transform(lstm['service_address'])
# lstm['bill_type_enc'] = bill_type_enc.fit_transform(lstm['bill_type'])

# daily - not performing great
# lstm_df = pd.DataFrame(lstm['kwh_usage'], index=lstm.index)
# lstm_df = lstm_df.resample('D').mean()
# lstm_df.head()

# # monthly
# lstm_df = pd.DataFrame(lstm['kwh_usage'], index=lstm.index)
# lstm_df = lstm_df.resample('MS').mean()
# len(lstm_df), lstm_df.head()

# indx = lstm_df.loc['2011-07-01':].index.strftime("%Y-%m-%d").tolist()

# added
lstm_df = data_df[['kwh_usage', 'week']]
lstm_df = lstm_df.groupby('week').mean()
lstm_df.shape, lstm_df.head()

plt.figure(figsize=(35, 7))

plt.grid()
plt.plot(lstm_df)

plt.title('Weekly Average Consumption of Electricity', fontsize=25)
plt.xlabel('Week', fontsize=20)
plt.ylabel('Average Energy Usage Consumption in Kwh', fontsize=20)
# plt.xticks(indx, rotation=90)

plt.tight_layout()

# lstm_df['kwh_usage'] = lstm_df['kwh_usage'].dropna()

res = seasonal_decompose(lstm_df['kwh_usage'].dropna(), period=1)
fig = res.plot()
fig.set_size_inches((15, 7))
# plt.xlabel(indx, rotation=90)
fig.tight_layout()
plt.show()

# monthly split
# train_data = lstm_df.dropna().loc['2011-07-01':'2013-12-01']
# test_data = lstm_df.dropna().loc['2014-01-01':]

# week wise data split
train_data = lstm_df.loc['0':'160']
test_data = lstm_df.loc['160':]

lstm_df.head(), lstm_df.tail()

scaler = MinMaxScaler()

scaler.fit(train_data)
scaled_train = scaler.transform(train_data)
scaled_test = scaler.transform(test_data)

# define generator
n_input = 15
n_features = 1
generator = TimeseriesGenerator(scaled_train, scaled_train, length=n_input, batch_size=1)
     
X,y = generator[0]
print(f'Given the Array: \n{X.flatten()}')
print(f'Predict this y: \n {y}')

# define model
model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

model.summary()

# fit model
model.fit(generator, epochs=50)

loss_per_epoch = model.history.history['loss']
plt.plot(range(len(loss_per_epoch)),loss_per_epoch)

plt.title('Plot of LSTM Training Loss vs Epoch')
plt.xlabel('Epoch')
plt.ylabel('Loss')

"""As we can see the loss is decreasing at each epoch."""

last_train_batch = scaled_train[-15:]
last_train_batch = last_train_batch.reshape((1, n_input, n_features))
model.predict(last_train_batch)

test_preds = []

first_eval_batch = scaled_train[-n_input:]
current_batch = first_eval_batch.reshape((1, n_input, n_features))

for i in range(len(test_data)):
    # get pred value for first batch
    current_pred = model.predict(current_batch)[0]
    # add preds into test_predictions[]
    test_preds.append(current_pred) 
    # use pred to update the batch and remove 1st value
    current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)

true_predictions = scaler.inverse_transform(test_preds)
test_data['predictions'] = true_predictions
test_data.head()

# test_data.plot(figsize=(14,5))
plt.figure(figsize=(20, 6))
plt.plot(train_data, label='Train kwh_usage')
plt.plot(test_data['kwh_usage'], label='Test kwh_usage')
plt.plot(test_data['predictions'], label='Predicted kwh_usage')

plt.legend(loc='upper left')
plt.title('Weekly Average Electricity Consumption Forecast')
plt.xlabel('Week')
plt.ylabel('Average Consumption Usage in Kwh')
plt.show()

"""We have taken previous 15 values to predict the future values becuase it would enough data for predictions. The model performed better for the past values = 15 that is close to three and half months as we considered data in week wise manner."""

from sklearn.metrics import mean_squared_error
from math import sqrt
rmse=sqrt(mean_squared_error(test_data['kwh_usage'],test_data['predictions']))
print(rmse)

"""# Visualizations"""

data_main = pd.read_csv('Electricity_Usage_Data.csv')

data_main[['bill_date']] = data_main[['bill_date']].apply(pd.to_datetime)

data_main.loc[:,'bill_date'] = data_main['bill_date'].apply(lambda x: pd.to_datetime(f'{x.year}-{x.month}-01'))

viz_df = data_main.set_index('bill_date')

viz_df.head()

"""### Visualization #1 - Hyndavi"""

import time
from pprint import pprint

data_main = pd.read_csv('Electricity_Usage_Data.csv')

data_main[['bill_date']] = data_main[['bill_date']].apply(pd.to_datetime)

data_main.loc[:,'bill_date'] = data_main['bill_date'].apply(
    lambda x: pd.to_datetime(f'{x.year}-{x.month}-01')
)

viz_df = data_main.set_index('bill_date')
viz_df.head()

address_enc = LabelEncoder()
bill_type_enc = LabelEncoder()

data_main['address_enc'] = address_enc.fit_transform(
    data_main['service_address']
)
data_main['bill_type_enc'] = bill_type_enc.fit_transform(
    data_main['bill_type']
)
data_main['year'] = data_main['bill_date'].apply(lambda x:x.year)
data_main['month'] = data_main['bill_date'].apply(lambda x:x.month)

sns.heatmap(data_main.corr())

"""There do not seem to be any features that have high correlation with kwh usage except total due. But this is to be expected since the amount of energy used is directly proportional to the cost.

It might be difficult to use the features as they are for ML modeling.
"""

def plotbox(df, column):
    plot_features = df.groupby(pd.Grouper(freq=str(60)+'T')).mean().copy()
    plot_features[column] = [eval('x.%s'%column) for x in plot_features.index] 
    plot_features.boxplot('kwh_usage', by=column, figsize=(12, 8), grid=False)
    plt.ylabel('kWh Usage')
    plt.xlabel(column)
    plt.show()

# Pie chart for 'Bill Type'
explode = (0, 0.4, 0.2)
plt.figure(figsize=(5, 4))
print('value_counts:\n', data_main['bill_type'].value_counts())
data_main['bill_type'].value_counts().plot(kind='pie', explode=explode) #, autopct='%1.10f%%')
plt.title('Bill Type Pie Chart')
plt.xlabel('Type of Bill')
plt.ylabel('Frequency')
plt.legend(loc='center left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()

# Bar chart for 'Business Area'
plt.figure(figsize=(8, 6))
ax = data_main['business_area'].value_counts().plot(kind='bar')
plt.title('business_area')
plt.xlabel('Area')
plt.ylabel('Frequency')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()

# Bar chart for 'Bill Type'
plt.figure(figsize=(8, 6))
data_main['bill_type'].value_counts().plot(kind='bar')
plt.title('Bill Type')
plt.xlabel('Type')
plt.ylabel('Frequency')
plt.show()

# Bar chart for 'Business Area'
plt.figure(figsize=(8, 6))
data_main['business_area'].value_counts().plot(kind='bar')
plt.title('business_area')
plt.xlabel('Area')
plt.ylabel('Frequency')
plt.show()

"""The business area 2000 is the most populous area based on the frequency plot.

And the most common type of Bill type is T.

References:

1. [sklearn](https://scikit-learn.org/stable/)
2. [pandas](https://pandas.pydata.org/docs/)
3. [scipy](https://docs.scipy.org/doc/scipy/)
4. [data](https://data.world/houston/houston-electricity-bills)
5. [TimeSeriesAnalsysis 1](https://analyticsindiamag.com/quick-way-to-find-p-d-and-q-values-for-arima/)
6. [TimeSeriesAnalsysis 2](https://towardsdatascience.com/the-complete-guide-to-time-series-analysis-and-forecasting-70d476bfe775)
7. [TimeSeriesAnalsysis 3](https://www.machinelearningplus.com/time-series/vector-autoregression-examples-python/)
"""