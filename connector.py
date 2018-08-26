import requests
import json

def getCred(file):
    with open(file) as f:
        return json.load(f)

def getToken():
    baseurl = 'https://oauth.audiencereport.com/oauth/access_token'
    get_token = getCred('credentials.json')
    return((requests.post(baseurl, params=get_token)).json())

def getList(token):
    baseurl = 'https://campaign-api.audiencereport.com/campaigns'
    header = {'Authorization': 'Bearer '+token}
    par = {'start': '0', 'maxResults':'1000', 'sortColumn': 'creation-date', 'sortDirection': 'desc' }
    return(requests.get(baseurl, par, headers=header).json())

def getReport(token, cID):
    baseurl = 'https://campaign-api.audiencereport.com/reports/'
    header = {'Authorization': 'Bearer '+token}
    par = {'id': cID}
    return(requests.get(baseurl+cID, headers=header).json())





