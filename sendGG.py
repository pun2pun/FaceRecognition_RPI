import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds' , 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Python to Sheet-acac1079924d.json', scope)

gc = gspread.authorize(creds)

wks = gc.open('Student sheet').sheet1

print(wks.get_all_recorde())