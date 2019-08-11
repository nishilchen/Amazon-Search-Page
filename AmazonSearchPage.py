# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:09:01 2019

@author: Li Hsin Chen
"""

import requests
from lxml import etree
#import responses
import pandas as pd
from datetime import datetime as dt
from lxml import html
from time import sleep
#%%
class AmazonSearchPage():
    def __init__(self, url):
        self.user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        self.headers={"User-Agent":self.user_agent}
        self.url = url
        self.parse = self.get_product_page()    


    def get_product_page(self):
        page = requests.get(self.url, headers = self.headers, verify=False)
        page_response = page.text
        return html.fromstring(page_response)
    
    def get_product_info(self,item):
        sponsor = item.xpath('.//div[@class="sg-col-inner"]/div/div/span[@class="a-size-base a-color-secondary"]/text()')
        sponsor1 = str(".".join(sponsor).split('.')[0])

        if sponsor1 == 'Sponsored':
            type1 = 'Sponsored'
        else:
            type1 = 'Organic'
        
        raw_product = item.xpath('.//div/div/div/h2/a/span/text()')
        product_name = ''.join(raw_product).strip()

        raw_price = item.xpath('.//div/a/span[@class="a-price"]/span/text()')
        product_price = ''.join(raw_price).strip()
        
        try:            
            raw_rating = item.xpath('.//a/i/span[@class="a-icon-alt"]/text()')
            product_rating = float(''.join(raw_rating).strip().split(" ")[0])
        except:
            product_rating = None
            
            
        try:
            raw_total_review = item.xpath('.//span[@class="a-size-base"]/text()')
            total_review = int(raw_total_review[0])
        except:
            total_review = None
  
        return {"Product Name": product_name,
                "ASIN": item.values()[0],
                "position": int(item.values()[1]),
                "Price": product_price,
                "Rating": product_rating,
                "Total Reviews": total_review,
                "Type":type1}
        
        
    def get_product_list(self):
        XPATH_PRODUCT = '//div[@data-index]'
        raw_products = self.parse.xpath(XPATH_PRODUCT)
        
#        if not raw_products:
#            XPATH_PRODUCT = '//li[@data-result-rank]'
#            raw_products = self.parse.xpath(XPATH_PRODUCT)
        
        return raw_products
        
    
    def get_result(self):
        raw_products = self.get_product_list()
        result = []
        for item in raw_products:
            newData = self.get_product_info(item)
            result.append(newData)
        return result
    
    
    def get_brand_info(self):
        XPATH_BRAND_NAME = '//div/span[@id="hsaSponsoredByBrandName"]/text()'
        raw_brand_name = self.parse.xpath(XPATH_BRAND_NAME)
        brand_name = ''.join(raw_brand_name).strip()
        
        return {"Sponsored Brand": brand_name}

#%%
def get_url(keyword):
    url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='
    nkws = keyword.replace(" ","+")
    return url + nkws
#%%
url = "https://www.amazon.de/s?k=cashmere+sweater&__mk_de_DE=ÅMÅŽÕÑ&ref=nb_sb_noss_1"
page = AmazonSearchPage(url)
product_result_list = page.get_result()

pd.DataFrame(product_result_list)




