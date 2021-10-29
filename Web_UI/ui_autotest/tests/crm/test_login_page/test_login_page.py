from Web_UI.ui_autotest.PageObject.crm.PageObject import LoginPage


def test_login(driver, data):
    page = LoginPage(driver)
    page.login(data['email'], data['password'], data['code'])

    page.verify(*data['expect'])
