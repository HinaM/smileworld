'''
import pygsheets
gc = pygsheets.authorize(service_file="C:\\Users\\user\\Desktop\\smileworld\\smile-world-340813-6b2b86613f09.json")
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1FsfvfBLAazAehvUqaVH9rH6zzdCowoYpedVsDSkuAdk/')
wks_list = sht.worksheets()
wks = sht[0]


if wks.cell('A2')=="王":
    print("王")
'''

from fileinput import filename
import gspread
gc=gspread.service_account(filename='smile-world-340813-6b2b86613f09.json')
sh=gc.open_by_key('1FsfvfBLAazAehvUqaVH9rH6zzdCowoYpedVsDSkuAdk')
worksheet=sh.sheet1

res=worksheet.get_all_records()
print(res)

x="王"
userList = worksheet.col_values(1)
for i in range(len(userList)):
    if userList[i]==x:
        print(i)
i+=1
rowList=worksheet.row_values(i)
print(rowList)
print(userList)
worksheet.update('A2', '張')
print(res)