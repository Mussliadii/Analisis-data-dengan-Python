#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# Load dataset
all_df_shunyi = pd.read_csv("Dashboard/all_data.csv")

# Title of the dashboard
st.title('Air Quality Analysis Dashboard: Wanliu Station')

# Dashboard header
st.write("**This dashboard contains air quality and variables that affect air quality at Wanliu Station.**")

# Histogram
st.subheader('Data distribution')
fig, axes = plt.subplots(nrows=1, ncols=len(all_df_shunyi.columns), figsize=(15, 4))

# Jika ada satu kolom, axes bukan array
if len(all_df_shunyi.columns) == 1:
    axes = [axes]  # Ubah menjadi list agar dapat diakses seperti array

for i, column in enumerate(all_df_shunyi.columns):
    axes[i].hist(all_df_shunyi[column])
    axes[i].set_title(column)

plt.tight_layout()  # Add this to adjust the layout
st.pyplot(fig)

# Correlation heatmap of some variables
st.subheader('Correlation Heatmap of Air Quality Indicators')
corr = all_df_shunyi[['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(15,10))
sns.heatmap(corr, annot=True, ax=ax)
plt.title('Correlation Heatmap')
st.pyplot(fig)

# PM2.5 Trendline from month to month
st.subheader('Trendline of PM2.5 from Month to Month')
all_df_shunyi['year_month'] = all_df_shunyi['year'].astype(str) + '-' + all_df_shunyi['month'].astype(str).str.zfill(2)
pm25_monthly = all_df_shunyi.groupby('year_month')['PM2.5'].mean().reset_index()

sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(data=pm25_monthly, x='year_month', y='PM2.5', marker='o', color='b', ax=ax)
plt.xlabel('Year-Month')
plt.ylabel('Average PM2.5')
plt.xticks(rotation=90)
plt.tight_layout()
st.pyplot(fig)

# Relationship between NO2 and CO
st.subheader('Relationship between NO2 and CO')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='NO2', y='CO', data=all_df_shunyi, ax=ax)
plt.xlabel('NO2')
plt.ylabel('CO')
plt.title('Relationship between NO2 and CO')
st.pyplot(fig)

# Comparison of PM2.5 and PM10 from Year to Year
st.subheader('Comparison of PM2.5 and PM10 from Year to Year')
pm_yearly = all_df_shunyi.groupby('year')[['PM2.5', 'PM10']].mean()

# Plotting with matplotlib instead of DataFrame plot
fig, ax = plt.subplots(figsize=(10, 6))
pm_yearly.plot(marker='o', ax=ax)
plt.xlabel('Year')
plt.ylabel('Average Concentration')
plt.xticks(pm_yearly.index)
plt.grid(True)
plt.legend(title='Pollutant', loc='upper left')
plt.title('Comparison of PM2.5 and PM10 from Year to Year')
plt.tight_layout()
st.pyplot(fig)
