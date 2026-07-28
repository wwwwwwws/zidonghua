from playwright.sync_api import sync_playwright
import time

# 内置登录页面HTML，不需要外部login.html
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>登录页面</title>
    <style>
        .box{width:320px;margin:100px auto;}
        .item{margin:12px 0;}
        input{width:100%;padding:8px;box-sizing:border-box;font-size:16px;}
        button{width:100%;padding:10px;background:#2266dd;color:#fff;border:none;font-size:16px;cursor:pointer;}
    </style>
</head>
<body>
<div class="box">
    <h2>系统登录</h2>
    <div class="item">
        <input id="username" placeholder="用户名">
    </div>
    <div class="item">
        <input id="password" placeholder="密码" type="password">
    </div>
    <div class="item">
        <button onclick="login()">登录</button>
    </div>
</div>

<script>
function login(){
    const name = document.getElementById('username').value;
    const pwd = document.getElementById('password').value;
    if(name === "111" && pwd === "222"){
        alert("登录成功");
    }else{
        alert("登录失败");
    }
}
</script>
</body>
</html>
"""

# ----------------测试数据 5组----------------
test_data = [
    ("111", "222"),    # 正确
    ("111", "333"),    # 密码错误
    ("222", "222"),    # 用户名错误
    ("", ""),          # 空账号密码
    ("111", "")        # 密码为空
]

def run_login_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_content(HTML_CONTENT)

        for index, (user, pwd) in enumerate(test_data, 1):
            print(f"\n===== 执行第{index}组测试：用户名={user}，密码={pwd} =====")
            # 填入账号密码
            page.locator("#username").fill(user)
            page.locator("#password").fill(pwd)

            dialog_msg = ""
            # 捕获弹窗
            def handle_dialog(dialog):
                nonlocal dialog_msg
                dialog_msg = dialog.message
                print(f"弹窗信息：{dialog_msg}")
                # 弹窗停留2秒再关闭
                time.sleep(2)
                dialog.accept()

            page.once("dialog", handle_dialog)
            page.locator("button").click()
            # 留出足够时间等待弹窗处理完毕
            page.wait_for_timeout(2500)

        print("\n✅ 全部5组用例执行完毕，自动关闭浏览器")
        browser.close()

if __name__ == "__main__":
    run_login_test()
