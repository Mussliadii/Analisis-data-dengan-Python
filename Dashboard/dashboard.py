import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Konfigurasi halaman
st.set_page_config(page_title="Air Quality Analysis Dashboard: Wanliu Station", layout="wide")

# Judul dashboard
st.title("Dashboard Data Analisis")

# Baca data
try:
    df = pd.read_csv("Dashboard/all_data.csv")
except FileNotFoundError:
    st.error("File 'all_data.csv' tidak ditemukan. Pastikan file ada di direktori yang benar.")
    st.stop()

# Tampilkan informasi kolom
st.write("Kolom yang tersedia:", df.columns.tolist())
st.write("Tipe data kolom:")
st.write(df.dtypes)

# Tampilkan dataframe
st.subheader("Data Mentah")
st.dataframe(df.head())

# Pilih kolom numerik
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

# Buat dua kolom
col1, col2 = st.columns(2)

with col1:
    st.subheader("Histogram")
    selected_column = st.selectbox("Pilih kolom untuk histogram:", numeric_columns)
    try:
        fig, ax = plt.subplots()
        ax.hist(df[selected_column], bins=20)
        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frekuensi")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Terjadi error saat membuat histogram: {str(e)}")

with col2:
    st.subheader("Scatter Plot")
    x_column = st.selectbox("Pilih kolom untuk sumbu X:", numeric_columns)
    y_column = st.selectbox("Pilih kolom untuk sumbu Y:", numeric_columns)
    try:
        fig, ax = plt.subplots()
        ax.scatter(df[x_column], df[y_column])
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Terjadi error saat membuat scatter plot: {str(e)}")

# Buat heatmap
st.subheader("Heatmap Korelasi")
try:
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df[numeric_columns].corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.error(f"Terjadi error saat membuat heatmap: {str(e)}")

# Widget
    # Widget interaktif
    st.subheader("Analisis Kolom")
    column = st.selectbox("Pilih kolom untuk dianalisis:", df.columns)
    st.write(df[column].describe())
