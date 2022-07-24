# search-dashboards
Search particular metric in all dashboards


This utility searches for given metric in all the dashboards and provides the list of dashboards/panels that contain the given metric.

This utility is written in Python3 and uses request module to query dashboards in Sysdig.

### Pre-Req:
Make sure python3 is installed.
Make sure requests module for python3 is installed
Get Sysdig Monitor API Token (Look at next slide on how to get Sysdig Monitor API Token)


### Invoke the script
Script takes 2 command line arguments:

 **Sysdig Monitor API Token** -> Sysdig Monitor API Token. It will use the token to associate the dashboard with a particular user/team. 

 **Metric** -> Metric you are interested searching in the dashboard

_python3 search_dashboards.py \<Sysdig Monitor API Token/> \<Metric you want to search/> _



### How to get Sysdig Monitor API Token:

1. Login to your Sysdig UI
2. Click on your Initial Icon at the bottom left
3. Go to Settings
4. Go to User Profile
5. Copy Sysdig Monitor API Token
