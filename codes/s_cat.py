#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# s cat
# Gwendolyn Dmitruk; 2025
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# concatonates the .sbd files into a singular .csv
# Replaces the old .csv with new incoming data
# A copy of this program should sit in every folder 
# you want iridium data to be processed
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# import the libraries

import pandas as pd
import glob
import os


# Change working directory to Unit_7660

os.chdir(os.path.dirname(os.path.abspath(__file__)))

sbd_folder = '.'
sbd_files = sorted(glob.glob(os.path.join(sbd_folder, '*.sbd')))
output_file = 'Base Camp.csv'


# Delete the old output file

if os.path.exists(output_file):
    os.remove(output_file)
    print(f"🗑️ Removed old .csv")


# Confirm the existance of .sbd files

print(f"🔍 Found {len(sbd_files)} .sbd files")

all_data = []

for file in sbd_files:
    try:
        df = pd.read_csv(file, sep=',', header=None, quotechar='"')
        df.columns = ['Time (NPT)', 'Temperature (Celsius)', 'Relative Humidity', 'col3', 'col4', 'col5']
        df['Time (NPT)'] = pd.to_datetime(df['Time (NPT)'], format='%Y-%m-%d %H:%M:%S')

        # Weather code mapping
        weather_map = {
            0: 'NP',
            51: 'UP', 52: 'UP', 53: 'UP', 54: 'UP', 55: 'UP', 56: 'UP', 57: 'UP', 58: 'UP', 59: 'UP',
            61: 'RN-', 62: 'RN', 63: 'RN+',
            67: 'RNSN-', 68: 'RNSN', 69: 'RNSN+',
            71: 'SN-', 72: 'SN', 73: 'SN+',
            77: 'UP', 78: 'UP', 79: 'UP',
            87: 'GP', 88: 'GP+'
        }

        # Map col3 to Weather code
        df['Weather'] = df['col3'].map(weather_map)

        # Add an empty Precipitation column
        df['Precipitation'] = ''

        all_data.append(df)
    except Exception as e:
        print(f"❌ Failed to read {file}: {e}")


if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('Time (NPT)')


    # Remove duplicates before resampling

    combined_df = combined_df.drop_duplicates(subset='Time (NPT)')
    combined_df.set_index('Time (NPT)', inplace=True)


    # Fill missing timestamps at a 1-hour interval

    full_df = combined_df.resample('1h').asfreq()  

    # Compute hourly precipitation difference
    full_df['Precipitation'] = full_df['col4'].diff()

    # Replace negative values and NaN with 0
    full_df['Precipitation'] = full_df['Precipitation'].clip(lower=0).fillna(0).round(1)


    # Flag missing timestamps

    full_df['Missing'] = full_df.isnull().any(axis=1)


    # Reset index to make 'timestamp' a column again

    full_df.reset_index(inplace=True)


    # Save

    full_df.to_csv(output_file, index=False)
    print(f"✅ Combined .csv with hourly timestamps written to {output_file}")
else:
    print("❌ No valid .sbd files were read.")

# Trigger upload.py t_rh.py, and t_rh_10.py
import subprocess

subprocess.run(['python3', 't_rh.py'], check=True)
subprocess.run(['python3', 't_rh_10.py'], check=True)
subprocess.run(['python3', 'upload.py'], check=True)
#subprocess.run(['python3', 'WebAccessGateway.py'], check=True)
print(" Finished subprocesses successfully")