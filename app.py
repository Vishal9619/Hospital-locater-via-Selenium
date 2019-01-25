import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# driver = webdriver.Chrome(chrome_options = options)
# print("launch start"
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
elem.clear()
elem.send_keys("DR VIJAY ENT HOSPITAL AJMER")
elem.send_keys(Keys.RETURN)
time.sleep(1)
hospital_suggestions = driver.find_element_by_class_name("hdpi")
items = hospital_suggestions.find_elements_by_class_name("pac-item")
print(len(items))
#print(items)
if(len(items)==1):
	#items.click()
	get_button = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[1]/form[1]/div[2]/div/button")
	get_button.click()
	time.sleep(2)
	#lat = driver.find_element_by_xpath("//*[@id='info_window']")
	
	print("Latitude = ",(driver.find_element_by_id('latitude')).get_attribute('value'))#lat.get_attribute('innerHTML'))
	print("Longitude= ",(driver.find_element_by_id('longitude')).get_attribute('value'))
	#time.sleep(5)
# for item in items:
# 	tt = item.find_elements_by_tag_name('span')
# 	hospital_name=""
# 	for individual in tt:
# 		h_name = individual.get_attribute('innerHTML')
# 		start_index=-1
# 		end_index=-1
# 		if(h_name.find('<span') != -1):
# 			start_index = h_name.index('<span')
# 		if(h_name.find('</span>') != -1):
# 			end_index = h_name.index('</span>')
# 		if(start_index!=-1 and end_index!=-1):
# 			end_index+=6
# 			for counter,i in enumerate(h_name):
# 				if(counter>=start_index and counter<=end_index):
# 					continue
# 				hospital_name+=i
# 		else:
# 			hospital_name+=h_name
# 		hospital_name+=' '

# 	print(hospital_name)
	

	# item.click()
	# time.sleep(10)
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
