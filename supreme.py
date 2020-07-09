from time import sleep
from config import keys
from selenium import webdriver
import time
import os
from threading import Thread
import math
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests 

#time the run
def timeme(method):
    def wrapper(*args, **kw):
        startTime= int(round(time.time()*1000))
        result = method (*args, **kw)
        endTime = int(round(time.time()*1000))
        print("Execution time: {}".format((endTime-startTime)/1000))
        return result
    return wrapper

@timeme
def order(k):

    driver.get(k['product_url'])

    colorz=k['product_color']
    colorIndex=1
    sizeIndex=1
    desiredSize=k['product_size']

    productName = driver.find_element_by_xpath('//*[@id="details"]/h1')
    print (productName.text)


    #find color
    productColor = driver.find_element_by_xpath('//*[@id="details"]/p[1]')
    print (productColor.text)

    while(productColor.text!=colorz):
        colorIndex=colorIndex+1
        driver.find_element_by_xpath('//*[@id="details"]/ul/li[{}]/a'.format(colorIndex)).click()
        productColor = driver.find_element_by_xpath('//*[@id="details"]/p[1]')
        print (productColor.text)

    time.sleep(0.1)

    #find size
    productSize = driver.find_element_by_xpath('//*[@id="size"]/option[1]')
    print (productSize.text)

    while(productSize.text!=desiredSize):  
        sizeIndex=sizeIndex+1  
        print (sizeIndex)
        productSize = driver.find_element_by_xpath('//*[@id="size"]/option[{}]'.format(sizeIndex))
        
        
    productSize = driver.find_element_by_xpath('//*[@id="size"]/option[{}]'.format(sizeIndex)).click()

    #navigate to checkout
    
    addToBag = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="add-remove-buttons"]/input')))
    addToBag.click()
    waitForCheckOutNow = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="cart"]/a[2]')))
    waitForCheckOutNow.click()

    #checkout form

    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(k["name"])
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(k["email"])
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(k["phone_number"])
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(k["address"])
    driver.find_element_by_xpath('//*[@id="oba3"]').send_keys(k["address2"])
    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(k["city"])
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(k["zip"])
    driver.find_element_by_xpath('//*[@id="order_billing_country"]/option[{}]'.format(k["country"])).click()
    driver.find_element_by_xpath('//*[@id="credit_card_type"]/option[{}]'.format(k["cardtype"])).click()
    driver.find_element_by_xpath('//*[@id="cnb"]').send_keys(k["cardnr"])
    driver.find_element_by_xpath('//*[@id="credit_card_month"]/option[{}]'.format(k["cardmo"])).click()
    driver.find_element_by_xpath('//*[@id="credit_card_year"]/option[{}]'.format(k["cardyear"])).click()
    driver.find_element_by_xpath('//*[@id="vval"]').send_keys(k["cardcvv"])
    driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()    
    #checkout delay
    #time.sleep(2)
    driver.find_element_by_xpath('//*[@id="pay"]/input').click()


    time.sleep(3)

    #captcha solver
 
    #PARAMS = {

    #    'key': 'e0468a8dbf5ca7851c3c897791cb8823',
    #    'method': 'userrecaptcha',
    #    'googlekey': '6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz',
    #    'pageurl': 'https://www.supremenewyork.com/checkout',
    #    'json': 1

    #}

    #r = requests.get(url = 'https://2captcha.com/in.php', params = PARAMS) 
    
    #data = r.json()
    #print (data)

    #ok1= data['status']
    #ok2= data['request']

    #print(ok1)
    #print (ok2)

    #time.sleep(30)

    #PARAMS2 = {

     #   'key': 'e0468a8dbf5ca7851c3c897791cb8823',
     #   'action': 'get',
     #   'id': ok2,
     #   'json': 1

    #}

    #r2 = requests.get(url = 'https://2captcha.com/res.php', params = PARAMS2) 

    #data2 = r2.json()

    #ok3 = data2['request']


    #print (data2)
    #print (ok3)


    #driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/textarea').send_keys(ok3)

    #driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/input[1]').click()


if __name__ == '__main__':
    #op = webdriver.ChromeOptions()
    #op.add_argument('headless')
    #driver = webdriver.Chrome(options=op)
    driver = webdriver.Chrome('./chromedriver')

    order(keys)
