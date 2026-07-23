#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Temperature and Relative Humidity Graphic of the last 10 Days

# Gwendolyn Dmitruk; 2025
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This program will be triggered by s_cat.py after t_rh.py
# Creates a line graph depicting relative humidity in blue
# and Celcius temperature readings in red
# a copy of this program should be in every folder
# where iridium data is processed
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#Import the libraries

import pandas as pd
import matplotlib.pyplot as plt


# Load your data

filename = "Base Camp.csv"  # example: "Camp 2.csv"
df = pd.read_csv(filename)


# Parse timestamp and clean

df.rename(columns={'Time (NPT)': 'timestamp'}, inplace=True)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df[df['Missing'] == False]
df = df.sort_values('timestamp')

# Convert to timezone-aware datetime (assuming original is UTC)

df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kathmandu')


# Filter to 10 days in Nepal time

latest_time = df['timestamp'].max()
start_time = latest_time - pd.Timedelta(days=10)
df = df[df['timestamp'] >= start_time]

df = df.rename(columns={
    'Temperature (Celsius)': 'Temperature (°C)',
    'Relative Humidity': 'Relative Humidity (%)'
})


# Plot

fig, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(df['timestamp'], df['Temperature (°C)'], color='red', marker='o', label='Temperature (°C)')
ax1.set_xlabel('Nepal Local Time')
ax1.set_ylabel('Temperature (°C)', color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.grid(True, linestyle='--', alpha=0.4)


# RH on secondary axis

ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['Relative Humidity (%)'], color='blue', marker='s', label='RH (%)')
ax2.set_ylabel('Relative Humidity (%)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')


# Improve formatting

fig.autofmt_xdate()
plt.title(f"Last 10 Days (NPT): Temperature and RH at {filename.replace('.csv', '')}")
fig.tight_layout()


# Save as PNG

plt.savefig("trh_bc.png", dpi=300)
plt.savefig("/mnt/MetData/trh_bc.png", dpi=300)
# plt.show()