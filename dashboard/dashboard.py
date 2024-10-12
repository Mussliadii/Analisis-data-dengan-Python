import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import urllib

sns.set(style='dark')

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", 
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("https://raw.githubusercontent.com/mhdhfzz/data-analyst-dicoding/main/dashboard/df.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('https://raw.githubusercontent.com/mhdhfzz/data-analyst-dicoding/main/dashboard/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("https://raw.githubusercontent.com/mhdhfzz/data-analyst-dicoding/main/dashboard/logo.png", width=100)
    with col3:
        st.write(' ')

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
    total_order = main_df["order_id"].nunique()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = main_df["payment_value"].sum()
    st.markdown(f"Total Revenue: **{total_revenue:.2f}**")

fig, ax = plt.subplots(figsize=(12, 6))
daily_orders = main_df.groupby(main_df["order_approved_at"].dt.date)["order_id"].count()
sns.lineplot(
    x=daily_orders.index,
    y=daily_orders.values,
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Customer Spend Money
st.subheader("Customer Spend Money")
col1, col2 = st.columns(2)

with col1:
    total_spend = main_df["payment_value"].sum()
    st.markdown(f"Total Spend: **{total_spend:.2f}**")

with col2:
    avg_spend = main_df["payment_value"].mean()
    st.markdown(f"Average Spend: **{avg_spend:.2f}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=main_df.groupby(main_df["order_approved_at"].dt.date)["payment_value"].sum().reset_index(),
    x="order_approved_at",
    y="payment_value",
    marker="o",
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = main_df["order_item_id"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = main_df["order_item_id"].mean()
    st.markdown(f"Average Items: **{avg_items:.2f}**")

# Review Score (Assuming 'review_score' exists in the data)
st.subheader("Review Score")
col1, col2 = st.columns(2)

if "review_score" in main_df.columns:
    avg_review_score = main_df["review_score"].mean()
    most_common_review_score = main_df["review_score"].value_counts().idxmax()

    with col1:
        st.markdown(f"Average Review Score: **{avg_review_score:.2f
