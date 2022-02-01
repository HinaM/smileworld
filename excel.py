import pygsheets
gc = pygsheets.authorize(service_file='../tough-electron-312216-e50c97e4c7c5.json')
sht = gc.open_by_url(
'https://docs.google.com/spreadsheets/d/1UkCDXA3WOU_AzEdE0OXf0e_zcqZd4VQfyJLbwAz0TdI/edit?usp=sharing'
)
def e(event):
    wks_list = sht.worksheets()
    print(wks_list)
    