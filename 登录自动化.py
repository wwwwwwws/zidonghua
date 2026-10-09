from playwright.sync_api import sync_playwright
import ddddocr
import time

# 测试账号
test_users = [
    {"username": "111", "password": "222", "captcha": None},          # 账号错误、密码错误，自动识别验证码
    {"username": "admin", "password": "111", "captcha": None},        # 正确账号、错误密码，自动识别验证码
    {"username": "admin", "password": "  ", "captcha": None},        # 账号正确，密码全部空格，自动识别验证码
    {"username": "  ", "password": "weilaikeji666", "captcha": None},# 账号全部空格，正确密码，自动识别验证码
    {"username": "  ", "password": "  ", "captcha": None},           # 账号空格、密码空格，自动识别验证码
    {"username": "", "password": "weilaikeji666", "captcha": None},  # 用户名为空，密码正确，自动识别验证码
    {"username": "admin", "password": "", "captcha": None},            # 账号正确，密码为空，自动识别验证码
    {"username": "", "password": "", "captcha": None},               # 账号空、密码空，自动识别验证码
    {"username": "admin", "password": "weilaikeji666", "captcha": None},#账号密码全部正确，自动识别验证码
    {"username": "admin", "password": "weilaikeji666", "captcha": ""},#账号密码正确，验证码为空字符串
    {"username": "admin", "password": "weilaikeji666", "captcha": "aaaa"},#账号密码正确，输入错误4位验证码
    {"username": "admin", "password": "weilaikeji666", "captcha": "  "},  #账号密码正确，验证码只输入空格
    {"username": "", "password": "", "captcha": ""},                     #账号空、密码空、验证码为空
    {"username": "  ", "password": "  ", "captcha": "  "},               #账号空格、密码空格、验证码空格
    {"username": "admin", "password": "weilaikeji666", "captcha": "123"}, #账号密码正确，验证码3位（不足4位）
    {"username": "admin", "password": "weilaikeji666", "captcha": "12345"},#账号密码正确，验证码5位（超过4位）
    {"username": "", "password": "", "captcha": "9999"},                 #账号空、密码空，填写错误验证码
    {"username": "  ", "password": "weilaikeji666", "captcha": "test"},   #账号空格，密码正确，错误验证码
    {"username": " admin ", "password": "weilaikeji666", "captcha": None} #账号前后带空格，密码正确，自动识别验证码
]


ocr = ddddocr.DdddOcr(show_ad=False)
login_url = "http://manager-v2-uat.baoanlailou.com/login"


def get_captcha(page, max_retry=3):
    """获取验证码，识别错误自动刷新重试"""
    captcha_loc = page.locator(".sendCode img")
    for retry in range(max_retry):
        # 截图
        img_bytes = captcha_loc.screenshot()
        code = ocr.classification(img_bytes).strip()
        print(f"第{retry+1}次识别结果：{code}")
        # 判断必须4位字符
        if len(code) == 4:
            return code
        # 识别失败，点击验证码刷新
        captcha_loc.click()
        time.sleep(0.8)
    print("⚠️验证码多次识别失败，放弃本次登录")
    return None


def run_login(page, user_info):
    username = user_info["username"]
    password = user_info["password"]
    input_captcha = user_info["captcha"]

    print(f"\n======== 当前账号：{username} | 指定验证码：{input_captcha} ========")
    page.goto(login_url)
    page.wait_for_timeout(1500)

    # 输入账号
    page.locator('input[placeholder="请输入账号"]').fill(username)
    time.sleep(0.5)
    # 输入密码
    page.locator('input[placeholder="请输入密码"]').fill(password)
    time.sleep(0.5)

    # 判断是否手动指定验证码
    if input_captcha is None:
        captcha_code = get_captcha(page)
        if captcha_code is None:
            return
    else:
        captcha_code = input_captcha

    page.locator('input[placeholder="请输入验证码"]').fill(captcha_code)
    time.sleep(0.8)

    # 点击登录
    page.locator(".btn").click()
    page.wait_for_timeout(2500)
    print(f"【{username}】登录操作执行完毕")
    time.sleep(2)


if __name__ == '__main__':
    with sync_playwright() as p:
        # Jenkins运行请改为 headless=True
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        for user in test_users:
            run_login(page, user)

        browser.close()
        print("\n✅所有账号测试流程执行结束")