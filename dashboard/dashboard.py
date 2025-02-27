import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
days_df = pd.read_csv("dashboard/df_day_clean.csv")
hours_df = pd.read_csv("dashboard/df_hour_clean.csv")

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()


st.markdown("<h1 style='text-align:center;text-decoration:underline'>Bike Sharing Dashboard<h1>", unsafe_allow_html=True)

with st.expander("Filter"):
    start_date, end_date = st.date_input(
                label="Tanggal",
                min_value=min_date_days,
                max_value=max_date_days,
                value=[min_date_days, max_date_days])
    
    season = st.selectbox( label="Musim",
                          options=('All', 'Springer', 'Summer', 'Fall', 'Winter'))
    
    temperature = st.selectbox(label="Suhu",
                               options=('All', 'Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi'))
    
    weather = st.selectbox(label="Cuaca",
                                options=('All',
                                         'Clear, Few clouds, Partly cloudy, Partly cloudy',
                                         'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
                                         'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
                                         'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'))
    workingday = st.selectbox(label="Hari Kerja",
                                options=('All','Ya', "Tidak"))
    
    hue = st.selectbox(label="Hue",
                        options=('All', 'season', 'temperature_cat', 'weathersit', 'workingday'))



filtered_days_df = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]
filtered_days_df['dteday'] =  pd.to_datetime(filtered_days_df["dteday"])

if season != 'All':
    filtered_days_df = filtered_days_df[filtered_days_df['season']==season]
if temperature != 'All':
    filtered_days_df = filtered_days_df[filtered_days_df['temperature_cat']==temperature]
if weather != 'All':
    filtered_days_df = filtered_days_df[filtered_days_df['weathersit']==weather]
if workingday != 'All':
    if workingday == 'Ya':
        filtered_days_df = filtered_days_df[filtered_days_df['workingday']=='Yes']
    else:
        filtered_days_df = filtered_days_df[filtered_days_df['workingday']=='No']
if hue == 'All':
    hue = None

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = filtered_days_df.cnt.sum()
    st.metric("Jumlah Penyewa (Semua)", value=total_orders)

with col2:
    total_sum = filtered_days_df.registered.sum()
    st.metric("Jumlah Penyewa (Registered)", value=total_sum)

with col3:
    total_sum = filtered_days_df.casual.sum()
    st.metric("Jumlah Penyewa (Casual)", value=total_sum)

fig, ax = plt.subplots(figsize=(16, 8))
sns.scatterplot(
    filtered_days_df,
    x='dteday',
    y='cnt',
    hue=hue
)
ax.set_title('Jumlah Penyewa / Hari', fontsize=30)
ax.set_xlabel('Tanggal', fontsize=20)
ax.set_ylabel('Jumlah Penyewa', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

filtered_hours_df = hours_df[(hours_df["dteday"] >= str(start_date)) & (hours_df["dteday"] <= str(end_date))]
filtered_hours_df['dteday'] =  pd.to_datetime(filtered_hours_df["dteday"])

if season != 'All':
    filtered_hours_df = filtered_hours_df[filtered_hours_df['season']==season]
if temperature != 'All':
    filtered_hours_df = filtered_hours_df[filtered_hours_df['temperature_cat']==temperature]
if weather != 'All':
    filtered_hours_df = filtered_hours_df[filtered_hours_df['weathersit']==weather]
if workingday != 'All':
    if workingday == 'Ya':
        filtered_hours_df = filtered_hours_df[filtered_hours_df['workingday']=='Yes']
    else:
        filtered_hours_df = filtered_hours_df[filtered_hours_df['workingday']=='No']

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    filtered_hours_df.groupby('hr').cnt.mean().reset_index(),
    x='hr',
    y='cnt'
)
ax.set_title('Rata - Rata Penyewa / Hari / Jam', fontsize=20)
ax.set_xlabel('Jam', fontsize=20)
ax.set_ylabel('Rata - Rata Penyewa', fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)