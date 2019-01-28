import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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


# path = "C:/Users/axafrance/Desktop/Hospital_Rajasthan.xlsx"

# all_hospital = pd.read_excel(path)
# full_details = all_hospital.iloc[0:len(all_hospital) ,[0,1]]

driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\chromedriver')
driver.get("https://www.gps-coordinates.net/")
#time.sleep(10)
assert "GPS coordinates" in driver.title
# give time for website to open up
try:
	elem = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,"address"))) 
except:
	print("search box isn't yet available")
# print("search over")
time.sleep(2)
hospital = "AJMER ENT HOSPITAL ajmer"
hospital_key = "AJMER ENT HOSPITAL ajmer"
elem.clear()
elem.send_keys(hospital)
time.sleep(2)
hospital_suggestions = driver.find_element_by_class_name("hdpi")
items = hospital_suggestions.find_elements_by_class_name("pac-item")
print(len(items))
#print(items)

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
	counter = find_suitable_hospital(hospital_key,hospital_name)
	if(counter>max_counter):
		max_counter = counter
		final_hospital_item_index = index
if(final_hospital_item_index != -1):
	items[final_hospital_item_index].click()
	get_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button")
	get_button.click()
	time.sleep(2)
	print("Latitude = ",(driver.find_element_by_id('latitude')).get_attribute('value'))#lat.get_attribute('innerHTML'))
	print("Longitude= ",(driver.find_element_by_id('longitude')).get_attribute('value'))
	(driver.find_element_by_id('latitude')).clear()
	(driver.find_element_by_id('longitude')).clear()

	# item.click()
time.sleep(5)
	# gecor = driver.find_element_by_class_name("infoWindow")
	# latitude = gecor.find_element_by_class_name("inputLat")
	# longitude = gecor.find_element_by_class_name("inputLng")
	# sea = gecor.find_element_by_class_name("seaHeight")
	#print(tt)
	# print(latitude.get_attribute('value'))
	# print(longitude.get_attribute('value'))
	# print(sea.get_attribute('value'))
#print(items[1].text)
#elem.send_keys(Keys.RETURN)

assert "No results found." not in driver.page_source
driver.close()