import pandas as pd
import requests
import time


df = pd.read_csv(filepath)

location_column = 'Address'

df['latitude'] = ''
df['longitude'] = ''

api_key = 'pk.232dfcf17342ac98b1912e93e8fc7df2'

for index, row in df.iterrows():
    location = row[location_column]
    
    url = f'https://us1.locationiq.com/v1/search.php?key={api_key}&q={location}&format=json'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            
            df.at[index, 'latitude'] = latitude
            df.at[index, 'longitude'] = longitude
        
        else:
            print(f"Error fetching data for {location}: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    time.sleep(1)  

df.to_csv('restaurants_with_modified.csv', index=False)
print("after_adding_longitude_and_latitude")
