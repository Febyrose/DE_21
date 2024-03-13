import pandas as pd
import requests
import time
import pickle


def save_cache(cache, filename='country_cache.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(cache, f)

def load_cache(filename='country_cache.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}  # Return an empty cache if the file doesn't exist


def get_artist_country_by_mbid(mbid):
    # Construct the URL with the artist's MBID
    if mbid in country_cache:
        return country_cache[mbid]
    
    url = f"https://musicbrainz.org/ws/2/artist/{mbid}?fmt=json"

    # Pause for 1 second to respect the MusicBrainz API rate limit
    time.sleep(1) 
    
    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the country from the response
        country = data.get('country', 'Country information not available')
        country_cache[mbid] = country  # Cache the result
        return country
    else:
        return 'Failed to retrieve information'


def main():
    # Load dataset
    country_cache = load_cache()
    df = pd.read_csv('your_updated_dataset_test_4.csv')
    
    # Add a new column for the country, initialized to 'Unknown'
    df['Country'] = 'Unknown'
    
    for index in range(0, 10000):
        row = df.iloc[index]  # Get the row by integer location
        mbid = row['Artist_mbid']
        country = get_artist_country_by_mbid(mbid)
        df.at[index, 'Country'] = country
    
    save_cache(country_cache)
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv('processedDataWithCountry.csv', index=False)
