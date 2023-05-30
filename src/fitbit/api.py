import requests

import utils

def retrieve_heartrates(cfg) -> list | None:
    ret = []

    # Dummy data for now.
    # return [70, 72, 74, 70, 65, 60]

    # Send HTTP request and retrieve response.
    api_url = "https://api.fitbit.com/1/user/" + cfg["UserID"] + "/activities/heart/date/today/1d/1sec.json"

    resp = requests.get(api_url, headers={"Authorization": "Bearer " + cfg["Authorization"]})

    # check status code.
    if resp.status_code != 200:
        print("Error retrieving heart rates! Status code => " + str(resp.status_code))

        return None
    
    # Debug message.
    utils.debug_message(cfg, 3, "Heart rates JSON => " + resp.json())

    # Parse data.
    data = resp.json()["activities-heart"][0]["activities-heart-intraday"]["dataset"]

    if data is None:
        print("Heart rates data is none.")

        return None
    
    # Retrieve last x amount of items on list where x is the average count config setting.
    items = data[-(int(cfg["AvgCount"])):]

    # Loop through each item in the list and append to our return.
    for ele in items.items():
        ret.append(int(ele["value"]))

    return ret

