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


def download_wait(directory, timeout = 30):
    """
    Wait for download to finish
    
    Args
    ----
    directory: str
        The directory to which the file(s) are being downloaded
    timeout: int
        How many seconds to wait before timing out
    """
    seconds = 0
    while True:
        time.sleep(1)
        #if path ends with .part, then we're not done
        if len(glob.glob('{}/*csv.part'.format(directory))) == 0:
            print('Download finished!')
            break
        seconds += 1
        if seconds > timeout:
            raise Exception('download timed out')


#first remove any straggling files
files = glob.glob('/home/dan/Downloads/LaqnData*.csv')
if files:
    for file in files:
        os.remove(file)


#change download preferences
fp = webdriver.FirefoxProfile()
fp.set_preference('browser.download.manager.showWhenStarting', False)
fp.set_preference('browser.download.alwaysOpenPanel', False)

#navigate to url
url = 'https://www.londonair.org.uk/london/asp/datadownload.asp'
driver = webdriver.Firefox(firefox_profile = fp)
driver.get(url)


#loop through stations
select = Select(driver.find_element_by_id('species1'))
num_stations = len(select.options)
print('number of stations: {}'.format(num_stations))

missing_stations = ['GN5', 'TL4', 'GR9', 'ME5', 'NM4']

for station_idx in range(1,num_stations):
    select = Select(driver.find_element_by_id('species1'))
    station = select.options[station_idx]

    if 'closed' not in station.text and station.get_attribute('value') in missing_stations:


        print(station_idx,station.text,':', station.get_attribute('value'))
        #select station from drop-down menu
        station_val = station.get_attribute('value')
        print(station_val)
        select.select_by_value(station_val)
        
        #go to next page
        xpath_to_button = '/html/body/div[1]/div[2]/div/div/div/form[1]/table/tbody/tr[4]/td/input'
        a = driver.find_element(By.XPATH, xpath_to_button)
        a.click()
        
        checkboxes = driver.find_elements_by_css_selector("#checkbox1")
        
        batch_size = 6
        num_batches = ceil(len(checkboxes) / batch_size)
        for i in range(num_batches):
            #click checkboxes
            start_idx = batch_size * i
            end_idx = min(len(checkboxes), start_idx + batch_size)
            for checkbox in checkboxes[start_idx:end_idx]:
                time.sleep(0.1)
                checkbox.click()
        
            #set year 1 to oldest time possible in data
            select = Select(driver.find_element_by_id('year1'))
            select.select_by_value('1993')
        
            #change averaging period to daily mean
            select = Select(driver.find_element_by_id('avperiod'))
            select.select_by_value('daily')
        
            #Plot graph
            time.sleep(0.1)
            plot_button = driver.find_element(By.NAME, 'Submit')
            plot_button.click()
       

            #Download csv if it exists
            try:
                ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
                plot_button = WebDriverWait(driver, 30,ignored_exceptions=ignored_exceptions)\
                                    .until(expected_conditions.presence_of_element_located((By.ID, 'csv')))
                plot_button.click()
            
                #wait until download is complete
                download_wait('/home/dan/Downloads')
            
                #move data from Downloads to current directory
                cwd = os.getcwd()
                idx = 0
                os.rename('/home/dan/Downloads/LaqnData.csv',cwd+'/data/{}_{}.csv'.format(station_val,i))

            except:
                print('Download not happening, moving on.')
        
            #unclick checkboxes if not done
            checkboxes = driver.find_elements_by_css_selector("#checkbox1")
            if end_idx != len(checkboxes):
                for checkbox in checkboxes[start_idx:end_idx]:
                    time.sleep(0.1)
                    checkbox.click()
        
        driver.get(url)
