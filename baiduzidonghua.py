from playwright.sync_api import sync_playwright

def baidu_search(browser, keyword):
    # 每次搜索独立创建上下文，隔离缓存、弹窗、会话
    context = browser.new_context()
    page = context.new_page()
    try:
        page.goto("https://www.baidu.com", timeout=15000)
        input_loc = page.locator('input[name="wd"]')
        input_loc.wait_for(state="visible", timeout=8000)
        input_loc.fill(keyword)
        # 回车提交搜索
        input_loc.press("Enter")
        page.wait_for_timeout(2000)
        print(f"【{keyword}】搜索执行完毕")
    except Exception as e:
        print(f"【{keyword}】执行异常：{str(e)}")
    finally:
        page.close()
        context.close()

if __name__ == "__main__":
    search_words = ["中国", "美食", "音乐", "电影"]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        for word in search_words:
            print(f"开始搜索：{word}")
            baidu_search(browser, word)
        browser.close()
