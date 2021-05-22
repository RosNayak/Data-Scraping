from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class JobPost:
    
    def __init__(self, tag):
        self.element_tag = tag
    
    def setJobRole(self):
        self.role = self.element_tag.find('div', class_='BjJfJf PUpOsf').text
        
    def setCompany(self):
        self.company = self.element_tag.find('div', class_='vNEEBe').text
        
    def setSource(self):
        self.source = self.element_tag.find_all('div', class_='Qk80Jf')[1].text
        
    def setLocation(self):
        self.location = self.element_tag.find('div', class_='Qk80Jf').text
        
    def setJobId(self):
        try:
            check = lambda tag : tag.name == 'div' and tag.has_attr('data-encoded-doc-id')
            self.jobid = self.element_tag.find(check)['data-encoded-doc-id']
        except:
            self.jobid = -1
            
    def setDescription(self, description):
        self.description = description
        
    def getDetails(self):
        details = []
        details.append(self.jobid)
        details.append(self.role)
        details.append(self.company)
        details.append(self.source)
        details.append(self.location)
        return details
