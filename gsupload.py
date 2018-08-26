import gspread
from oauth2client.service_account import ServiceAccountCredentials
from connector import getCred, getReport, getList, getToken

#Import data from AR

token = getToken()['access_token']
campaignList = getList(token)
parameters = ['name', 'events', 'reach', 'frequency', 'affinity']


for c in campaignList['data']:
    data = getReport(token, c['id'])['data']
    print(c['name'])
    print('Events: ' + str(data['totals']['events']))
    print('Reach: ' + str(data['totals']['reach']))
    print('Frequency: ' + str(data['totals']['frequency']))
    print('Affinity in target group: ' + str(data['totals']['affinity']))
    for rpi in data['reportItems']:
        print('CID: ' + str(rpi['name']))
        print('Events: ' + str(rpi['events']))
        print('Reach: ' + str(rpi['reach']))
        print('Frequency: ' + str(rpi['frequency']))
        print('Affinity in target group: ' + str(rpi['affinity']))

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('KPI_Dashboard-9eceeadde073.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('JP-POL-Dashboard').sheet1
wks.resize(rows=2)

leng = len(campaignList['data'])+1
range1 = wks.range('A2:A'+str(leng))
i = 0
for cell in range1:
    cell.value = dealDictDF[i]['deal_owner']
    i += 1
for p in range(len(parameters)-1):
    i = 0
    range2 = wks.range(chr(p+98)+'2:'+chr(p+98) + str(leng))
    for cell in range2:
        cell.value = dealDictDF[i][parameters[p+1]]
        i += 1
    range1.extend(range2)

# Update in batch
wks.update_cells(range1)
