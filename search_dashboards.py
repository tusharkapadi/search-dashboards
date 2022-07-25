

import requests
import json
import sys


api_token = ""
end_point = "https://us2.app.sysdig.com"


sysdig_dashboards = ""

def export_dashboard():
    # Use a breakpoint in the code line below to debug your script.

    # usage:
    # Param 1 - Sysdig Monitor API Token
    # Param 2 - Metric name you want to search

    if len(sys.argv) != 3:
        print(('usage: %s <Sysdig Monitor API Token> <Metric you want to search in all dashboards>' % sys.argv[0]))
        sys.exit(1)

    global api_token
    api_token = sys.argv[1]

    global metric
    metric = sys.argv[2]

    global total_dashboards

    global found_dashboards_list
    global found_dashboard_dict
    found_dashboards_list = []
    found_dashboard_dict = {}


    all_dashboards = get_dashboards_names()
    all_dashboards = json.loads(all_dashboards)

    total_dashboards = len(all_dashboards['dashboards'])

    for dashboard in all_dashboards['dashboards']:
        dashboard_data = get_dashboard(dashboard['id'])
        dashboard_data = json.loads(dashboard_data)

        #print(dashboard["name"])
        if metric in json.dumps(dashboard_data):
            #print("metric found")

            print("X", end="", flush=True)
            # metric found... search for panel and query
            for panel in dashboard["panels"]:
                panel_str = json.dumps(panel)
                if metric in panel_str:
                    #print("Found in panel - " +  panel["name"])
                    #found_dashboard_dict = {"dashboard_name": dashboard["name"], "panel_name": panel["name"]}
                    panel_url = end_point + "/#/dashboards/" + str(dashboard["id"]) + "/" + str(panel["id"]) + "/edit?last=600"
                    found_dashboard_dict = {"dashboard_name": dashboard["name"], "panel_id": panel["id"], "panel_name": panel["name"], "panel_url": panel_url}
                    found_dashboards_list.append(found_dashboard_dict.copy())
                    found_dashboard_dict.clear()

        else:
            print(".", end="", flush=True)


    print("")
    #file_name = download_folder + "/search_results.csv"

    #write_csv(file_name)
    print_summary_output()

def print_summary_output():

    print("="*100)
    print("SUMMARY")
    print("="*100)
    print("Script attempted to search - " + metric + " - in " + str(total_dashboards) + " dashboards and found in following " +
          str(len(found_dashboards_list)) + " dashboards/panels:")

    for dashboard in found_dashboards_list:
        print("-" * 100)
        print("dashboard: " + dashboard["dashboard_name"])
        print("panel id: " + str(dashboard["panel_id"]))
        print("panel name: " + dashboard["panel_name"])
        print("panel url: " + dashboard["panel_url"])



# def write_csv(file_name):
#     fieldnames = ['dashboard_name', 'panel_name']
#
#     with open(file_name, 'w', encoding='UTF8', newline='') as outfile:
#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#
#         writer.writerow("Metric - " + "testtttt")
#
#         writer.writeheader()
#         writer.writerows(found_dashboards_list)


def get_dashboards_names():

    url = end_point + "/api/v3/dashboards/"

    payload = {}

    auth = "Bearer " + api_token
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.ok is False:
        print("Status: received an error while getting a dashboard - " + json.dumps(response.text))

    return response.text


def get_dashboard(dashboard_id):

    url = end_point + "/api/v3/dashboards/" + str(dashboard_id)

    payload = {}

    auth = "Bearer " + api_token
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.ok is False:
        print("Status: received an error while getting a dashboard - " + json.dumps(response.text))

    return response.text


if __name__ == '__main__':
    export_dashboard()
