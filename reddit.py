import keyboard
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ 初始化 chromedriver 路径
service = Service(r"P:\OneDrive - kaist.ac.kr\IMPKALE\chromedriver.exe")

# 加载链接
with open('website.txt', 'r') as f:
    reddit_links = [line.strip() for line in f if line.strip()]

print("✅ 读取完成，共 {} 个链接".format(len(reddit_links)))
print("按空格查看下一个 Reddit 链接，按 q 退出。")

# 启动浏览器
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

# 打开初始空白页
driver.get("about:blank")
index = 0

while index < len(reddit_links):
    if keyboard.is_pressed(" "):
        url = reddit_links[index]
        print(f"\n🔗 打开第 {index+1} 个链接：{url}")

        # 打开新标签页
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        time.sleep(2)

        # 尝试点击“View Post”
        try:
            view_post = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="view-post-button"]'))
            )
            view_post.click()
            print("✅ 已自动点击 View Post 链接")
        except:
            print("⚠️ 没有找到 View Post 按钮，可能已经是图片页")

        # 关闭前一个标签页（如果不是第一个）
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-2])
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

        index += 1
        time.sleep(0.5)

    elif keyboard.is_pressed("q"):
        print("👋 已退出")
        break

if index == len(reddit_links):
    print("🎉 所有链接都done!")

driver.quit()
