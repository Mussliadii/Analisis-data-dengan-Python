import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Air Quality Analysis Dashboard: Wanliu Station", layout="wide")

# Judul dashboard
st.title("Dashboard Data Analisis Air Quality: Wanliu Station")

# Baca data
try:
    airdata_df = pd.read_csv("Dashboard/all_data.csv")
except FileNotFoundError:
    st.error("File 'all_data.csv' tidak ditemukan. Pastikan file ada di direktori yang benar.")
    st.stop()

# Tampilkan informasi kolom
st.write("Tipe data kolom:")
st.write(airdata_df.dtypes)

# Tampilkan data mentah
st.subheader("Data Mentah")
st.dataframe(airdata_df.head())

# Merge year dan month menjadi year_month
airdata_df['year_month'] = airdata_df['year'].astype(str) + '-' + airdata_df['month'].astype(str).str.zfill(2)

# Menghitung rata-rata bulanan PM2.5
pm25_monthly = airdata_df.groupby('year_month')['PM2.5'].mean().reset_index()

# Membuat plot trendline PM2.5 dari bulan ke bulan
st.subheader("Trendline PM2.5 dari Bulan ke Bulan")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=pm25_monthly, x='year_month', y='PM2.5', marker='o', color='Black', ax=ax)
ax.set_xlabel('Year-Month')
ax.set_ylabel('Average PM2.5')
ax.set_title('Trendline of PM2.5 from Month to Month')
plt.xticks(rotation=90)
st.pyplot(fig)

# Scatter plot antara NO2 dan CO
st.subheader("Scatter Plot antara NO2 dan CO")
fig, ax = plt.subplots()
sns.scatterplot(x='NO2', y='CO', data=airdata_df, ax=ax)
ax.set_xlabel('NO2')
ax.set_ylabel('CO')
ax.set_title('Relationship between NO2 and CO')
st.pyplot(fig)

# Korelasi antara NO2 dan CO
correlation = airdata_df['NO2'].corr(airdata_df['CO'])
st.write(f"Nilai korelasi antara NO2 dan CO: {correlation:.2f}")
if correlation > 0.5:
    st.write("Ada korelasi positif yang kuat antara NO2 dan CO.")
elif correlation < -0.5:
    st.write("Ada korelasi negatif yang kuat antara NO2 dan CO.")
else:
    st.write("Tidak ada korelasi yang kuat antara NO2 dan CO.")

# Menghitung rata-rata tahunan PM2.5 dan PM10
pm_yearly = airdata_df.groupby('year')[['PM2.5', 'PM10']].mean()

# Perbandingan PM2.5 dan PM10 dari tahun ke tahun
st.subheader("Perbandingan PM2.5 dan PM10 dari Tahun ke Tahun")
fig, ax = plt.subplots()
pm_yearly.plot(marker='o', ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Average Concentration')
ax.set_title('Comparison of PM2.5 and PM10 from Year to Year')
ax.grid(True)
st.pyplot(fig)

# Heatmap korelasi
st.subheader("Heatmap Korelasi")
fig, ax = plt.subplots(figsize=(15, 8))
sns.heatmap(airdata_df[['PM2.5', 'PM10', 'NO2', 'CO']].corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)
