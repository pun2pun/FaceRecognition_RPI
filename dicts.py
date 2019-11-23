import gspread
from oauth2client.service_account import ServiceAccountCredentials

def addSheet(number,ids,name,time):
        
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Python to Sheet-e59681cb97ad.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Student sheet").sheet1
    
    sheet.update_cell(number+1,1,number)
    sheet.update_cell(number+1,2,ids)
    sheet.update_cell(number+1,3,name)
    sheet.update_cell(number+1,4,time)
    sheet.update_cell(number+1,5,'1')


