from Web_UI.ui_autotest.PageObject.ctrip.PageObject import LoginPage


def test_login(driver, data):
    page = LoginPage(driver)
    page.login(data['username'], data['password'])

    page.verify(*data['verification'])
