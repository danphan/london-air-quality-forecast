from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd


#navigate to url
url = 'https://www.londonair.org.uk/london/asp/datadownload.asp'
driver = webdriver.Firefox()
driver.get(url)


#loop through stations
select = Select(driver.find_element_by_id('species1'))
num_stations = len(select.options)

station_text_list = []
station_val_list = []

for option in select.options:
    if 'closed' not in option.text:
        station_text_list.append(option.text)
        station_val_list.append(option.get_attribute('value'))

data = {'abbreviation': station_val_list,
        'station': station_text_list}

df = pd.DataFrame(data)

df.to_csv('data/site_abbreviations.csv',index=False)
