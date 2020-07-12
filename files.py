#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
import pickle


# In[2]:


# Chrome Set Up
download_directory = "/home/mars/Desktop/programming/python/fb_group_files_extraction/downloaded_files"
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(options=chrome_options)
sleep(2)
driver.maximize_window()


# In[3]:


# Constants
fb_url = "https://www.facebook.com"
# Credentials
creds = open('creds/fb_creds.txt').readlines()
fb_id = creds[0].strip()
fb_pass = creds[1].strip()
# Groups
groups = []
lines = open('group_ids.txt').readlines()
for line in lines:
    key_value = line.strip().split(':')
    group = {
        'Name': key_value[0].strip(),
        'ID': key_value[1].strip()
    }
    groups.append(group)


# In[4]:


def fb_login(driver, login_id, password, cookies_file):
    email_el = driver.find_element_by_name('email')
    password_el = driver.find_element_by_name('pass')
    email_el.clear()
    email_el.send_keys(login_id)
    sleep(2)
    password_el.clear()
    password_el.send_keys(password)
    sleep(2)
    login_btn = driver.find_element_by_xpath('//input[@aria-label="Log In"]')
    login_btn.click()
    sleep(3)
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    pickle.dump(driver.get_cookies(), open(cookies_file, 'wb'))
    sleep(2)


def load_cookies(driver, location, url=None):
    cookies = pickle.load(open(location, 'rb'))
    driver.delete_all_cookies()
    url = "https://www.google.com" if url is None else url
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)


# def search_in_fb(driver, keywords):
#     search_box = driver.find_element_by_name('q')
#     search_box.clear()
#     search_box.send_keys(keywords)
#     search_btn = driver.find_element_by_xpath('//button[@aria-label="Search"]')
#     search_btn.click()
#     sleep(2)
#     first_search_el = driver.find_element_by_xpath('//div[@class="_6v_0 _4ik4 _4ik5"]/a')
#     first_search_el.click()
#     sleep(2)


def grab_group_files(driver, group_id):
    driver.get(f'https://www.facebook.com/groups/{group_id}/files/')
    sleep(2)
    files_ul = driver.find_element_by_xpath('//ul[@class="uiList _4kg _4ks"]')
    files_li = driver.find_elements_by_class_name('_pu_')
    all_files = []
    for file_li in files_li:
        upload_time = file_li.find_element_by_class_name('timestampContent').text
        download_link = file_li.find_element_by_tag_name('a').get_attribute('href')
        file_type = file_li.find_element_by_xpath('//span[@class="_50f8"]').text.strip().lower()
        if file_type != 'document':
            fl = {
                'Download Link': download_link,
                'Upload Time': upload_time
            }
            all_files.append(fl)
    return all_files
    


# In[5]:


try:
    load_cookies(driver, 'cookies/mars_fb_cookies.txt')
    sleep(2)
    driver.get(fb_url)
    sleep(2)
except:
    fb_login(driver, fb_id, fb_pass, 'cookies/mars_fb_cookies.txt')


# In[6]:


grabbed_files = []
for group in groups:
    fls = grab_group_files(driver, group['ID'])
    dct = {
        'Group Name': group['Name'],
        'Files': fls
    }
    grabbed_files.append(dct)


# In[7]:


for group in grabbed_files:
    g_files = group['Files']
    for file in g_files:
        d_link = file['Download Link']
        driver.get(d_link)
        sleep(random.randrange(2,5))


# In[8]:


closing_command = ''
while closing_command.lower() != 'exit':
    closing_command = input("Type exit when downloads successfully done: ")
    if closing_command.lower() == 'exit':
        driver.close()

