import os

from locust import HttpUser, TaskSet, task
from faker import Faker
import requests


class Task(TaskSet):
    fake = Faker(locale='zh_CN')

    def get_count_info(self):
        """
        获取手机号及验证码
        :return: mobile,sms_code
        """
        mobile = self.fake.phone_number()

        # 当不希望API被Locust收集时，则用requests库发起请求即可
        url = 'http://121.4.47.229:8000/oauth/sendSmsCode/' + mobile
        res = requests.get(url=url)

        sms_code = res.json().get('code')

        nickname = self.fake.name()
        username = self.fake.user_name()

        return mobile, sms_code, nickname, username

    @task
    def logon(self):
        mobile, sms_code, nickname, username = self.get_count_info()
        data = {
            'mobile': str(mobile),
            'nickname': nickname,
            'password': "Zj123456",
            'password2': "Zj123456",
            'smsCode': str(sms_code),
            'username': username,
        }

        url = '/logon/'
        with self.client.post(url=url, data=data, catch_response=True) as response:
            # 断言，依赖 catch_response=True
            if response.status_code == 201:
                response.success()
            else:
                response.failure('注册失败')  # failure函数需要入参


class WebSite(HttpUser):
    tasks = [Task, ]  # 新版本用列表指定任务类
    host = 'http://121.4.47.229:8000'  # 这里写上host，在启动locust时就可以不写了
    min_wait = 2000
    max_wait = 3000  # task 每个用户执行两个任务间隔的上下限在2～3秒之间


if __name__ == '__main__':
    os.system('locust -f 测试平台-用户注册.py --master')
