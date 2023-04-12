#!/usr/bin/env python
# coding: utf-8

# # Individual Project 1

# ### Coding 1.2

# In[6]:


import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
import re
import time
import random
from tqdm.notebook import tqdm as tqdm


# In[94]:


URL = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&LH_Sold=1"
my_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
page = requests.get(URL, headers = my_header)


# In[49]:


# Reading entire page and creating a BeautifulSoup object
soup = BeautifulSoup(page.content, "html.parser")


# In[9]:


# Save the html page to a local file
with open("amazon_gift_card_01","a+") as f:
    f.write(str(soup))
f.close()


# In[11]:


# take your code in (a) and write a loop that will download the first 10 pages of search results. 
# Save each of these pages to "amazon_gift_card_XX.htm"

base_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&LH_Sold=1&_pgn="
page_count = 10
base_fname= "amazon_gift_card"
for i in tqdm(range(page_count)):
    # fetch result from page 1 to page 10
    page_num = i+1
    url = base_url + str(page_num)
    
    # Making get requests to fetch each individual page
    search_page = requests.get(url, headers = my_header)
    search_page_content = BeautifulSoup(search_page.content, "html.parser")
    
    # Saving the html page to a local file
    fname = f"{base_fname}_{page_num}.html"
    with open(fname,"a+") as f:
        f.write(str(search_page_content))
    f.close()
    
    # Adding sleep time
    time.sleep(10)


# In[76]:


for i in tqdm(range(page_count)):
    # Creating a dynamic file name to loop over the saved files
    fname= f"amazon_gift_card_{i+1}.html"
    with open(fname) as f:
        soup = BeautifulSoup(f, "html.parser")
        
        product_box = soup.find("ul", class_="srp-results srp-list clearfix")
        
        # Each individual product exists in the list item <li> tag.
        product_list = product_box.find_all("li")
        
        # Getting the item per page countsx
        item_per_page = soup.find("div", class_ = "srp-ipp")
        item_per_page = item_per_page.find("span", class_ = "btn__cell")
        
    for elem in product_list:
        try:
            # Extract the info section of each search result
            product = elem.find("div", class_="s-item__info clearfix")
            
            # Extracting the title of the product from the div
            title = product.find("div", class_="s-item__title")
            
            # Price
            price = product.find("span", class_="s-item__price")
            
            # Shipping price
            shippingprice = product.find("span", class_="s-item__shipping s-item__logisticsCost")
            
            # Printing this information
            print(f"Title: {title.text}")
            print(f"Price: {price.text}")
            print(f"Shipping Price: {shippingprice.text}")
            print(f"")
            
        except Exception as ex:
            # Creating a try catch rule to get rid of irrelevant list items in t
            # item begins
            pass
    print(f"Number of items in this page: {item_per_page.text}")
    print(f"")


# In[77]:


# using RegEx, identify and print to screen gift cards that sold above face value. 
# ex. use RegEx to extract the value of a gift card from its title when possible 
# (doesn’t need to work on all titles, > 90% success rate if sufficient). 
# Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  
# If value < price + shipping, then a gift card sells above face value.
#product_list
#product = elem.find("div", class_="s-item__info clearfix")


#dollars = re.findall('\$\d+(?:\.\d+)?', product_list)
#dollars


# In[ ]:


# What fraction of Amazon gift cards sells above face value? Why do you think this is the case?


# ### Coding 2.2 

# In[12]:


import requests
import time
from bs4 import BeautifulSoup


# In[83]:


username = "kmunjal"
password = " "


# In[80]:


# Following the steps we discussed in class and write code that automatically logs into the website fctables.com

url = "https://www.fctables.com/user/login/"
my_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
session = requests.session()
page = requests.get(URL, headers = my_header)


# In[93]:


# Reading entire page and creating a BeautifulSoup object
soup = BeautifulSoup(page.content, "html.parser")


# In[81]:


# Accessing the cookies
cookies = page.cookies.get_dict()
cookies


# In[92]:


user_details = {"username": username,
                "password": password}

data = {**user_details}

# Making the post request
res = session.post(url, 
                   data = data, 
                   headers = my_header,
                   cookies = cookies,
                   timeout = 15)

data


# In[89]:


# Verify that you have successfully logged in:  use the cookies you received during log in 
# and write code to access https://www.fctables.com/tipster/my_bets/ 
#Check whether the word “Wolfsburg” appears on the page.  
# Don’t look for your username to confirm that you are logged in (it won’t work) 
# and use this page’s content instead.

URL = "https://www.fctables.com/tipster/my_bets/"
my_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
page = requests.get(URL, headers = my_header)
page


# In[91]:


# Reading entire page and creating a BeautifulSoup object
soup = BeautifulSoup(page.content, "html.parser")
soup


# In[ ]:




