import pandas as pd
import numpy as np


import urllib.request
import requests
from bs4 import BeautifulSoup
import os
import time


from multiprocessing import Pool
from selenium import webdriver


def web_scraping(page):
    lst_name = []
    lst_link = []

    driver = webdriver.PhantomJS(os.getcwd() + "/dependency/phantomjs-2.1.1-windows/bin/phantomjs.exe")

    url = 'https://www.coursera.org/directory/courses?page=' + str(page)
    driver.get(url)
    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()

    soup = BeautifulSoup(res, 'lxml')
    c_link = soup.findAll('a', {'class':'c-directory-link'}, href=True)

    for c in c_link:
        lst_name.append(c.getText())
        lst_link.append('https://coursera.org' + str(c['href']))

    data_dict = {'Name':lst_name, 'Link':lst_link}
    return data_dict

warnings.simplefilter('ignore')
if __name__ == '__main__':
    start = time.time()

    choke = np.arange(1, 115, 10)[:-1]
    lst_name = []
    lst_link = []
    dataset = {'Name': lst_name, 'Link':lst_link}
    for i in choke:
        
        p = Pool(10)
        data = p.map(web_scraping, range(i, i+10))
        p.terminate()
        p.join()
        
        lst_name = []
        lst_link = []
        scraped_data = {'Name': lst_name, 'Link':lst_link}
        for d in data:
            scraped_data['Name'] += d['Name']
            scraped_data['Link'] += d['Link']
        
        dataset['Name'] += scraped_data['Name']
        dataset['Link'] += scraped_data['Link']


    end = time.time()

    

    pd.DataFrame(data=dataset).to_csv('coursera-courses-data.csv')
