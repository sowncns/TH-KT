from  selenium import  webdriver

from  selenium.webdriver.common.by import By


driver =webdriver.Chrome()
driver.get("https://tiki.vn/dien-thoai-may-tinh-bang/c1789")
driver.execute_script("window.scrollTo(0,300)")
driver.implicitly_wait(2)
main_window = driver.current_window_handle
index =1
pages =[]
products = driver.find_elements(By.CSS_SELECTOR,'a.product-item')
for p in products[:2]:
      href = p.get_attribute('href')
      title = p.find_element(By.CSS_SELECTOR, '.info h3')

      print(f"Sản phẩm {index}: {title.text}")
      print(f"Link: {href}")
      print("-" * 20)
      index = index + 1
      pages.append(href)

for idx,p in enumerate(pages):
  driver.get(p)
  driver.save_screenshot(f'img{idx}.png')
  driver.execute_script("window.scrollTo(0,2200)")
  driver.implicitly_wait(1)
  comments = driver.find_elements(By.CLASS_NAME, 'review-comment')

  for c in comments[:5]:
      user = c.find_element(By.CLASS_NAME, 'review-comment__user-name')
      tiltle_cmt = c.find_element(By.CLASS_NAME, 'review-comment__content')
      print(f'{user.text} da comment : {tiltle_cmt.text} ')

driver.quit()
