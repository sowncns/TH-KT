from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from  selenium.webdriver.common.by import By



driver = webdriver.Chrome(service=service)
driver.get('https://vnexpress.net/')
article = driver.find_elements(By.CSS_SELECTOR,'#automation_TV0')
for a in article:
    title = a.find_element(By.TAG_NAME,"h3")
    des = a.find_element(By.CLASS_NAME,"description")
    img = a.find_elements(By.CSS_SELECTOR,"#dark_theme > section.section.section_topstory > div > div > div > article > div > a")
    print(title)
driver.quit()
