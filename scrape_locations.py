from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import requests
import time
import os
from math import ceil
import glob
import pandas as pd

file_path = '/home/dan/air_quality/data/site_locations.csv'

def find_element(by, string, timeout=30):
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    return WebDriverWait(driver, timeout,ignored_exceptions=ignored_exceptions)\
                    .until(expected_conditions.presence_of_element_located((by, string)))

#check if file exists. if not, create it and add header
if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        f.write('station,classification,road_distance,height,latitude,longitude\n')


#navigate to url
url = 'https://www.londonair.org.uk/london/asp/publicdetails.asp'
driver = webdriver.Firefox()
driver.get(url)


#loop through stations
#dropdown = WebDriverWait(driver, 30,ignored_exceptions=ignored_exceptions)\
#                    .until(expected_conditions.presence_of_element_located((By.ID, 'select-sites')))
dropdown = find_element(By.ID, 'select-sites')
select = Select(dropdown)

num_stations = len(select.options)
print('number of stations: {}'.format(num_stations-1))

start_idx = 66

for station_idx in range(start_idx,num_stations):
    dropdown = find_element(By.ID, 'select-sites')
    select = Select(dropdown)
    station = select.options[station_idx]
    station_text = station.text
    station_val = station.get_attribute('value')
    
    time.sleep(2)

    print('Station {}: {}'.format(station_idx,station_text))
    select.select_by_value(station_val)

    time.sleep(2)

    #click to see monitoring site details
    site_details_btn = find_element(By.LINK_TEXT, 'View monitoring site details')
    site_details_btn.click()

    xpath_classification = '/html/body/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/em/a'

    xpath_distance_to_road = '/html/body/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[4]/td[2]/em'

    xpath_sampling_height = '/html/body/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[5]/td[2]/em'

    classification = find_element(By.XPATH, xpath_classification).text
    distance_to_road = find_element(By.XPATH, xpath_distance_to_road).text
    height = find_element(By.XPATH, xpath_sampling_height).text
    print('classification:',classification)
    print('distance to road:',distance_to_road)
    print('sampling height:',height)

    site_location_btn = find_element(By.LINK_TEXT, 'site location')
    site_location_btn.click()

    time.sleep(2)

    xpath_location = '/html/body/div[1]/div[2]/div/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/em'
    location = find_element(By.XPATH, xpath_location).text
    latitude, longitude = location.split(', ')
    print('latitude: {}'.format(latitude))
    print('longitude: {}'.format(longitude))

    sampling_details_btn = find_element(By.LINK_TEXT, 'sampling details')
    sampling_details_btn.click()

    #append data to lists
    str_data = ','.join([station_text,
                         classification,
                         distance_to_road,
                         height,
                         latitude,
                         longitude])
    str_data = str_data + '\n'

    with open(file_path, 'a') as f:
        f.write(str_data)




