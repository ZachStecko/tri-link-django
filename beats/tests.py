from django.test import TestCase

# Create your tests here.
import unittest
from selenium import webdriver
import os
import time

#select browser
browser = webdriver.Firefox()
browser.get('http://localhost:8000/accounts/login/')

#user login
username = browser.find_element_by_name("username")
password = browser.find_element_by_name("password")

username.send_keys("user")
password.send_keys("password")
browser.find_element_by_name("submit").click()

#home
browser.find_element_by_name("create").click()

for x in range(10):
    #software
    stroke = browser.find_element_by_name("strokeColour")
    stroke.send_keys('255,255,255')

    fill = browser.find_element_by_name("fillColour")
    fill.send_keys('255,255,255')

    browser.find_element_by_id("id_imgfile").send_keys(os.getcwd()+"\static\sunset.jpg")
    browser.find_element_by_id("id_docfile").send_keys(os.getcwd()+"\\static\\au.mp3")

    browser.find_element_by_id("submitBtn").click()

    time.sleep(50)
    browser.find_element_by_name("createAgain").click()