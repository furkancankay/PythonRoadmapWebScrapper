import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdfkit


class Scraper:
    """This is a docstring example."""
    BASE_URL = "https://roadmap.sh/python"
    LIST_CLICK = (By.CSS_SELECTOR, ".clickable-group")
    PHONE_CLICK = (By.XPATH, '//*[starts-with(@id,"datevUI_form_Select")]/div[2]/span[contains(text(), "In Buchungs-ABC")]')
    CLOSE_CLICK = (By.XPATH, '//*[@id="close-topic"]/img')

    def login(self):
        """_summary_"""
        driver = webdriver.Chrome()
        driver.get(Scraper.BASE_URL)
        driver.maximize_window()
        roadmaps_list = driver.find_elements(By.CSS_SELECTOR, "[data-group-id^='10'] > text")
        total_list=[]
        for i in roadmaps_list:
            link_list=[]
            i.click()
            time.sleep(2)
            if len(driver.find_elements(By.CSS_SELECTOR, "#main-content > ul > li > a"))> 0:
                pdf_link = driver.find_elements(By.CSS_SELECTOR, "#main-content > ul > li > a")
                for j in pdf_link:
                    time.sleep(1)
                    link_list.append([j.get_attribute("href"),j.text])
            else:
                pass
            driver.find_element(By.ID, 'close-topic').click()
            total_list.append([i.text, link_list])

        driver.quit()
        for category in total_list:
            for link_info in category[1]:
                link = link_info[0]
                print(link, ' loading...')
                convertwith = str.maketrans(':/|%&-','      ')
                temp = link_info[1]
                pdfname = temp.translate(convertwith)
                if not os.path.exists(pdfname+'.pdf'):
                    pdfkit.from_url(link, pdfname+'.pdf')
                    print(link, ' downloaded.')
                else:
                    print(pdfname,' is already exist.')

if __name__ == '__main__':
    START = Scraper()
    START.login()
