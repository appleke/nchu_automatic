# 中興大學自動選課程式
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
from transformers import VisionEncoderDecoderModel, TrOCRProcessor
import torch

# 輸入要加選的課程代碼
c1 = '123'
c2 = '456'
c3 = '789'
c4 = '1253'
c5 = '21'
c6 = '51'
c7 = '13'
c8 = '1321'
c9 = '2213'
c10 = '135153'
values = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]

# 設定網址與帳密
url = "https://idp.nchu.edu.tw/nidp/idff/sso?id=12&sid=4&option=credential&sid=4&target=https%3A%2F%2Fportal.nchu.edu.tw%2Fportal"
username = ''
password = ''
course_url = "https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_nomo1_list"
course_url2 ='https://onepiece2-sso.nchu.edu.tw/cofsys/plsql/enro_direct1_list'

# 初始化瀏覽器
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 設置瀏覽器分離
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)#打開登入網頁
driver.maximize_window()#視窗最大化

# 模擬登入
driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[2]/div/input').send_keys(username)
driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[4]/div/input').send_keys(password)

# 輸入驗證碼
# 使用驗證碼識別模型"anuashok/ocr-captcha-v3"
processor = TrOCRProcessor.from_pretrained("anuashok/ocr-captcha-v3")
model = VisionEncoderDecoderModel.from_pretrained("anuashok/ocr-captcha-v3")
captcha_element = driver.find_element(By.XPATH, "//*[@id='stylized']/form/div/div[5]/div/div")
captcha_element.screenshot("captcha.png")
image =Image.open('captcha.png').convert("RGBA")

# Create white background
background = Image.new("RGBA", image.size, (255, 255, 255))
combined = Image.alpha_composite(background, image).convert("RGB")

# Prepare image
pixel_values = processor(combined, return_tensors="pt").pixel_values

# Generate text
generated_ids = model.generate(pixel_values)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0] 


driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[7]/div/input').send_keys(generated_text)
driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/div[1]/div/div/form/div/div[8]/div[1]/button").click() #登入

# 4進入選課系統
driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[1]/div[2]/div/a[4]").click() #先進入選課系統
time.sleep(3) # 等待網頁加載完成
driver.get(course_url2)
driver.switch_to.window(driver.window_handles[0]) # 跳回選課視窗

for i, value in enumerate(values): # 各欄輸入框擁有規律的XPATH，用迴圈簡化之
    row = (i // 2) + 2  
    col = 2 if i % 2 == 0 else 4
    xpath = f'/html/body/form/table[1]/tbody/tr[{row}]/td[{col}]/input'
    driver.find_element(By.XPATH, xpath).send_keys(value)

# 重複按下確認
for i in range(2):
   driver.find_element(By.XPATH, "/html/body/form/table[2]/tbody/tr/td[1]/input").click()


