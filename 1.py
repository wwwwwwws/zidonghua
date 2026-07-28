from playwright.sync_api import sync_playwright
import time

def run_test():
    with sync_playwright() as p:
        # Jenkins SYSTEM账户必须无头模式，看不见浏览器窗口
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 访问百度
        page.goto("https://www.baidu.com")
        print(f"当前页面标题：{page.title()}")

        # 搜索测试
        page.fill("#kw", "自动化测试")
        page.click("#su")
        time.sleep(2)

        print("测试执行完成！")
        browser.close()

if __name__ == "__main__":
    run_test()
