import requests
import pytest
import ddddocr
import base64

BASE_URL = "https://manager-saas-uat.baoanlailou.com"
ocr = ddddocr.DdddOcr(show_ad=False)


def get_captcha() -> tuple[str, str]:
    """调用getCode接口，获取uuid（等同于codekey）和base64图片，识别验证码"""
    captcha_url = f"{BASE_URL}/api/admin/auth/getCode"
    resp = requests.get(captcha_url)
    res_json = resp.json()
    print("\n==== getCode接口完整返回 ====")
    print(res_json)

    # 真实字段：data下 uuid 和 imageBase
    uuid = res_json["data"]["uuid"]
    img_base64_str = res_json["data"]["imageBase"]

    # 去掉base64前缀 data:image/png;base64,
    if img_base64_str.startswith("data:image/png;base64,"):
        img_base64_str = img_base64_str.replace("data:image/png;base64,", "")
    img_bytes = base64.b64decode(img_base64_str)
    # ddddocr识别验证码
    code = ocr.classification(img_bytes)
    print(f"识别出验证码：{code}, uuid(codekey):{uuid}")
    return code, uuid


def login_api(username: str, password: str):
    code, codekey = get_captcha()
    url = f"{BASE_URL}/api/admin/auth/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "password": password,
        "code": code,
        "codekey": codekey
    }
    resp = requests.post(url=url, json=payload, headers=headers)
    return resp


# ========== 参数化测试用例 ==========
@pytest.mark.parametrize("username, password, expect_success", [
    ("ptzh001", "admin123", True),    # 正确账号密码
    ("ptzh001", "wrongpass", False),  # 正确账号，错误密码
    ("wronguser", "admin123", False), # 错误账号，正确密码
    ("", "admin123", False),          # 用户名为空
    ("ptzh001", "", False),           # 密码为空
])
def test_login_param(username, password, expect_success):
    resp = login_api(username, password)
    assert resp.status_code == 200
    res = resp.json()
    print(f"\n【登录接口返回】{res}")

    if expect_success:
        assert res["success"] is True
        assert res["code"] == 200
        assert res["msg"] == "操作成功"
        token = res["data"]["token"]
        assert token
        print(f"\n✅登录成功，token: {token}")
    else:
        assert res["success"] is False


if __name__ == "__main__":
    response = login_api("ptzh001", "admin123")
    result = response.json()
    print("登录返回：")
    print(result)
