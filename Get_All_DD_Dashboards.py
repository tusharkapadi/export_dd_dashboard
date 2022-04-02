import sys

import requests
import json


def get_all_dashboards():

    if len(sys.argv) != 4:
        print(('usage: %s <Datadog api key> <Datadog app key> <directory to save Datadog dashboards>' % sys.argv[0]))
        sys.exit(1)

    api_key = sys.argv[1]
    app_key = sys.argv[2]
    folder = sys.argv[3]

    payload = {}
    headers = {
        'DD-API-KEY': api_key,
        'DD-APPLICATION-KEY': app_key,
        'Content-Type': 'application/json'
    }

    # Get all dashboards
    url = "https://api.datadoghq.com/api/v1/dashboard"

    response = requests.request("GET", url, headers=headers, data=payload)

    dashboards_list = json.loads(response.text)
    i = 1
    success = 0
    fail = 0
    for dashboard in dashboards_list["dashboards"]:
        url = "https://api.datadoghq.com/api/v1/dashboard/" + dashboard["id"]
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.ok:
            dash = json.loads(response.text)
            with open(folder + dash["title"] + ".json", 'w') as outfile:
                json.dump(dash, outfile)
            print(str(i) + " - " + dash["title"] + " - COMPLETED")
            success += 1
        else:
            print(str(i) + " - " + dash["title"] + " - FAILED")
            fail += 1

        i += 1

    print("")
    print("Downloaded " + str(success) + " dashboards out of " + str(i-1))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_all_dashboards()
