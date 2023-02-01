# search-dashboards
Search particular metric in all dashboards. It simply uses string to check wehther metric exists or not so it can be used for the complete metric or partial metric.

It creates either csv (default) or json output file and prints the summary of dashbard/panel info with matched metric.

This utility is written in Python3 and uses request module to query dashboards in Sysdig.

### Pre-Req:
Make sure python3 is installed.
Make sure requests module for python3 is installed
Get Sysdig Monitor API Token (Look at next slide on how to get Sysdig Monitor API Token)


### Invoke the script
Script takes 4 command line arguments as key=value pair:

 **sysdig_endpoint_url** -> Sysdig backend's SaaS endpoint URL for your account - check for more info - https://docs.sysdig.com/en/docs/administration/saas-regions-and-ip-ranges/
 
 **sysdig_api_token** -> Sysdig Monitor API Token. It will use the token to query dashbaords through REST API

 **Metric** -> Metric you are interested searching in the dashboard. You don't need to specify the complete metric, partial metric name is allowed.
 
 **output** -> Optional - values can be either "csv" or "json". It will create a file in specified output format. It creates a file with <Metric>_<Today's date>.<output>
 
 

```
earch_dashboards.py sysdig_endpoint_url=<sysdig_endpoint_url> sysdig_api_token=<sysdig_api_token> metric_search_str=<metric_search_str> output=<output>  

example:
python3 earch_dashboards.py sysdig_endpoint_url=https://us2.app.sysdig.com sysdig_api_token=AAAAAAAAAAAA metric_search_str=memory output=json
```


### How to get Sysdig Monitor API Token:

1. Login to your Sysdig UI
2. Click on your Initial Icon at the bottom left
3. Go to Settings
4. Go to User Profile
5. Copy Sysdig Monitor API Token
