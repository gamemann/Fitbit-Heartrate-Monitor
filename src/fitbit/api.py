import requests

def retrieve_heartrates(cfg):
    # Send HTTP request and retrieve response.
    api_url = "https://api.fitbit.com/1/user/" + cfg["UserID"] + "/activities/heart/date/today/1d.json"

    resp = requests.get(api_url, headers={"Authorization": "Bearer " + cfg["Authorization"]})

    # Dummy data for now until we figure out what API endpoint to use and how to parse data.
    return [70, 72, 74, 70, 65, 60]

