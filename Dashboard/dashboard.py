import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Air Quality Analysis Dashboard: Wanliu Station", layout="wide")

# Judul dashboard
st.title("Dashboard Data Analisis")

# Baca data
@st.cache_data
def load_data():
    data = pd.read_csv("Dashboard/all_data.csv")
    return data

df = load_data()

# Tampilkan dataframe
st.subheader("Data Mentah")
st.dataframe(df.head())

# Buat dua kolom
col1, col2 = st.columns(2)

with col1:
    st.subheader("Histogram")
    fig, ax = plt.subplots()
    ax.hist(df['kolom_numerik'], bins=20)
    st.pyplot(fig)

with col2:
    st.subheader("Scatter Plot")
    fig, ax = plt.subplots()
    ax.scatter(df['kolom_x'], df['kolom_y'])
    st.pyplot(fig)

# Buat heatmap
st.subheader("Heatmap Korelasi")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Widget interaktif
st.subheader("Analisis Kolom")
column = st.selectbox("Pilih kolom untuk dianalisis:", df.columns)
st.write(df[column].describe())
