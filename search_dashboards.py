import csv
import requests
import json
import sys
from datetime import date


def search_dashboard():
    # parse arguments
    end_point, api_token, metric, output = parse_ags()

    # query all the dashbaords from Sysdig
    all_dashboards = json.loads(get_dashboards(end_point, api_token))

    total_dashboards = len(all_dashboards['dashboards'])

    # search metric str in all the dashboards and prepared a dashboard/panel found list
    found_dashboards_list = search_metrics(all_dashboards, end_point, metric)

    if output == "csv":
        # create a CSV file
        write_csv(found_dashboards_list, metric)
    elif output == "json":
        # create a Json file
        write_json(found_dashboards_list, metric)

    # print summary
    print_summary_output(found_dashboards_list, metric, total_dashboards)


def parse_ags():
    # usage:
    # Param 1 - Sysdig Monitor EndPoint URL
    # Param 2 - Sysdig Monitor API Token
    # Param 3 - Metric name you want to search
    # Param 4 - output - either json or csv - Optional - default is csv

    if len(sys.argv) < 4:
        print((
                          'usage: %s sysdig_endpoint_url=<Sysdig Monitor Endpoint URL> sysdig_api_token=<Sysdig Monitor API Token> metric_search_str=<Metric you want to search in all dashboards> output=<optional - output file format>' %
                          sys.argv[0]))
        sys.exit(1)

    output = "csv"
    for arg in sys.argv:
        k = arg.split("=")
        if k[0] == "sysdig_endpoint_url":
            end_point = k[1]
        elif k[0] == "sysdig_api_token":
            api_token = k[1]
        elif k[0] == "metric_search_str":
            metric = k[1]
        elif k[0] == "output":
            output = k[1].lower()

    if output != "csv" and output != "json":
        print("output needs to be either csv or json")
        print((
                          'usage: %s sysdig_endpoint_url=<Sysdig Monitor Endpoint URL> sysdig_api_token=<Sysdig Monitor API Token> metric_search_str=<Metric you want to search in all dashboards> output=<optional - output file format - csv or json>' %
                          sys.argv[0]))

        sys.exit()

    return end_point, api_token, metric, output


def get_dashboards(end_point, api_token):
    url = end_point + "/api/v3/dashboards/"

    payload = {}

    auth = "Bearer " + api_token
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.ok is False:
        print("Status: received an error while getting a dashboard - " + json.dumps(response.text))

    return response.text


def search_metrics(all_dashboards, end_point, metric):
    found_dashboards_list = []

    for dashboard in all_dashboards['dashboards']:
        if metric in json.dumps(dashboard):
            print("X", end="", flush=True)
            # metric found... search through panels and query
            for panel in dashboard["panels"]:
                panel_str = json.dumps(panel)
                if metric in panel_str:
                    panel_url = end_point + "/#/dashboards/" + str(dashboard["id"]) + "/" + str(
                        panel["id"]) + "/edit?last=600"
                    found_dashboard_dict = {"dashboard_name": dashboard["name"], "panel_id": panel["id"],
                                            "panel_name": panel["name"], "panel_url": panel_url}
                    found_dashboards_list.append(found_dashboard_dict.copy())
                    found_dashboard_dict.clear()
        else:
            print(".", end="", flush=True)

    return found_dashboards_list


def write_csv(found_dashboards_list, metric):
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")

    file_name = "./" + metric + "_" + d1 + ".csv"
    fieldnames = ['dashboard_name', 'panel_id', 'panel_name', 'panel_url']

    with open(file_name, 'w', encoding='UTF8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(found_dashboards_list)


def write_json(found_dashboards_list, metric):
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")

    file_name = "./" + metric + "_" + d1 + ".json"
    fieldnames = ['dashboard_name', 'panel_id', 'panel_name', 'panel_url']

    with open(file_name, 'w', encoding='UTF8', newline='') as outfile:
        outfile.write(json.dumps(found_dashboards_list))


def print_summary_output(found_dashboards_list, metric, total_dashboards):
    unique_dashboards_list = list(set([x["dashboard_name"] for x in found_dashboards_list]))

    print("")
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print("Script attempted to search - " + metric + " - in " + str(
        total_dashboards) + " dashboards and found in "
          + str(len(found_dashboards_list)) + " panels in " + str(len(unique_dashboards_list)) + " dashboards")

    if len(found_dashboards_list) > 0:

        print("-" * 100)
        print("list of all dashboards having metric - " + metric)
        print("-" * 100)
        print("\n".join(unique_dashboards_list))
        print("-" * 100)

        print("list of all dashboards and panels having metric - " + metric)

        for dashboard in found_dashboards_list:
            print("-" * 100)
            print("dashboard: " + dashboard["dashboard_name"])
            print("panel id: " + str(dashboard["panel_id"]))
            print("panel name: " + dashboard["panel_name"])
            print("panel url: " + dashboard["panel_url"])


if __name__ == '__main__':
    search_dashboard()
