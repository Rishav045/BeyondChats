import requests
import json
import pprint

# Function to fetch data from the API
def fetch_data_from_api():
    base_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    page = 1
    data = []
    
    while True:
        print(page)
        
        # Construct the URL for the current page
        url = f"{base_url}?page={page}"
        
        # Send a GET request to the API
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            json_data = response.json()
            
            # Print the data for the current page
            pprint.pprint(json_data["data"])
            
            # Append the data to the list
            data.append(json_data["data"]["data"])
            
            print(data)
            
            # Check if there is a next page
            if json_data["data"]["next_page_url"] is None:
                break
            else:
                page += 1
        else:
            # Print an error message if the request was not successful
            print(f"Error fetching data from API. Status code: {response.status_code}")
            break
    
    return data

# Function to save data to a JSON file
def save_to_json_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Fetch data from the API
data = fetch_data_from_api()

# Save the fetched data to a JSON file
save_to_json_file(data, "extracted.json")
