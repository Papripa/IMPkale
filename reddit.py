from pynput.keyboard import Listener, Key
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ 初始化 chromedriver 路径
service = Service("/usr/local/bin/chromedriver")  # 请替换为正确的 chromedriver 路径

# Function to read the website.txt file
def read_links():
    with open('website.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Function to update the website.txt file
def update_links(links):
    with open('website.txt', 'w') as f:
        for link in links:
            f.write(f"{link}\n")

# Initialize WebDriver function
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("about:blank")
    return driver

# 加载链接
reddit_links = read_links()

print("✅ 读取完成，共 {} 个链接".format(len(reddit_links)))
print("按shift键查看下一个 Reddit 链接，按 q 退出。")

# Initialize the browser
driver = init_driver()

index = 0

# Prepare to store the results in a list
results = []
is_waiting_for_input = False
current_input = ""

# Define key press event handler
def on_press(key):
    global index
    global is_waiting_for_input
    global current_input
    try:
        if key == Key.shift:  # When Tab key is pressed
            if index < len(reddit_links):
                print(f"shift 键按下了！打开第 {index + 1} 个链接：{reddit_links[index]}")
                
                # Open a new tab and navigate to the Reddit link
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
                driver.get(reddit_links[index])  # Open the Reddit link

                # Try to click the "View Post" button if it exists
                try:
                    view_post = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="view-post-button"]'))
                    )
                    view_post.click()
                    print("✅ 已自动点击 View Post 链接")
                except Exception as e:
                    print(f"⚠️ 没有找到 View Post 按钮，可能已经是图片页: {e}")

                # Remove the visited link from the list
                reddit_links.pop(0)  # Remove the first link in the list
                update_links(reddit_links)  # Update website.txt

                # Close the previous tab only if it's still open
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[-2])  # Switch to the previous tab
                    driver.close()  # Close the previous tab

                # Switch to the new tab after closing the old one
                driver.switch_to.window(driver.window_handles[-1])

                # Move to the next link
                index += 1

                # If there are no more links, print a message
                if len(reddit_links) == 0:
                    print("🎉 所有链接已访问完成！")
            else:
                print("🎉 所有链接已访问完成！")

        elif key == Key.esc:  # Exit the program when 'esc' is pressed
            print("👋 已退出")
            driver.quit()  # Close the browser
            # Save results to a CSV file before quitting
            with open('output.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Output"])  # Write the header for the CSV
                for result in results:
                    writer.writerow([result])  # Write each result in a new row
            print("✅ 输出已保存到 'output.csv'")

            # Update website.txt only when exiting
            update_links(reddit_links)  # Save remaining links to the file
            print("✅ 已更新 'website.txt'，移除了已访问的链接")

            listener.stop()  # Stop the listener to exit the program

    except AttributeError:
        print(f"Special key {key} pressed")

# Start the listener in a blocking fashion (removing threading for simplicity)
listener = Listener(on_press=on_press)
listener.start()

# Wait for the listener to stop
listener.join()
