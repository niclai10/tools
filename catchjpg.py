from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 初始化浏览器（需提前下载对应浏览器驱动，如 chromedriver）
driver = webdriver.Chrome()
url = 'https://book.yunzhan365.com/dsovw/slpi/mobile/index.html'
driver.get(url)
time.sleep(5)  # 等待页面初步加载

page_num = 1
while True:
    # 保存当前页截图
    driver.save_screenshot(f'科顺手册_第{page_num}页.png')
    
    try:
        # 定位翻页按钮（需根据网页实际结构调试选择器）
        # 示例：通过检查云展网网页元素，找到真实翻页按钮定位方式
        next_btn_selector = '翻页按钮对应的 CSS 选择器或 XPath'
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, next_btn_selector))
        )
        next_btn.click()
        page_num += 1
        time.sleep(2)  # 等待翻页动画完成
    except:
        print("翻页结束或按钮定位失败")
        break

driver.quit()
