import os
import time
from job_post import *
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def getDriver():
    web_driver_location = os.path.join('C:\Program Files (x86)', "chromedriver.exe")
    return webdriver.Chrome(web_driver_location)

def openWebsite(driver, url):
    #opens on google search.
    driver.get(url)
    time.sleep(10)
    #get the show more jobs element link and load that page.
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)
    google_job_columns = soup.find_all('g-link', id='fMGJ3e')
    job_postings_link = google_job_columns[0].a['href']
    #load job listings page.
    driver.get(job_postings_link)
    time.sleep(10)
    
def loadFullJobsList(driver):
    for i in range(10):
        #get the last element.
        job_elements = driver.find_elements(By.XPATH, '//div[@data-hveid="CAEQAQ"]//li')
        #scroll to it which will load more jobs. Check out moveToElement.
        driver.execute_script("arguments[0].scrollIntoView();", job_elements[-1])
        time.sleep(10)

def getAllJobs(driver):
    all_jobs = []
    job_page_source = driver.page_source
    job_soup = BeautifulSoup(job_page_source)
    check_list_tag = lambda tag : tag.name == 'li' and tag.has_attr('data-ved')
    check_div_tag = lambda tag : tag.has_attr('decode-data-ved') and tag.has_attr('eid')
    
    jobs = job_soup.find_all(check_list_tag)
    all_jobs += jobs
    
    divs = job_soup.find_all(check_div_tag)
    for div in divs:
        jobs = div.find_all(check_list_tag)
        all_jobs += jobs
        
    return all_jobs

def getJobDetails(driver, jobs):
    jobDetails = []
    for job in jobs:
        jobObject = JobPost(job)
        jobObject.setJobId()
        jobObject.setJobRole()
        jobObject.setCompany()
        jobObject.setSource()
        jobObject.setLocation()
        jobDetails.append(jobObject)
    return jobDetails
        
def getElements(driver):
    xpath = '//div[@class="BjJfJf PUpOsf"]'
    return driver.find_elements(By.XPATH, xpath)

def getJobDescriptions(driver, job_details, tech):
    desc = []
    for job in job_details:
        if job.jobid == -1:
            desc.append('Null')
        else:
            link = 'https://www.google.com/search?q={}+jobs+in+india&ibp=htl;jobs&sa=X&ved=2ahUKEwiiwZO29qDwAhV26XMBHYJXDWgQudcGKAJ6BAgEECg&sxsrf=ALeKk00sqmTngAezwQPgjYkcTgYDEIYsYA:1619612416671#fpstate=tldetail&htivrt=jobs&htidocid={}%3D%3D'.format(tech, job.jobid)
            driver.get(link)
            time.sleep(8)
            xpath1 = '//div[@data-encoded-doc-id="{}"]//div[@class="YgLbBe YRi0le"]//span'.format(job.jobid)
            xpath2 = '//div[@data-encoded-doc-id="{}"]//div[@class="YgLbBe YRi0le"]//span//span[@class="WbZuDe"]'.format(job.jobid)
            text1 = driver.find_element_by_xpath(xpath1).get_attribute('textContent')
            
            try:
                text2 = driver.find_element_by_xpath(xpath2).get_attribute('textContent')
            except:
                text2 = ""
                
            desc.append(text1 + ' ' + text2)
    return desc

def merge_description(job_details, descriptions):
    final_data = []
    for (job, desc) in zip(job_details, descriptions):
        job.setDescription(desc)
        final_data.append(job)
    return final_data

def generateDictionary(jobs):
    jobs_dict = {
        'Role' : [],
        'Company' : [],
        'Source' : [],
        'Location' : [],
        'Description' : []
    }
    
    for job in jobs:
        jobs_dict['Role'].append(job.role)
        jobs_dict['Company'].append(job.company)
        jobs_dict['Source'].append(job.source)
        jobs_dict['Location'].append(job.location)
        jobs_dict['Description'].append(job.description)
        
    return jobs_dict
