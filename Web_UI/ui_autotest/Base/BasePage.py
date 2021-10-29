# 封装页面公用的元素定位、操作方法
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def verify(self, type, value):
        """
        验证测试结果
        :param type: 验证方式。title, element, text, url
        :param value: 验证文本
        :return:
        """
        self.wait = WebDriverWait(self.driver, 5)

        if type == "title":
            time.sleep(2)
            assert value in self.driver.title, self.driver.title
        if type == "element":
            try:
                self.wait.until(EC.presence_of_element_located(getattr(self, value)))
            except TimeoutException:
                assert False, str(TimeoutException)
            except AttributeError:
                assert False, f"PageObject中没有名为 {value} 的元素，请检查对应的Elements类"

    def get(self, url):
        """
        打开指定url网页
        :param url:
        :return:
        """
        self.driver.get(url)

    def find_element(self, location):
        """
        元素定位
        :param location: (locate type, value)
        :return: element
        """
        return self.driver.find_element(*location)

    def send_keys(self, location, key):
        """
        给定一个位置，向该位置元素输入一个值
        :param location: (locate type, value)
        :param key: str
        :return: none
        """
        self.find_element(location).send_keys(key)

    def click(self, location):
        """
        给定一个位置，点击该位置的元素
        :param location:
        :return:
        """
        self.find_element(location).click()
