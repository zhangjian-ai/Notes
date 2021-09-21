## 入门篇

### 简介

- Locust（俗称 蝗虫）一个轻量级的开源压测工具，基本功能是用Python代码描述所有测试。不需要笨拙的UI或庞大的XML，只需简单的代码即可。

### 安装依赖库

``` python
pip3 install locust

'''
Installing collected packages: 
brotli, roundrobin, pyzmq, psutil, msgpack, geventhttpclient, Flask-Cors, Flask-BasicAuth, ConfigArgParse, locust

说明：
	- pyzmq 主要是进程间通信的消息队列，用于分布式测试。
	- psutil 资源监控模块，包括服务器、数据库、JVM等。
	- geventhttpclient Locust基于协程并发，在单机上仍具有较高的并发能力。
	- Flask 相关模块，Locust 监控 web 是基于Flask开发的。
'''
```

- Locust 参数说明
  - -h, --help    查看帮助
  - -H HOST, --host=HOST    指定被测试的主机，采用以格式：http://10.21.32.33
  - --web-host=WEB_HOST    指定运行 Locust Web 页面的主机，默认为空 ''。
  - -P PORT, --port=PORT, --web-port=PORT    指定 --web-host 的端口，默认是8089
  - -f LOCUSTFILE, --locustfile=LOCUSTFILE    指定运行 Locust 性能测试文件，默认为: locustfile.py
  - --csv=CSVFILEBASE, --csv-base-name=CSVFILEBASE    以CSV格式存储当前请求测试数据。
  - --master    Locust 分布式模式使用，当前节点为 master 节点。
  - --worker    Locust 分布式模式使用，当前节点为 slave 节点。
  - --master-host=MASTER_HOST    分布式模式运行，设置 master 节点的主机或 IP 地址，只在与 --slave 节点一起运行时使用，默认为：127.0.0.1.
  - --master-port=MASTER_PORT    分布式模式运行， 设置 master 节点的端口号，只在与 --slave 节点一起运行时使用，默认为：5557。注意，slave 节点也将连接到这个端口+1 上的 master 节点。
  - --master-bind-host=MASTER_BIND_HOST    Interfaces (hostname, ip) that locust master should bind to. Only used when running with --master. Defaults to * (all available interfaces).
  - --master-bind-port=MASTER_BIND_PORT    Port that locust master should bind to. Only used when running with --master. Defaults to 5557. Note that Locust will also use this port + 1, so by default the master node will bind to 5557 and 5558.
  - --expect-slaves=EXPECT_SLAVES    How many slaves master should expect to connect before starting the test (only when --no-web used).
  - --no-web    no-web 模式运行测试，需要 -c 和 -r 配合使用.
  - -c NUM_CLIENTS, --clients=NUM_CLIENTS    指定并发用户数，作用于 --no-web 模式。
  - -r HATCH_RATE, --hatch-rate=HATCH_RATE    指定每秒启动的用户数，作用于 --no-web 模式。
  - -t RUN_TIME, --run-time=RUN_TIME    设置运行时间, 例如： (300s, 20m, 3h, 1h30m). 作用于 --no-web 模式。
  - -L LOGLEVEL, --loglevel=LOGLEVEL    选择 log 级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）. 默认是 INFO.
  - --logfile=LOGFILE    日志文件路径。如果没有设置，日志将去 stdout/stderr
  - --print-stats    在控制台中打印数据
  - --only-summary    只打印摘要统计
  - --no-reset-stats    Do not reset statistics once hatching has been completed。
  - -l, --list    显示测试类, 配置 -f 参数使用
  - --show-task-ratio    打印 locust 测试类的任务执行比例，配合 -f 参数使用.
  - --show-task-ratio-json    以 json 格式打印 locust 测试类的任务执行比例，配合 -f 参数使用.
  - -V, --version    查看当前 Locust 工具的版本.

### 两个关键的类（需要被继承使用）

- HTTPLocust：代码中客户端类需要继承该类，基于Locust类实现，同时封装requests库。

  > <font style="color: red">We’ve renamed the `Locust` and `HttpLocust` classes to `User` and `HttpUser` in version 1.0</font>

  - task_set：指向一个TaskSet类，TaskSet类定义了用户的任务信息，该静态字段为必填；
  - max_wait/min_wait：每个用户执行两个任务间隔的上下限（毫秒），具体数值在上下限中随机取值，若不指定则默认间隔时间为1秒；
  - host：被测试系统的host，当在终端中启动locust时没有指定--host参数时才会用到；
  - weight：同时运行多个Locust类时，用于控制不同类型的任务执行权重；
  - wait_time：每个任务之间设置间隔时间，随机从3~5区间内取，单位是 s； wait_time = between(3, 5)

- TaskSet：

  - TaskSet类实现了虚拟用户所执行任务的调度算法，包括规划任务执行顺序（schedule_task）、挑选下一个任务（execute_next_task）、执行任务（execute_task）、休眠等待（wait）、中断控制（interrupt）等待。在此基础上，就可以在TaskSet子类中采用非常简洁的方式来描述虚拟用户的业务测试场景，对虚拟用户的所有行为进行组织和描述，并可以对不同任务的权重进行配置。

  - 通过@task()装饰的方法为一个事务。方法的参数用于指定该行为的执行权重。参数越大每次被虚拟用户执行的概率越高。如果不设置默认为1。

  - TaskSet子类中定义任务信息时，采取两种方式：@task装饰器和tasks属性。

    ``` python
    # @task 定义任务
    from locust import TaskSet, task
    
    class UserBehavior(TaskSet):
        @task(1)
        def test_job1(self):
            self.client.get('/test1')
    
        @task(3)
        def test_job2(self):
            self.client.get('/test2')
    ```

    ``` python
    # tasks属性定义任务
    from locust import TaskSet
    
    def test_job1(obj):
        obj.client.get('/test1')
    
    def test_job2(obj):
        obj.client.get('/test2')
    
    class UserBehavior(TaskSet):
        tasks = {test_job1:1, test_job2:3}
        # tasks = [(test_job1,1), (test_job1,3)] # 两种方式等价
    ```

  - client属性：通过client属性来使用Python requests库的所有方法，调用方式与reqeusts完全一致。

  - TaskSet中的前置和后置。钩子函数 on_start、on_stop

    ```python
    class My_task_set(TaskSet):
      
        #添加初始化方法
        def on_start(self):
            print("类似类中的构造方法，每个用户的任务开始前，只执行一次")
      
        def on_stop(self):
            print("类似类中的后置方法，每个用户的任务结束后，只执行一次,")
    ```

### 检查点（断言）

- 在task任务中直接使用assert进行结果检查

- catch_response 参数

  ``` python
  class My_task_set(TaskSet):
    
      #添加初始化方法
      def on_start(self):
          print("类似类中的构造方法，每个用户的任务开始前，只执行一次")
    
      def on_stop(self):
          print("类似类中的后置方法，每个用户的任务结束后，只执行一次,")  
          
    	#这是某个任务,30是比例，比如这里是30/50
      @task(30)
      def getindex1(self):
          # client就是个requests对象
          # catch_response，告诉locust如何判断请求失败还是成功。
          with self.client.get("/",catch_response=True) as res:
            # 使用如下方式判断结果，必须让 catch_response=True，否则Locust并不能按预期区分
            if res.code == 200:
                res.success()
            else:
                res.failure("失败信息")
          
      @task(20)
      def getindex2(self):
          # client就是个requests对象
          res = self.client.get("/")
  				assert res.status_code == 200
  ```

### 启动Locust

> 以下是部分常用命令，详情可参考上面参数详解。可轻松组装出你想要的命令。

- 1、如果启动的locust文件名为locustfile.py并位于当前工作目录中，可以在编译器中直接运行该文件，或者通过cmd，执行如下命令：

   ``` 
   locust --host=https://www.cnblogs.com 
   ```

- 2、如果Locust文件位于子目录下且名称不是locustfile.py，可以使用-f命令启动上面的示例locust文件：

  ``` 
   locust -f testscript/locusttest.py --host=https://www.cnblogs.com 
  ```

- 3、如果要运行分布在多个进程中的Locust，通过指定`-master`以下内容来启动主进程 ：

   ``` 
   locust -f testscript/locusttest.py --master --host=https://www.cnblogs.com 
   ```

- 4、如果要启动任意数量的从属进程，可以通过-salve命令来启动locust文件：

  ``` 
  locust -f testscript/locusttest.py --worker --host=https://www.cnblogs.com 
  ```

- 5、如果要运行分布式Locust，必须在启动从机时指定主机（运行分布在单台机器上的Locust时不需要这样做，因为主机默认为127.0.0.1）：

   ``` 
   locust -f testscript/locusttest.py --worker --master-host=192.168.0.100 --host=https://cnblogs.com
   ```

- no web 模式

  ``` 
  locust -f stress_test.py --no-web -c 100 -r 20 -t 120
  
  --no-web：指定无 web UI模式
  -c：起多少 locust 用户（等同于起多少 tcp 连接）
  -r：多少时间内，把上述 -c 设置的虚拟用户全部启动
  -t：脚本运行多少时间，单位s
  ```

- 7、启动locust文件成功后，编译器控制台会显示如下信息：

  ``` 
  [2021-09-21 18:05:39,284] zhangjiandeMacBook-Pro.local/INFO/locust.main: Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)
  [2021-09-21 18:05:39,290] zhangjiandeMacBook-Pro.local/INFO/locust.main: Starting Locust 2.2.3
  ```

  - 8089是该服务启动的端口号，如果是本地启动，可以直接在浏览器输入http://localhost:8089打开UI界面，如果是其他机器搭建locust服务，则输入该机器的IP+端口即可。
  - Locust web 界面参数：
    - Number of users to simulate  设置**虚拟用户数，即并发用户数，对应中`no_web`模式的`-c, --clients`参数；**
    - Hatch rate（users spawned/second）**每秒产生(启动）的虚拟用户数** **， 对应着`no_web`模式的`-r, --hatch-rate`参数**，默认为1。

### 常见问题

- **COOKIES**
  - locust中的client会自动帮我们处理cookies。类似request.session()，所以如果我们登陆的时候，只需要在on_start中登陆一次就可以了。
- **多API问题**
  - 在locust中，如果url是不需要统计的，则我们不要用clent去访问api，应该用request去访问，这样就locust就不会统计request库发起的请请求。



## 实战篇

### 实战一：百度首页

``` python
import os

from locust import HttpUser, TaskSet, task


class Task(TaskSet):
    def on_start(self):
        print("前置操作，每个模拟用户开始执行task前都会执行")

    def on_stop(self):
        print("后置操作，每个模拟用户结束task后都会执行")

    @task
    def index(self):
        response = self.client.get('/')

        # 断言
        assert response.status_code == 200


class WebSite(HttpUser):
    tasks = [Task, ]  # 新版本用列表指定任务类
    host = 'https://www.baidu.com/'  # 这里写上host，在启动locust时就可以不写了
    min_wait = 2000
    max_wait = 3000  # task 任务执行时间间隔在2～3秒之间


if __name__ == '__main__':
    os.system('locust -f 百度首页测试.py ')
```



### 实战二：测试平台-用户注册

``` python
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
```



### 实战三：测试平台-添加用例

``` python
import json
import os
import random

from faker import Faker
from locust import HttpUser, TaskSet, task

from DbHelper import DbPool


class Task(TaskSet):
    fake = Faker(locale='zh_CN')
    pool = DbPool(host='121.4.47.229',
                  port=3300,
                  user='root',
                  password='zm_123456',
                  db='test_plat')

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
```



## 报告篇

- 性能参数

  - Type： 请求的类型，例如GET/POST。
  - Name：请求的路径。
  - request：当前请求的数量。
  - fails：当前请求失败的数量。
  - Median：中间值，单位毫秒，一半的服务器响应时间低于该值，而另一半高于该值。
  - 90%ile：百分位数。90%的响应时间对于该值，剩下的10%高于该值。
  - Average：平均值，单位毫秒，所有请求的平均响应时间。
  - Min：请求的最小服务器响应时间，单位毫秒。
  - Max：请求的最大服务器响应时间，单位毫秒。
  - Average size ：请求的平均大小，单位字节。
  - Current RPS：当前每秒钟请求的个数。类似Jmeter的TPS
  - Current Failures/s：当前每秒失败的请求数。

  **ps：**`RPS`和`平均响应时间`这两个指标显示的值都是根据最近2秒请求响应数据计算得到的统计值，我们也可以理解为瞬时值。



## 服务器监控 psutil（开箱即用）

> 服务器性能监控思路：
>
> ​	利用socket实时传输服务器信息。
>
> ​	需要编写socket服务端监控脚本和客户端接收监控信息。

``` python
import psutil
import datetime
import time
import platform
import socket
import sys
import os
import json
import redis
from multiprocessing import Process

monitor_process_types = ['python', 'java', 'scrapy', 'you-get']


def cal_process_msg(process_all_msg, process):
    process_all_msg['process_num'] += 1
    for process_type in monitor_process_types:
        if process_type in process['name'] or process_type in process['cmdline'] or process_type in process['exe']:
            process_all_msg[process_type] += 1
    if "run" in process['status']:
        process_all_msg['process_running_num'] += 1
        process_all_msg["process_running_mem_percent"] += process.get("memory_percent")

    else:
        if "stop" in process['status']:
            process_all_msg['process_stopped_num'] += 1
            process_all_msg["process_stopped_mem_percent"] += process.get("memory_percent")
        else:
            process_all_msg['process_sleeping_num'] += 1
            process_all_msg["process_sleeping_mem_percent"] += process.get("memory_percent")


def get_disk_speed(interval):
    disk_msg = psutil.disk_io_counters()
    read_count, write_count = disk_msg.read_count, disk_msg.write_count
    read_bytes, write_bytes = disk_msg.read_bytes, disk_msg.write_bytes
    read_time, write_time = disk_msg.read_time, disk_msg.write_time
    time.sleep(interval)
    disk_msg = psutil.disk_io_counters()
    read_count2, write_count2 = disk_msg.read_count, disk_msg.write_count
    read_bytes2, write_bytes2 = disk_msg.read_bytes, disk_msg.write_bytes
    read_time2, write_time2 = disk_msg.read_time, disk_msg.write_time
    read_count_speed = str(int((read_count2 - read_count) / interval)) + " 次/s"
    write_count_speed = str(int((write_count2 - write_count) / interval)) + " 次/s"

    read_bytes_speed = (read_bytes2 - read_bytes) / interval
    read_bytes_speed = str(round((read_bytes_speed / 1048576), 2)) + " MB/s" if read_bytes_speed >= 1048576 else str(
        round((read_bytes_speed / 1024), 2)) + " KB/s"
    write_bytes_speed = (write_bytes2 - write_bytes) / interval
    write_bytes_speed = str(round((write_bytes_speed / 1048576), 2)) + " MB/s" if write_bytes_speed >= 1048576 else str(
        round((write_bytes_speed / 1024), 2)) + " KB/s"
    return read_count_speed, write_count_speed, read_bytes_speed, write_bytes_speed


def get_net_speed(interval):
    net_msg = psutil.net_io_counters()
    bytes_sent, bytes_recv = net_msg.bytes_sent, net_msg.bytes_recv
    time.sleep(interval)
    net_msg = psutil.net_io_counters()
    bytes_sent2, bytes_recv2 = net_msg.bytes_sent, net_msg.bytes_recv
    sent_speed = (bytes_sent2 - bytes_sent) / interval
    sent_speed = str(round((sent_speed / 1048576), 2)) + " MB/s" if sent_speed >= 1048576 else str(
        round((sent_speed / 1024), 2)) + " KB/s"
    recv_speed = (bytes_recv2 - bytes_recv) / interval
    recv_speed = str(round((recv_speed / 1048576), 2)) + " MB/s" if recv_speed >= 1048576 else str(
        round(recv_speed / 1024, 2)) + " KB/s"

    return sent_speed, recv_speed


def main():
    server_info = {}
    print('-----------------------------系统信息-------------------------------------')

    os_info = {}
    os_name = platform.platform()
    pc_name = platform.node()
    processor = platform.processor()
    processor_bit = platform.architecture()[0]
    myname = socket.gethostname()
    # myaddr = socket.gethostbyname(myname)

    print(f"{'系统信息:':<15s}{os_name}")
    print(f"{'机器名称:':<15s}{pc_name}")
    print(f"{'处理器:':<15s}{processor}")
    print(f"{'处理器位数:':<15s}{processor_bit}")
    # print(f"{'IP地址:':<15s}{myaddr}")

    # print(f"系统信息:{os_name:>6s}\n机器名称:{pc_name}\n处理器:{processor}\n处理器位数:{bit_msg}\nIP:{myaddr}")
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(psutil.boot_time())))

    users_count = len(psutil.users())
    users_list = ",".join([u.name for u in psutil.users()])
    print(f"{'当前用户数量:':<15s}{users_count}")
    print(f"{'当前用户名:':<15s}{users_list}")

    boot_time_seconds = time.strptime(boot_time, "%Y-%m-%d %H:%M:%S")
    boot_time_seconds = int(time.mktime(boot_time_seconds))
    boot_hours = str(round((int(time.time()) - boot_time_seconds) / (60 * 60), 1)) + "小时"

    print(f"{'系统启动时间:':<15s}{boot_time}")
    print(f"{'系统当前时间:':<15s}{now_time}")
    print(f"{'系统已经运行:':<15s}{boot_hours}")
    # ip = myaddr[myaddr.rfind(".") + 1:]

    # os_info['os_ip'] = ip
    os_info['os_name'] = os_name
    os_info['os_pcname'] = pc_name
    os_info['os_processor'] = processor
    os_info['os_processor_bit'] = processor_bit
    os_info['os_boot_hours'] = boot_hours
    os_info['os_users_count'] = users_count

    server_info["os_info"] = os_info

    print('-----------------------------cpu信息-------------------------------------')
    cpu_info = {}
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_logic_cores = psutil.cpu_count(logical=True)
    cpu_used_percent = str(psutil.cpu_percent(interval=1, percpu=False)) + '%'
    # cpu_used_average = 0
    # for i in psutil.cpu_percent(interval = 1,percpu=True):
    # 	cpu_used_average += i
    # cpu_used_average = cpu_used_average/len(psutil.cpu_percent(interval = 1,percpu=True))
    # print(cpu_used_average)
    print(f"{'cpu使用率:':<15s}{cpu_used_percent}")
    print(f"{'物理cpu数量:':<15s}{cpu_cores}")
    print(f"{'逻辑cpu数量:':<15s}{cpu_logic_cores}")

    cpu_info['cpu_used_percent'] = cpu_used_percent
    cpu_info['cpu_cores'] = cpu_cores
    cpu_info['cpu_logic_cores'] = cpu_logic_cores

    server_info["cpu_info"] = cpu_info

    print('-----------------------------内存信息-------------------------------------')

    memory_info = {}
    memory = psutil.virtual_memory()
    mem_total = str(round(memory.total / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
    mem_free = str(round(memory.free / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
    mem_available = str(round(memory.available / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
    mem_used_percent = str(memory.percent) + "%"
    mem_used = str(round(memory.used / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
    try:
        buffers = str(round(memory.buffers / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
        cached = str(round(memory.cached / (1024.0 * 1024.0 * 1024.0), 2)) + "Gb"
    except:
        buffers = cached = ""
    print(f"{'内存使用率:':<15s}{mem_used_percent}")
    print(f"{'总内存:':<15s}{mem_total}")
    print(f"{'已使用内存:':<15s}{mem_used}")
    print(f"{'剩余内存:':<15s}{mem_free}")
    print(f"{'available内存:':<15s}{mem_available}")

    print(f"{'cached使用的内存:':<15s}{cached}")
    print(f"{'buffers使用的内存:':<15s}{buffers}")

    memory_info['mem_used_percent'] = mem_used_percent
    memory_info['mem_total'] = mem_total
    memory_info['mem_used'] = mem_used
    memory_info['mem_free'] = mem_free
    memory_info['mem_cached'] = cached
    memory_info['mem_buffers'] = buffers

    server_info["memory_info"] = memory_info

    print('-----------------------------磁盘信息---------------------------------------')

    # disk_msg = psutil.disk_usage("")
    # disk_total = str(int(disk_msg.total / (1024.0 * 1024.0 * 1024.0))) + "G"
    # disk_used = str(int(disk_msg.used / (1024.0 * 1024.0 * 1024.0))) + "G"
    # disk_free = str(int(disk_msg.free / (1024.0 * 1024.0 * 1024.0))) + "G"
    # disk_percent = float(disk_msg.percent)
    # print(f"磁盘总容量:{disk_total},已用容量:{disk_used},空闲容量:{disk_free},使用率:{disk_percent}%")
    # print("系统磁盘信息：" + str(io))
    disk_info = {}
    disk_partitons = psutil.disk_partitions()

    for disk in disk_partitons:
        print(disk)
        try:
            o = psutil.disk_usage(disk.mountpoint)
            path = disk.device
            total = str(int(o.total / (1024.0 * 1024.0 * 1024.0))) + "G"
            used = str(int(o.used / (1024.0 * 1024.0 * 1024.0))) + "G"
            free = str(int(o.free / (1024.0 * 1024.0 * 1024.0))) + "G"
            percent = o.percent
            print(f"磁盘路径:{path},总容量:{total},已用容量{used},空闲容量:{free},使用率:{percent}%")

            if disk.mountpoint == "/":
                disk_info["total"] = total
                disk_info["used"] = used
                disk_info["free"] = free
                disk_info["percent"] = percent


        except:
            print("获取异常", disk)
    read_count_speed, write_count_speed, read_bytes_speed, write_bytes_speed = get_disk_speed(3)
    print("硬盘实时IO")
    print(f"读取次数:{read_count_speed} 写入次数:{write_count_speed}")
    print(f"读取速度:{read_bytes_speed} 写入速度:{write_bytes_speed}")
    disk_info['disk_read_count_speed'] = read_count_speed
    disk_info['disk_write_count_speed'] = write_count_speed
    disk_info['disk_read_bytes_speed'] = read_bytes_speed
    disk_info['disk_write_bytes_speed'] = write_bytes_speed

    server_info["disk_info"] = disk_info

    print('-----------------------------网络信息-------------------------------------')

    net_info = {}
    sent_speed, recv_speed = get_net_speed(1)
    print(f"网络实时IO\n上传速度:{sent_speed}\n下载速度:{recv_speed}")
    net = psutil.net_io_counters()
    sent_bytes = net.bytes_recv / 1024 / 1024
    recv_bytes = net.bytes_sent / 1024 / 1024

    sent_bytes = str(round(sent_bytes, 2)) + "MB" if sent_bytes < 1024 else str(round(sent_bytes / 1024, 2)) + "GB"
    recv_bytes = str(round(recv_bytes, 2)) + "MB" if recv_bytes < 1024 else str(round(recv_bytes / 1024, 2)) + "GB"

    print(f"网卡总接收流量{recv_bytes}\n总发送流量{sent_bytes}")

    net_info['net_sent_speed'] = sent_speed
    net_info['net_recv_speed'] = recv_speed

    net_info['net_recv_bytes'] = recv_bytes
    net_info['net_sent_bytes'] = sent_bytes

    server_info["net_info"] = net_info

    print('-----------------------------进程信息-------------------------------------')
    # 查看系统全部进程

    processes_info = {}
    processes_info['process_running_num'] = 0
    processes_info['process_sleeping_num'] = 0
    processes_info['process_stopped_num'] = 0

    for process_type in monitor_process_types:
        processes_info[process_type] = 0

    processes_info["process_sleeping_mem_percent"] = 0
    processes_info["process_stopped_mem_percent"] = 0
    processes_info["process_running_mem_percent"] = 0

    processes_info['process_num'] = 0

    processes_info['process_memory_used_top10'] = []
    process_list = []

    for pnum in psutil.pids():

        try:
            p = psutil.Process(pnum)

            # print("====================================")
            process = {}
            process['name'] = p.name()
            process['cmdline'] = p.cmdline()
            process['exe'] = p.exe()
            process['status'] = p.status()
            process['create_time'] = str(datetime.datetime.fromtimestamp(p.create_time()))[:19]
            process['terminal'] = p.terminal()
            # process['cpu_times'] = p.cpu_times()
            # process['cpu_affinity'] = p.cpu_affinity()
            # process['memory_info'] = p.memory_info()
            process['memory_percent'] = p.memory_percent()
            process['open_files'] = p.open_files()
            # process['connections'] = p.connections()

            process['io_counters'] = p.io_counters()
            process['num_threads'] = p.num_threads()
            cal_process_msg(processes_info, process)

            process_list.append(process)
        # print(process)

        # print(f"进程名: {p.name()}  进程状态: {p.status()}  命令: {p.cmdline()}  进程号: {p.pid}  路径1: {p.exe()}  路径2: {p.cwd()}  内存占比: {round(p.memory_percent(),2)}%")
        except:
            pass
    processes_info["process_sleeping_mem_percent"] = str(processes_info["process_sleeping_mem_percent"])[:5] + "%"
    processes_info["process_stopped_mem_percent"] = str(processes_info["process_stopped_mem_percent"])[:5] + "%"
    processes_info["process_running_mem_percent"] = str(processes_info["process_running_mem_percent"])[:5] + "%"

    process_list = sorted(process_list, key=lambda x: (-int(x['memory_percent'])), reverse=False)
    print(process_list[:10])
    for i in process_list[:10]:
        top_10_info = i.get("cmdline")[0] + " " + i.get("cmdline")[1] + " " + str(i.get("memory_percent"))[:5] + "%"
        processes_info['process_memory_used_top10'].append(top_10_info)

    print(processes_info)

    server_info["processes_info"] = processes_info

    server_info_json = json.dumps(server_info, ensure_ascii=False, indent=4)
    print(server_info_json)
    pool = redis.ConnectionPool(host='ip', port=6379, decode_responses=True,
                                password='password',
                                db=2)  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379

    r = redis.Redis(connection_pool=pool)
    # r.hset("server_info", ip, server_info_json)


if __name__ == "__main__":
    main()
    print(sys.argv[0], os.getpid())
```

