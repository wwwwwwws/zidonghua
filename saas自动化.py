from playwright.sync_api import sync_playwright
import ddddocr
import time

short_url = "https://link.wtturl.cn/?target=https%3A%2F%2Fmanager-saas-uat.baoanlailou.com%2Flogin%3Fredirect%3D%252Findex&scene=im&aid=497858&lang=zh"
target_username = "ptzh001"
target_password = "admin123"

ocr = ddddocr.DdddOcr(show_ad=False)


def get_captcha(page, max_retry=3):
    captcha_loc = page.locator(".sendCode img")
    captcha_loc.wait_for(timeout=15000)
    for retry in range(max_retry):
        try:
            img_bytes = captcha_loc.screenshot(timeout=5000)
            code = ocr.classification(img_bytes).strip()
            print(f"第{retry+1}次识别验证码结果：{code}")
            if len(code) == 4:
                return code
            captcha_loc.click(timeout=5000)
            time.sleep(0.8)
        except Exception as e:
            print(f"验证码识别异常：{str(e)}")
            time.sleep(1)
    print("⚠️验证码多次识别失败，放弃本次登录")
    return None


def run_login(page):
    username = target_username
    password = target_password
    print(f"\n======== 当前账号：{username} ========")
    try:
        page.goto(short_url, timeout=30000)

        user_input = page.locator('input[placeholder="请输入账号"]')
        pwd_input = page.locator('input[placeholder="请输入密码"]')
        captcha_input = page.locator('input[placeholder="请输入验证码"]')
        login_btn = page.locator(".btn")

        user_input.wait_for(timeout=20000)
        print("✅账号输入框已找到，开始填写账号")
        user_input.clear()
        user_input.type(username, delay=50)
        time.sleep(0.3)

        pwd_input.wait_for(timeout=10000)
        print("✅密码输入框已找到，开始填写密码")
        pwd_input.clear()
        pwd_input.type(password, delay=50)
        time.sleep(0.3)

        captcha_code = get_captcha(page)
        if captcha_code is None:
            print(f"【{username}】验证码获取失败，停止本次登录")
            return

        captcha_input.wait_for(timeout=10000)
        print(f"✅填入验证码:{captcha_code}")
        captcha_input.clear()
        captcha_input.type(captcha_code, delay=50)
        time.sleep(0.8)

        login_btn.wait_for(timeout=10000)
        print("✅点击登录按钮")
        login_btn.click(timeout=8000)
        page.wait_for_timeout(3000)
        print(f"✅【{username}】登录操作执行完毕")

    except Exception as err:
        print(f"❌【{username}】执行出错：{str(err)}")


if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        run_login(page)

        input("\n登录流程结束，按回车关闭浏览器 >>>")
        browser.close()
        print("\n✅脚本执行完成")
