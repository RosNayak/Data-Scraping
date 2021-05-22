import os
import time
import pandas as pd
from utility import *
from job_post import *
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

techs = ['Android', 'Full Stack', 'Data Science']
count = 0

for tech in techs:
    count += 1
    
    data_dict = {
        'Role' : [],
        'Company' : [],
        'Source' : [],
        'Location' : [],
        'Description' : []
    }
    
    print('Scraping', tech, 'jobs')
    driver = getDriver()
    url = 'https://www.google.com/search' + '?q={} jobs in India'.format(tech)
    openWebsite(driver, url)

    loadFullJobsList(driver)
    jobs = getAllJobs(driver)

    job_details = getJobDetails(driver, jobs)

    descriptions = getJobDescriptions(driver, job_details, tech)

    jobs = merge_description(job_details, descriptions)
    jobs_dict = generateDictionary(jobs)
    
    for key in jobs_dict:
        data_dict[key] += jobs_dict[key]
        
    driver.quit()
    
    data = pd.DataFrame(data_dict)
    data.to_csv(tech + '_final.csv')
