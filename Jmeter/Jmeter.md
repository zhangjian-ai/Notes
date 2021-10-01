## 环境安装

### 安装JDK

- 下载JDK安装包：**https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html**

- Unix/Linux 将安装包copy到对应目录解压，然后配置环境变量。

  ``` shell
  # 在profile中添加如下配置
  export JAVA_HOME=/usr/local/jdk1.8.0_181/  #jdk安装目录  
  export CLASSPATH=.:${JAVA_HOME}/lib/:${JRE_HOME}/jre/lib
  export PATH=$PATH:${JAVA_HOME}/bin:${JAVA_HOME}/jre/bin:$PATH
  
  # -----------------------
  # linux/unix(intel) 配置文件路径: /etc/profile
  # unix(m1)配置文件路径：~/.zprofile
  
  # 添加脚本后，重新加载配置文件使其生效
  source /etc/profile
  
  # 检查安装情况
  java -version		# 查看java版本信息
  javac/java		# 查看是否有命令相关help信息
  ```

- Windows 安装大同小异，环境变量再计算机 -> 高级选项中配置即可。



### 安装Jmeter

- 下载Jmeter安装包： **http://jmeter.apache.org/ **

- Jmeter安装包解压即可使用。为了cmd能够全局使用，将启动文件配置到环境变量。

  ``` shell
  export JMETER_HOME=/var/local/apache-jmeter-5.4.1  # jmeter解压后的目录
  export PATH=${JMETER_HOME}/bin:$PATH
  export CLASSPATH=${JMETER_HOME}/lib/ext/ApacheJMeter_core.jar:${JMETER_HOME}/lib/jorphan.jar:${CLASSPATH}
  
  # 添加脚本后，重新加载配置文件使其生效
  source /etc/profile
  
  # 检查安装情况
  jmeter -v  # 打印jmeter版本信息
  ```



### 安装 Ant

- 下载Ant安装包：**https://ant.apache.org/bindownload.cgi**

- Ant 安装包解压后即可使用，同Jmeter

  ``` shell
  export JMETER_HOME=/var/local/apache-ant-1.10.11
  export PATH=${JMETER_HOME}/bin:$PATH
  
  # 添加脚本后，重新加载配置文件使其生效
  source /etc/profile
  
  # 检查安装情况
  ant -version  # 打印jmeter版本信息
  ```

  



## 配置详解

### 线程组

- **在取样器错误后要执行的动作：**
  -  这个指的是后续测试过程中如果发生错误，但测试计划并未满足预先设计的结束条件，是否继续执行。

- **线程数 :**
  - 即需要创建多少个线程，理解为需要启动多少个虚拟用户。

- **Ramp-Up时间(秒)：**
  - 即创建线程的准备时间， 和线程数组合，即希望在多少秒内创建多少个线程，这只是个尽量，不一定准。

- **循环次数：**
  - 这里有两个选项， 一旦勾选永远，则输入框不可用。与上述两个属性组合起来，即每多少秒创建多少线程发送请求，然后持续到永远，一直不停止。这个是基于时间，而不是次数。也可以取消勾选永远， 而精确到循环次数。

- **调度器：**
  - 持续时间(s):
    - 配合上面循环次数中的永远使用， 这样即可以不以次数为目标，而是以调度器指定的持续时间来完成测试任务， 当整个测试计划执行中达到了指定的时间，则测试计划终止。
  - 延迟启动(s):
    - 即在脚本启动后，延迟多少秒才开始执行测试。



### 配置元件





### 常用插件





## 启动测试

### 命令行模式启动

``` shell
jmeter -n -t [jmx file] -l [result file] -e -o [Path to web report folder]

# -n 表示已 non-web 方式执行
# -t 指定测试的 .jmx 文件
# -l 测试结果文件，是一个 .jtl 文件
# -e 生成测试报告
# -o 指定测试报告存放位置，是一个目录，里面有html文件可以预览

# 举例：
jmeter -n -t jmx/boot-quick.jmx -l jmx/boot-quick.jtl -e -o jmx/report
```



### 命令行启动分布式



## 性能分析定位

### 常见性能分析定位

- top 命令中CPU性能指标定位方向

  ``` shell
  [root@VM-0-10-centos ~]# top
  top - 15:41:25 up 1 day, 22:17,  1 user,  load average: 0.29, 0.18, 0.11
  Tasks: 113 total,   1 running, 112 sleeping,   0 stopped,   0 zombie
  %Cpu(s):  0.3 us,  0.7 sy,  0.0 ni, 99.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
  
  # 定位分析：
  # us、sy 高 重点看进程
  # hi 高 重点看硬中断相关
  # si 高 重点看网络相关
  # wa 高 重点看磁盘IO相关的
  ```

  - 假如一个进程ID为 6401 的java进程占用cpu很高

    - 查看当前进程下 线程 的状态，看哪些线程占用cpu资源多

      ``` shell
      top -Hp 6401  # 打印指定进程下 线程的资源占用信息。找到一个 线程ID 为 6425 的线程，资源占用特别高。
      ```

    - 线程ID 在 jstack 中是十六进制的，所以在查看时要转换一下(6425 -> 0x1919)

      ``` shell
      # jstack 查看 java stack、native stack 信息，可以获取到 相关线程信息。
      # jmap 查看进程 内存分配的相关信息。
      # jstat 查看进程中 classloader、compiler、gc 相关信息
      jstack 6401 | grep -A10 -B10 1919  # 匹配 6401 进程中，0x1919 线程 前10行和后10行的信息
      ```

    - 通过上面的打印信息，可以看到 线程的运行状态、以及当前正运行在哪个文件的哪一行。

    - 打开对应的 .java 文件，既可以看到 被运行的 代码，就可以看到 为什么 线程占用 cpu 大的原因。

    - 如果只能看到编译后的 .class 文件，可以借助反编译工具 JD-GUI(java decompile)，将 class 反编译成 java 文件。

    - 地址：**https://jd-gui.apponic.com/mac/**



## Jenkins Jmeter Ant 持续集成

> jenkins上面安装相关插件：ant、

