from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

url = "https://dailydictation.com/exercises/short-stories/1-first-snowfall.1/listen-and-type"
driver.get(url)
time.sleep(3)

# Mở transcript (nếu có nút)
try:
    show_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Full Audio & Plain Transcript')]")
    show_btn.click()
    time.sleep(1)
except:
    pass

print("---- TRANSCRIPT ----")

# Lấy tất cả div transcript theo mẫu HTML bạn gửi
transcript_items = driver.find_elements(By.XPATH, "//div[@title[contains(., 'Challenge #')]]")

for item in transcript_items:
    print(item.text)

print("\n---- AUDIO URL ----")

# Lấy thẻ <source> thật (nằm ngoài thẻ <audio>)
source_elements = driver.find_elements(By.XPATH, "//source[@type='audio/mpeg']")

if source_elements:
    audio_src = source_elements[0].get_attribute("src")
    print("✔ REAL AUDIO URL:", audio_src)
else:
    print("✖ Không tìm thấy source audio trong DOM.")

driver.quit()