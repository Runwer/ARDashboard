import gspread
from oauth2client.service_account import ServiceAccountCredentials
from connector import getCred, getReport, getList, getToken

#Import data from AR

token = getToken()['access_token']
campaignList = getList(token)
parameters = ['campaignName', 'name', 'events', 'reach', 'frequency', 'affinity']

output = []
empty = {'campaignName': '', 'name': '', 'events': '', 'reach': '', 'frequency': '', 'affinity': ''}

for c in campaignList['data']:
    data = getReport(token, c['id'])['data']
    for rpi in data['reportItems']:
        outDict = {}
        outDict['campaignName'] = (c['name'])
        for p in parameters[1:]:
            outDict[p] = rpi[p]
        output.append(outDict)
    outDict = {}
    outDict['campaignName'] = (c['name'])
    outDict['name'] = ('Total')
    for p in parameters[2:]:
        outDict[p] = data['totals'][p]
    output.append(outDict)
    output.append(empty)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('KPIDashboard.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('JP-POL-Dashboard').sheet1
wks.resize(rows=2)

leng = len(output)+1
range1 = wks.range('A2:A'+str(leng))
i = 0
for cell in range1:
    cell.value = output[i]['campaignName']
    i += 1
for p in range(len(parameters)-1):
    i = 0
    range2 = wks.range(chr(p+98)+'2:'+chr(p+98) + str(leng))
    for cell in range2:
        cell.value = output[i][parameters[p+1]]

        i += 1
    range1.extend(range2)

# Update in batch
wks.update_cells(range1)
