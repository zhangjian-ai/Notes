import json
import os
import random

from faker import Faker
from locust import HttpUser, TaskSet, task

from .database import DBPool


class Task(TaskSet):
    fake = Faker(locale='zh_CN')
    # pool = DBPool(host='121.4.47.229',
    #               port=3300,
    #               user='root',
    #               password='zm_123456',
    #               db='test_plat')

    def on_start(self):
        # 前置登陆
        id = random.randint(1, 1500)
        sql = f'select username from tp_users where id = {id}'
        username = self.pool.qyuery_one(sql).get('username')

        data = {
            'password': "Zj123456",
            'type': "account",
            'username': username.decode()
        }

        # 添加头信息
        self.client.headers['Content-Type'] = 'application/json;'

        with self.client.post(url='/login/', data=json.dumps(data)) as res:
            token = res.json().get('token')

            self.client.headers['Authorization'] = 'JWT ' + token

    @task
    def add_case(self):
        data = {
            'description': self.fake.sentence(),
            'expectation': self.fake.sentence(),
            'is_auto': False,
            'module': 3,
            'name': self.fake.sentence(),
            'priority': random.randint(1, 3),
            'step': self.fake.sentence()
        }

        with self.client.post(url='/case/', data=json.dumps(data), catch_response=True) as res:
            if '用例添加成功' in res.text:
                res.success()
            else:
                res.failure(f'用例添加失败！{res.text}')


class WebSite(HttpUser):
    tasks = [Task, ]  # 新版本用列表指定任务类
    host = 'http://121.4.47.229:8000'  # 这里写上host，在启动locust时就可以不写了
    min_wait = 2000
    max_wait = 3000


if __name__ == '__main__':
    os.system('locust -f 测试平台-添加用例.py')
