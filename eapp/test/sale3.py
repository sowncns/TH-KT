from  selenium import  webdriver
from selenium.webdriver.common.keys import Keys

from  selenium.webdriver.common.by import By

driver =webdriver.Chrome()

driver.get("https://thuvien.ou.edu.vn")
original_window = driver.current_window_handle

search = driver.find_element(By.ID,'txtSearch')
search.send_keys("kiem thu")
search.send_keys(Keys.ENTER)
driver.implicitly_wait(3)
iframe =[]
list = driver.find_elements(By.CLASS_NAME,'li-list')
for idx,ip in enumerate(list):
    link  = ip.find_element(By.CLASS_NAME,'name-book')
    driver.execute_script("arguments[0].click();", link)
    driver.implicitly_wait(2)
    modal = driver.find_element(By.CSS_SELECTOR,'.modal-body iframe')
    iframe.append(modal.get_attribute('src'))

for ifr in iframe:
    driver.get(ifr)
    r = driver.find_element(By.XPATH,'/html/body/form/div[4]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[2]')
    if r.text.index('IBSC'):
        print(r.text)

        # 4. QUAN TRỌNG: Đóng Modal để có thể click cuốn sách tiếp theo
        # Tìm nút X hoặc nút Close trên Modal
    close_btn = driver.find_element(By.CSS_SELECTOR, "#bookDetailModal button[data-bs-dismiss='modal']")
    driver.execute_script("arguments[0].click();", close_btn)

driver.quit()