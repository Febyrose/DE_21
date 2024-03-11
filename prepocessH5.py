import os
import glob
import pandas as pd
import utils



def get_all_data(basedir, ext='.h5'):
    # Define a list to store data
    data = []

    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*' + ext))
        for f in files:
            h5 = utils.open_h5_file_read(f)
            
            # Extract desired fields
            song_id = utils.get_song_id(h5)  # Assuming you have a similar function to get song ID
            title = utils.get_title(h5)
            artist_name = utils.get_artist_name(h5)  # Assuming you have this function
            artist_mbid = utils.get_artist_mbid(h5)
            # Add more fields as needed...
            
            # Append a dictionary of the extracted data to the list
            data.append({
                'SongID': song_id,
                'Title': title,
                'ArtistName': artist_name,
                'Artist_mbid': artist_mbid,
                # Include more fields here...
            })
            
            h5.close()

    # Convert the list of data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Optionally, you can sort or perform any other DataFrame operations here
    
    # Write the DataFrame to a CSV file
    df.to_csv('your_output.csv', index=False)

# Usage
basedir = "dataset"  # Update this to your dataset directory
get_all_data(basedir) 
