import requests
import json
import pprint
def fetch_data_from_api():
    base_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    page = 1
    data = []

    while True:
        print(page)
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()
            pprint.pprint(json_data["data"])
            data.append(json_data["data"]["data"])
            print(data)
            if json_data["data"]["next_page_url"] is None:
                break
            else:
                page += 1
        else:
            print(f"Error fetching data from API. Status code: {response.status_code}")
            break

    return data

def save_to_json_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
data=fetch_data_from_api()

save_to_json_file(data,"extracted.json")





