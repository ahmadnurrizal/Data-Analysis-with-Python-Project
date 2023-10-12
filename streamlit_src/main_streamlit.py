import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from datetime import datetime

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_sum_order_items_df(df):
  order_items_df = df["product_category_name_english"].value_counts().reset_index()
  order_items_df.columns = ["product_category_name_english", "products"]
  order_items_df = order_items_df.sort_values(by="products", ascending=False)
  return order_items_df

def create_order_monthly_df(df):
  monthly_df = df.resample(rule='M').agg({
      "order_id": "nunique"
  })
  
  monthly_df.index = monthly_df.index.strftime('%B') #mengubah format order_approved_at menjadi Tahun-Bulan
  monthly_df = monthly_df.reset_index()
  monthly_df.rename(columns={
      "order_id": "order_count",
  }, inplace=True)

  monthly_df = monthly_df.sort_values('order_count').drop_duplicates('order_approved_at', keep='last')
  monthly_df.sort_values(by='order_count')
  month_mapping = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
  }

  monthly_df["month_numeric"] = monthly_df["order_approved_at"].map(month_mapping)
  monthly_df = monthly_df.sort_values("month_numeric")
  monthly_df = monthly_df.drop("month_numeric", axis=1)
    
  return monthly_df

def create_monthly_spend_df(df):
  monthly_spend_df = df.resample(rule='M').agg({
    "payment_value": "sum"
  })
  
  monthly_spend_df.index = monthly_spend_df.index.strftime('%B') #mengubah format order_approved_at menjadi Tahun-Bulan
  monthly_spend_df = monthly_spend_df.reset_index()
  monthly_spend_df.rename(columns={
      "payment_value":"total_spend"
  }, inplace=True)
  
  monthly_spend_df = monthly_spend_df.sort_values('total_spend').drop_duplicates('order_approved_at', keep='last')
  monthly_spend_df.sort_values(by='total_spend')
  
  month_mapping = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
  }
  monthly_spend_df["month_numeric"] = monthly_spend_df["order_approved_at"].map(month_mapping)
  monthly_spend_df = monthly_spend_df.sort_values("month_numeric")
  monthly_spend_df = monthly_spend_df.drop("month_numeric", axis=1)
  
  return monthly_spend_df
  
  
# Load cleaned data
all_data_df = pd.read_csv("../all_data.csv")

datetime_columns = ["order_approved_at"]
all_data_df.sort_values(by="order_approved_at", inplace=True)
all_data_df.reset_index(inplace=True, drop=True)  # Drop the old index

for column in datetime_columns:
    all_data_df[column] = pd.to_datetime(all_data_df[column])


all_data_df.set_index("order_approved_at", inplace=True)  # Set the column as the index

min_date = all_data_df.index.min()
max_date = all_data_df.index.max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    

main_df = all_data_df[(all_data_df.index >= min_date) & (all_data_df.index <= max_date)]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
sum_order_items_df = create_sum_order_items_df(main_df)
order_monthly_df = create_order_monthly_df(main_df)
monthly_spend_df = create_monthly_spend_df(main_df)

st.header('Final Project Analisis Data :sparkles:')
# Product performance
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Number of Orders per Month (2018)
st.subheader("Number of Orders per Month (2018)")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
  order_monthly_df["order_approved_at"],
  order_monthly_df["order_count"],
  marker='o', 
  linewidth=2,
  color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Total customer spend money per Month (2018)
st.subheader("Total customer spend money per Month (2018)")
# st.dataframe(monthly_spend_df)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
  monthly_spend_df["order_approved_at"],
  monthly_spend_df["total_spend"],
  marker='o', 
  linewidth=2,
  color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)
st.caption('Copyright © Ahmad Nur Rizal 2023')