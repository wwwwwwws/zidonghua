from playwright.sync_api import sync_playwright

def baidu_search(browser, keyword):
    page = browser.new_page()
    page.goto("https://www.baidu.com")
    page.wait_for_timeout(2000)
    input_loc = page.locator('input[name="wd"]')
    input_loc.click(force=True)
    input_loc.fill(keyword)
    page.locator('input[id="su"]').click(force=True)
    page.wait_for_timeout(3000)
    page.close()

if __name__ == "__main__":
    search_words = ["中国", "美食", "音乐", "电影"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        for word in search_words:
            print(f"开始搜索：{word}")
            baidu_search(browser, word)
        browser.close()
