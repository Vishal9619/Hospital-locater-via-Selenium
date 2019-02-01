import requests, json 
import xlwt, time
import pandas as pd
from xlwt import Workbook

all_hospital = pd.read_excel("C:\\Users\\axafrance\\Desktop\\Hospital_Rajasthan.xlsx")
full_details = all_hospital.iloc[0:len(all_hospital) ,[0,1]]  #len(all_hospital)

wb = Workbook()  # making our new workbook
sheet1 = wb.add_sheet('Google coordinates')
sheet2 = wb.add_sheet('No coordinates')
# enter your api key here
api_key = 'AIzaSyCNToPLZPsm7MNWQCN4kFKuJrfV3rX6I5s'

# url variable store url
url = 'https://maps.googleapis.com/maps/api/geocode/json?'

sheet1_index_row=1
sheet2_index_row=1

for index, row in full_details.iterrows():
	hospital = row["Hospital Name"]+" "+row["Hospital District"]
	# take place as input
	place = hospital  #"dr vijay ent hospital ajmer"
	new_place=""
	for word in place.split():
		new_place+=word+"+"
	new_place+="India"
	# get method of requests module returns response object 
	res_ob = requests.get(url + 'address=' + new_place + '&key=' + api_key)
	time.sleep(1)
	x = res_ob.json()
	if(x['status']=="OK"):
		sheet1.write(sheet1_index_row,0,row["Hospital Name"])
		sheet1.write(sheet1_index_row,1,row["Hospital District"])
		sheet1.write(sheet1_index_row,2,x['results'][0]['geometry']['location']["lat"])
		sheet1.write(sheet1_index_row,3,x['results'][0]['geometry']['location']["lng"])
		sheet1_index_row+=1
	else:
		sheet2.write(sheet2_index_row,0,row["Hospital Name"])
		sheet2.write(sheet2_index_row,1,row["Hospital District"])
		sheet2_index_row+=1
	wb.save('GeoLocations.xlsx')
	#print(str(sheet1_index_row)+"->"+new_place)

wb.save('GeoLocations.xlsx')