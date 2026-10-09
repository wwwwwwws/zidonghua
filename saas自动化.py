from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ddddocr
import base64
import time

# 初始化OCR
ocr = ddddocr.DdddOcr(show_ad=False)

# ==========Chrome中文配置==========
options = webdriver.ChromeOptions()
options.add_argument("--lang=zh-CN")
options.add_experimental_option('prefs', {'intl.accept_languages': 'zh-CN,zh'})
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# 浏览器启动
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://manager-saas-uat.baoanlailou.com/login?redirect=%2Findex")
wait = WebDriverWait(driver, 15)
driver.implicitly_wait(2)
time.sleep(1.5)

# ====================== 1.账号输入框 ======================
user_xpath = '//input[normalize-space(@placeholder)="请输入账号" and contains(@class,"el-input__inner")]'
user_elem = wait.until(EC.element_to_be_clickable((By.XPATH, user_xpath)))
driver.execute_script("arguments[0].removeAttribute('readonly');arguments[0].focus();", user_elem)
user_elem.clear()
user_elem.send_keys("ptzh001")
print("✅账号ptzh001输入完成")

# ====================== 2.密码输入框 ======================
pwd_xpath = '//input[normalize-space(@placeholder)="请输入密码" and contains(@class,"el-input__inner")]'
pwd_elem = wait.until(EC.element_to_be_clickable((By.XPATH, pwd_xpath)))
driver.execute_script("arguments[0].removeAttribute('readonly');arguments[0].focus();", pwd_elem)
pwd_elem.clear()
pwd_elem.send_keys("admin123")
print("✅密码admin123输入完成")

# ====================== 3.验证码图片（匹配你截图的img标签） ======================
captcha_img_xpath = '//img[contains(@style,"width: 103px") and contains(@style,"height: 34px")]'
captcha_img = wait.until(EC.presence_of_element_located((By.XPATH, captcha_img_xpath)))
# 点击图片刷新验证码，拿到最新base64
captcha_img.click()
time.sleep(1)

# 获取base64图片
src_data = captcha_img.get_attribute("src")
base64_str = src_data.replace("data:image/png;base64,", "")
img_bytes = base64.b64decode(base64_str)
captcha_code = ocr.classification(img_bytes).strip()
print(f"✅识别验证码：{captcha_code}")

# ======================4.验证码输入框 ======================
code_xpath = '//input[@name="code" and contains(@class,"el-input__inner")]'
code_elem = wait.until(EC.element_to_be_clickable((By.XPATH, code_xpath)))
driver.execute_script("arguments[0].removeAttribute('readonly');arguments[0].focus();", code_elem)
code_elem.clear()
code_elem.send_keys(captcha_code)
print("✅验证码输入完成")

# ======================5.登录按钮 ======================
login_btn_xpath = '//button[contains(@class,"el-button--primary")]'
login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, login_btn_xpath)))
login_btn.click()
print("✅自动点击登录按钮")

# 等待登录跳转，断言首页
try:
    wait.until(EC.url_contains("/index"))
    print("🎉登录成功！")
except Exception as e:
    print(f"⚠️登录跳转等待异常：{e}")

time.sleep(5)
# driver.quit()
