from selenium.webdriver.common.by import By


class LoginPageElements:
    # 页面地址
    url = "https://passport.ctrip.com/user/login"

    # 页面元素
    loginname = (By.ID, "nloginname")
    pwd = (By.ID, "npwd")
    err = (By.ID, "nerr")
    submit = (By.ID, "nsubmit")
