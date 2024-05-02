from os import write
import requests
import pandas as pd
import io
#from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
#from IPython.display import HTML
# Load the whole JSON file
import json
import folium


API_KEY= "u-lC2ltXMMNhd2MvNxIG3r2PxNLEFWuSusALGUeJCz39gFQFzRmS_yAq4ci3W6rcUUDZiURa8gYrZUvNK7hs-MkIOPZC59HDLetudP4gBVw1tWwYe1HTc-I4LrgpZnYx"


url = "https://api.yelp.com/v3/businesses/search?term='black business'&location='Baltimore, MD'&sort_by=best_match"


headers = {"accept": "application/json", "Authorization": "Bearer %s" % API_KEY }
response = requests.get(url, headers=headers)
Ydata = json.load(io.StringIO(response.text))
df = pd.DataFrame.from_records(   Ydata['businesses']   )

#BWDCdata=pd.read_csv(explore_data_bow_06.csv)
df2 = pd.read_csv('explore_data_bow_06.csv')
drop_columns = [ 'geo_level','geo_name','state_name']
df2 = df2.drop(drop_columns, axis=1)
df2 = df2.sort_values(by=['year'], ascending=False)
json2 = df2.to_json()
#print(json2)

#inspected data and decided to drop columns that I don't need
#df = df.drop(df.columns[[0, 1, 3]], axis=1)
#df = df[df['is_closed']=='false']
drop_columns = [ 'url', 'transactions','price','phone','display_phone','distance','attributes', 'alias', 'image_url']
df = df.drop(drop_columns, axis=1)

#categorization
# Explode the 'categories' list into separate rows for each category
df_exploded = df.explode('categories')
# Extract category titles
df_exploded['category_title'] = df_exploded['categories'].map(lambda x: x['title'])
# Count occurrences of each category
category_counts = df_exploded['category_title'].value_counts()
# Print the counts
#print(category_counts)



# Extract latitude and longitude from the coordinates dictionary
df['latitude'] = df['coordinates'].apply(lambda x: x['latitude'])
df['longitude'] = df['coordinates'].apply(lambda x: x['longitude'])

# Function to format category titles for display
def format_categories(categories):
    return ', '.join([cat['title'] for cat in categories])

# Adding formatted categories to DataFrame
df['formatted_categories'] = df['categories'].apply(format_categories)


# Create a map centered around an average location
map_center_latitude = df['latitude'].mean()
map_center_longitude = df['longitude'].mean()
map = folium.Map(location=[map_center_latitude, map_center_longitude], zoom_start=12)

# Add points to the map
for idx, row in df.iterrows():
    # Popup content including the number of reviews
    popup_content = f"<b>{row['name']}</b><br>{row['formatted_categories']}<br>Reviews: {row['review_count']}"
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=popup_content,
        tooltip=row['name']
    ).add_to(map)

# Display the map
map.save('index.html')  # Saves the map to an HTML file

json = df.to_json()
df.to_csv('business_data.csv', index=False)
#print(csv)




