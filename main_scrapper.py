from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os
import requests
import lxml
import idnpass
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

login_id = idnpass.my_id
login_pass = idnpass.mypass

scrapping_profile_id = "mukit.h"
folder_name = scrapping_profile_id
os.makedirs(folder_name, exist_ok=True)
browser = webdriver.Firefox()

browser.get("https://instagram.com")
sleep(2)
id_elem = browser.find_element_by_css_selector(
    "div.-MzZI:nth-child(2) >" +
    " div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")

pass_elem = browser.find_element_by_css_selector(
    "div.-MzZI:nth-child(3) >" +
    " div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")


id_elem.send_keys(login_id)
pass_elem.send_keys(login_pass)

login_btn_elem = browser.find_element_by_css_selector("div.Igw0E:nth-child(4)")
login_btn_elem.click()
sleep(3)
browser.get("https://www.instagram.com/" + scrapping_profile_id + "/")
sleep(5)

# scroll the page
current_scroll_height = 1
prev_scroll_height = 0

retrieved_image = []
while current_scroll_height != prev_scroll_height:
    prev_scroll_height = current_scroll_height

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    current_scroll_height = browser.execute_script(
        "return document.body.scrollHeight")
    sleep(3)
    soup_profile = BeautifulSoup(browser.page_source, 'lxml')
    captured_images = soup_profile.select("img.FFVAD")

    for image in captured_images:
        if image not in retrieved_image:
            retrieved_image.append(image)
# sleep(5)
# get page source and turn into soup
# page_source_html = str(browser.page_source)
# soup_profile = BeautifulSoup(page_source_html, 'lxml')

# get all the images in page
# images are in class = "FFVAD"
# images = soup_profile.select("img.FFVAD")
failed_images = []

# download images
n = 0
for image in retrieved_image:
    try:
        img_url = image.get('src')
        print("downloading the image")
        image_res = requests.get(img_url)

        with open(os.path.join(folder_name, str(n) + ".jpg"), 'wb') as imgFile:
            for chunk in image_res.iter_content():
                imgFile.write(chunk)
        print("image saved")
    except:
        print("couldn't download the image")
        failed_images.append(img_url)
        logging.info(image_res.status_code)

    n += 1
print("Done!")
logging.info(len(failed_images))
logging.info(failed_images)
