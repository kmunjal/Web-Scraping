#!/usr/bin/env python
# coding: utf-8

# In[148]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
from tqdm.notebook import tqdm
import re
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pymongo


# In[ ]:


# In[ ]:


# Question 1
# Done


# In[154]:


# Question 2

driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)

driver.get("https://opensea.io/collection/boredapeyachtclub?search[stringTraits][0][name]=Fur&search[stringTraits][0][values][0]=Solid%20Gold");

# get number of elements to click on
find_length = 8

# declare a counter to track the loop and keep track of which element in the list to click
list_count = 0

apes = []
# loop through elements and click the element at [list_count] index
while (list_count < find_length):
    # get the elements
    first_el = driver.find_elements(By.XPATH,'//div[@class="sc-29427738-0 sc-e7851b23-1 dVNeWL hfa-DJE Asset--loaded"]')

    # click the current indexed element
    first_el[list_count].click()
    
    # Ouput ape number
    ape_number = driver.find_element(By.XPATH,'//h1[@class="sc-29427738-0 hKCSVX item--title"]')
    text = ape_number.text
    apes.append(text)
    print(text)
    
    # store to disk
    filename_prefix = 'bayc_'
    filename_suffix = '.html'
    
    html_source = driver.page_source
    filename = filename_prefix + text + filename_suffix
    with open(filename, "w") as file:
        file.write(html_source)

    # go back
    time.sleep(3)
    driver.back()
    list_count = list_count + 1
    
    
driver.quit()


# In[149]:


# Question 3
client = MongoClient("mongodb+srv://kmunjal:Onedirection123@kmunjal.ivcwvn1.mongodb.net/?retryWrites=true&w=majority")
client


# In[152]:


# Create a new database called "bayc"
db = client["bayc"]

# Create a new collection called "bayc"
collection = db["bayc"]
collection


# In[187]:


# read html files
def loadString(f="test.html"):
    try:
        html = open(f, "r", encoding='utf-8').read()
        return(html)
    except Exception as ex:
        print('Error: ' + str(ex))

filename_prefix = 'bayc_'
filename_suffix = '.html'

for i in range(8):
    file_name = filename_prefix + apes[i] + filename_suffix
    page = loadString(file_name)
    soup = BeautifulSoup(page, "html.parser")
    
    # get ape number
    ape_number = soup.find("h1", class_ = "sc-29427738-0 hKCSVX item--title").text
    #print(ape_number)
    
    types =[]
    values = []
    #attributes
    attributes_type = soup.find_all("div", class_ = "Property--type")
    attributes_value = soup.find_all("div", class_ = "Property--value")
    
    for attribute in attributes_type:
        text = attribute.text
        types.append(text)
        #print(text)
        
    for attribute in attributes_value:
        text = attribute.text
        values.append(text)
        #print(text)
    
    # Insert the ape's information into the MongoDB collection
    document = {
                'ape_number': ape_number,
                'types' : types,
                'values' : values
    
            }
    collection.insert_one(document)


# In[198]:


# Question 4
base_url = 'https://www.yellowpages.com/search?search_terms=pizzeria&geo_location_terms=San+Francisco%2C+CA'
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
page = requests.get(base_url, headers = headers)
page


# In[199]:


# Reading entire page and creating a BeautifulSoup object
soup = BeautifulSoup(page.content, "html.parser")


# In[206]:


# Top 30
top_30 = soup.findAll('div', class_='result')


# Remove the ads
top_30.pop(0)


# In[207]:


fname = "sf_pizzeria_search_page" + '.html'

with open(fname, 'w') as f:
    f.write(str(top_30))
    f.close()


# In[217]:


# Question 5 and 6
with open(fname, 'r') as f:
    soup = BeautifulSoup(f, "html.parser")
f.close()


# In[243]:


client = MongoClient("mongodb+srv://kmunjal:<password>@kmunjal.ivcwvn1.mongodb.net/?retryWrites=true&w=majority")

pizzeria = client["pizzeria"]

# Creating/Accessing a collection
sf_pizzerias = pizzeria["sf_pizzerias"]
sf_pizzerias


# In[223]:


# Defining a url prefix to append to the shop urls
url_prefix = 'https://www.yellowpages.com'
    
# Identifying all the titles on the search page
title = soup.find_all('h2', class_ = 'n')


# In[244]:


# Looping over all the identified titles
for elem in title:

    if elem.text[0].isdigit():
            
        # Cleaning the label and extracting shop rank and shop name from it.
        clean_label = re.sub(r'\\[a-z0-9]{3}','',elem.text)
        shop_rank = clean_label.split('.')[0]
        shop_name = clean_label.split('.')[1]
        
        #print(shop_rank)
        #print(shop_name)
        
        # Extracting the shop url and appending the url prefix defined earlier
        url = elem.find('a')['href']
        shop_url = url_prefix + str(url)
        #print(shop_url)
        
        # trip advisor rating
        # star rating 
        # number of reviews 
        # number of TA reviews 
        # “$” signs IIE
        # years in business
        # review 
        # amenities
        
        document = {
                'Rank': shop_rank,
                'Name' : shop_name,
                'Url' : shop_url 
        }
        #print(document)
    sf_pizzerias.insert_one(document) 


# In[246]:


# Question 7
query = {}
myquery = {"Url": 1,
           "Rank":1}

mydoc = sf_pizzerias.find(query, myquery)

out = dict()
for x in mydoc:
#     print (x)
    out[x['Rank']] = x['Url']


# In[249]:


#for key, value in out.items():
    #print (key, value)


# In[248]:


base_fname = 'sf_pizzerias_'
for key, value in tqdm(out.items()):
    print (key, value)
    
    search_page = requests.get(value, headers = headers)
    search_content = str(search_page.content)
    
    fname = base_fname + str(key) + '.html'
    
    with open(fname, 'w') as f:
        f.write(search_content)
    f.close()
    
    time.sleep(random.randint(4,6))


# In[250]:


# Question 8
fname = base_fname + list(out.keys())[0] + '.html'
fname


# In[271]:


new_info = {}
for key in list(out.keys()):
    fname = base_fname + str(key) + '.html'
    
    with open(fname, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
    f.close()

    shop_data = {}
    
    name = soup.find('h1', class_ = "dockable business-name").text
    #print(name)
    box = soup.find('section', class_ = "inner-section")
    phone = box.find('a', class_ = "phone dockable").text
    shop_data["Phone"] = phone
    #print(phone)
    address = box.find('span', class_ = "address").text
    shop_data["Address"] = address
    #print(address)
    
    try:
        website = box.find('a', class_ = "website-link dockable")["href"]
        shop_data["Website"] = website
    except:
        pass

    #print(shop_data)
    
    # This does not add it to Mongodb properly
    #sf_pizzerias.insert_one(shop_data)
    new_info[key] = shop_data


# In[291]:


# Question 9
base_api = "http://api.positionstack.com/v1/forward?access_key=<key>&query="


# In[292]:


import json
for key in new_info.keys():
    try:
        address = new_info[key]['Address']
        api_url = base_api + address
        
        response = requests.get(api_url, headers=headers)
        content = response.content
        
        json_res = json.loads(content)
        
        new_info[key]['latitude'] = json_res['data'][0]['latitude']
        new_info[key]['longitude'] = json_res['data'][0]['longitude']
    except:
        pass
    
    #print(new_info[key])
    sf_pizzerias.update_many({"Rank":str(key)},{"$set": new_info[key]})


# In[293]:


filter_ = {}
fields = {}
# We pass both the filter criteria and the relevant fields to the find query
query_out = sf_pizzerias.find(filter_)
for x in query_out:
    print(x)

