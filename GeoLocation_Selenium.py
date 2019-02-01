import time
import pandas as pd
import xlwt
from xlwt import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#Program to return count of words from given hospital name to suggested hospital names 
def find_suitable_hospital(hospital_key,hospital_name):
	counter = 0
	for word in hospital_key:
		if(word in hospital_name):
			counter+=1
	return counter

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# driver = webdriver.Chrome(chrome_options = options)

#Reading data from Excel file
all_hospital = pd.read_excel("C:/Users/axafrance/Desktop/Hospital_Rajasthan.xlsx")
full_details = all_hospital.iloc[0:len(all_hospital) ,[0,1]]

wb = Workbook()  # making our new workbook
sheet1 = wb.add_sheet('Exact coordinates')
sheet2 = wb.add_sheet('Probable coordinates')
sheet3 = wb.add_sheet('No coordinates')

driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\chromedriver')
driver.get("https://www.gps-coordinates.net/")
assert "GPS coordinates" in driver.title
# give time for website to open up
try:
	elem = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,"address"))) 
except:
	print("search box isn't yet available")
time.sleep(3)
elem.clear()

sheet1_index_row = 0
sheet1_index_col = 0
sheet2_index_row = 0
sheet2_index_col = 0
sheet3_index_row = 0
sheet3_index_col = 0
# Iterating rows from Excel file
for index, row in full_details.iterrows():
	hospital = row["Hospital Name"]+" "+row["Hospital District"]
	time.sleep(2)
	elem.clear()
	elem.send_keys(hospital)
	time.sleep(1)
	hospital_suggestions = driver.find_element_by_class_name("hdpi")
	items = hospital_suggestions.find_elements_by_class_name("pac-item")
	print(len(items))
	#Printing the no. of suggestions occuring for a particular hospital
	if(len(items)==1):
		items[0].click()  # first suggestion clicked
		get_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button")
		get_button.click()  # "Get GPS coordinates" button clicked
		time.sleep(2)
		sheet1.write(sheet1_index_row,sheet1_index_col,hospital)
		sheet1.write(sheet1_index_row,sheet1_index_col+1,(driver.find_element_by_id('latitude')).get_attribute('value'))
		sheet1.write(sheet1_index_row,sheet1_index_col+2,(driver.find_element_by_id('longitude')).get_attribute('value'))
		sheet1_index_row+=1
		sheet1_index_col+=1
		# print("Latitude = ",(driver.find_element_by_id('latitude')).get_attribute('value'))
		# print("Longitude= ",(driver.find_element_by_id('longitude')).get_attribute('value'))
		(driver.find_element_by_id('latitude')).clear()
		(driver.find_element_by_id('longitude')).clear()

	elif(len(items)>1):
		max_counter = 0
		final_hospital_item_index = -1
		for index,item in enumerate(items):
			counter = 0
			tt = item.find_elements_by_tag_name('span')
			hospital_name=""
			for individual in tt:
				h_name = individual.get_attribute('innerHTML')
				start_index=-1
				end_index=-1
				if(h_name.find('<span') != -1):
					start_index = h_name.index('<span')
				if(h_name.find('</span>') != -1):
					end_index = h_name.index('</span>')
				if(start_index!=-1 and end_index!=-1):
					end_index+=6
					for counter,i in enumerate(h_name):
						if(counter>=start_index and counter<=end_index):
							continue
						hospital_name+=i
				else:
					hospital_name+=h_name
				hospital_name+=' '
			counter = find_suitable_hospital(hospital,hospital_name)
			if(counter>max_counter):
				max_counter = counter
				final_hospital_item_index = index
		if(final_hospital_item_index != -1):
			items[final_hospital_item_index].click()  # Clicking the best suggestion
			get_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button")
			get_button.click()  # "Get GPS coordinates" button clicked
			time.sleep(2)
			sheet2.write(sheet2_index_row,sheet2_index_col,hospital)
			sheet2.write(sheet2_index_row,sheet2_index_col+1,(driver.find_element_by_id('latitude')).get_attribute('value'))
			sheet2.write(sheet2_index_row,sheet2_index_col+2,(driver.find_element_by_id('longitude')).get_attribute('value'))
			sheet2_index_row+=1
			sheet2_index_col+=1
			# print("Latitude = ",(driver.find_element_by_id('latitude')).get_attribute('value'))
			# print("Longitude= ",(driver.find_element_by_id('longitude')).get_attribute('value'))
			(driver.find_element_by_id('latitude')).clear()
			(driver.find_element_by_id('longitude')).clear()

	else:
		print("Hospital not available on map")
		sheet3.write(sheet3_index_row,sheet3_index_col,hospital)
		sheet3_index_row+=1
		sheet3_index_col+=1
wb.save('xlwt GeoLocations.xls')
assert "No results found." not in driver.page_source
driver.close()
