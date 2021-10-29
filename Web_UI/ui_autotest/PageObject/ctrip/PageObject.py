from Web_UI.ui_autotest.Base import BasePage
from Web_UI.ui_autotest.PageObject.ctrip.elements import *


class LoginPage(BasePage, LoginPageElements):
    """登录页面"""

    def __init__(self, driver):
        self.driver = driver

    # 业务操作
    def login(self, username, password):
        """登录操作"""
        self.get(self.url)
        self.send_keys(location=self.loginname, key=username)
        self.send_keys(location=self.pwd, key=password)
        self.click(location=self.submit)
