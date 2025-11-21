### 基础命令

#### 查看 ADB 版本及安装路径
- 命令：`adb version`
- 含义：查看 ADB 的版本信息及安装路径。
- 示例：`adb version`，成功执行后会显示 ADB 的版本号及安装路径等信息，如 `Android Debug Bridge version 1.0.41`。

#### 查看已连接设备
- 命令：`adb devices`
- 含义：查看当前已连接到计算机的 Android 设备。
- 示例：`adb devices`，执行后会列出已连接的设备，如 `List of devices attached` 下方显示设备的序列号。

#### 启动/关闭 ADB 服务
- 启动服务：`adb start-server`
- 关闭服务：`adb kill-server`
- 含义：分别用于启动和关闭 ADB 服务。
- 示例：`adb start-server` 用于启动 ADB 服务，`adb kill-server` 用于关闭 ADB 服务。

#### 截图
- 命令：`adb shell screencap -p /sdcard/screenshot.png`，然后使用 `adb pull /sdcard/screenshot.png` 将截图文件从设备中拉取到本地。
- 含义：通过 ADB 命令实现对设备屏幕的截图，并将截图文件保存到指定位置。
- 示例：执行上述命令后，设备的屏幕截图会被保存到设备的 `/sdcard/` 目录下，并可通过 `adb pull` 命令将截图文件拉取到本地指定目录。

#### 文件传输
- 从设备复制文件到本地：`adb pull <remote&gt; &lt;local&gt;`
- 将本地文件复制到设备：`adb push &lt;local&gt; &lt;remote&gt;`
- 含义：`adb pull` 命令用于将设备中的文件复制到本地计算机，`adb push` 命令用于将本地计算机的文件复制到设备中。
- 示例：`adb pull /sdcard/yourfile.txt /path/to/local/directory/` 将设备中的 `yourfile.txt` 文件复制到本地的 `/path/to/local/directory/` 目录下；`adb push /path/to/local/file.txt /sdcard/` 将本地的 `file.txt` 文件复制到设备的 `/sdcard/` 目录下。

#### 安装 APK
- 命令：`adb install &lt;apk_path&gt;`
- 含义：在设备上安装指定路径的 APK 文件。
- 示例：`adb install -r -t -d xxx/yyy.apk`，其中 `-r` 表示覆盖安装，保留数据，`-t` 允许安装测试 APK，即开发常常用到的 debug 版本，`-d` 允许版本降级安装，即要安装的版本低于手机里的应用版本。

### Shell命令


#### 查看设备信息
- 命令：`adb shell pm get-package-info &lt;package_name&gt;`
- 含义：查看指定应用的详细信息，包括其安装位置、权限等。
- 示例：`adb shell pm get-package-info com.example.myapp | grep dataDir`，可查看指定应用的数据目录路径。

#### 强制停止应用
- 命令：`adb shell am force-stop &lt;package_name&gt;`
- 含义：强制停止指定应用的运行。
- 示例：`adb shell am force-stop com.example.yourapp`，用于强制停止 `com.example.yourapp` 应用的运行。

#### 安装应用到 SD 卡
- 命令：`adb install -r -s &lt;path_to_apk&gt;`
- 含义：将 APK 文件强制安装到设备的 SD 卡上。
- 示例：`adb install -r -s /path/to/your/app.apk`，将 `/path/to/your/app.apk` 安装到设备的 SD 卡上。

#### 查看应用安装位置
- 命令：`adb shell pm get-install-location | grep -w [internal|external]`
- 含义：检查应用是安装在内部存储还是外部存储。
- 示例：`adb shell pm get-install-location | grep -w [internal|external]`，通过该命令可查看应用的安装位置是在内部存储还是外部存储。

#### 查询应用包名列表
- 命令：`adb shell pm list packages`
- 含义：列出设备上安装的所有应用的包名。
- 示例：`adb shell pm list packages`，执行后会列出设备上所有已安装应用的包名。

#### 清除应用缓存
- 命令：`adb shell pm clear &lt;package_name&gt; --keep-data`
- 含义：清除指定应用的缓存，但保留其数据。
- 示例：`adb shell pm clear &lt;package_name&gt; --keep-data`，用于清除指定应用的缓存，但保留其数据。

#### 备份应用数据
- 命令：`adb backup -f &lt;backup_file&gt; &lt;package_name&gt;`
- 含义：备份指定应用的数据。
- 示例：`adb backup -f /sdcard/backup.ab com.example.yourapp`，将 `com.example.yourapp` 应用的数据备份到 `/sdcard/backup.ab` 文件中。

#### 恢复应用数据
- 命令：`adb restore &lt;backup_file&gt;`
- 含义：从备份文件中恢复应用数据。
- 示例：`adb restore /sdcard/backup.ab`，从 `/sdcard/backup.ab` 备份文件中恢复应用数据。

#### 查看应用权限
- 命令：`adb shell dumpsys package &lt;package_name&gt; | grep -A 10 "requested permissions"`
- 含义：显示指定应用请求的权限列表。
- 示例：`adb shell dumpsys package &lt;package_name&gt; | grep -A 10 "requested permissions"`，通过该命令可查看指定应用请求的权限列表。

#### 启动 Activity
- 命令：`adb shell am start -n &lt;package_name&gt;/&lt;activity_name&gt;`
- 含义：启动指定应用的 Activity。
- 示例：`adb shell am start -n com.example.myapp/.MainActivity`，启动 `com.example.myapp` 应用的 `MainActivity`。

#### 停止 Activity
- 命令：`adb shell am force-stop &lt;package_name&gt;`
- 含义：强制停止指定应用的所有 Activity。
- 示例：`adb shell am force-stop com.example.myapp`，强制停止 `com.example.myapp` 应用的所有 Activity。

#### 获取当前前台 Activity
- 命令：`adb shell dumpsys activity top`
- 含义：获取当前设备上运行的前台 Activity。
- 示例：`adb shell dumpsys activity top`，执行后会显示当前设备上运行的前台 Activity。

#### 获取当前前台所有 Activity
- 命令：`adb shell dumpsys activity activities | grep mResumedActivity`
- 含义：获取当前设备上运行的前台 Activity。
- 示例：`adb shell dumpsys activity activities | grep mResumedActivity`，执行后会显示当前设备上运行的前台 Activity。

#### 发送广播
- 命令：`adb shell am broadcast -a &lt;action_name&gt;`
- 含义：发送指定的广播。
- 示例：`adb shell am broadcast -a android.intent.action.BOOT_COMPLETED`，发送设备启动完成的广播。

#### 启动 Service
- 命令：`adb shell am startservice -n &lt;package_name&gt;/&lt;service_name&gt;`
- 含义：启动指定应用的 Service。
- 示例：`adb shell am startservice -n com.example.myapp/.MyService`，启动 `com.example.myapp` 应用的 `MyService`。

#### 杀死进程
- 命令：`adb shell am kill &lt;package_name&gt;`
- 含义：杀死指定应用的所有进程。
- 示例：`adb shell am kill com.example.myapp`，杀死 `com.example.myapp` 应用的所有进程。

### Monkey命令


#### 随机事件模式
- 命令：`adb shell monkey &lt;event_count&gt;`
- 含义：让 Monkey 在设备上执行指定次数的随机事件，用于测试应用的稳定性。
- 示例：`adb shell monkey 100`，让 Monkey 在设备上执行 100 次随机事件。

#### 指定应用测试
- 命令：`adb shell monkey -p &lt;package_name&gt; &lt;event_count&gt;`
- 含义：让 Monkey 仅针对指定应用执行随机事件测试。
- 示例：`adb shell monkey -p com.example.yourapp 100`，让 Monkey 仅针对 `com.example.yourapp` 应用执行 100 次随机事件。

#### 日志输出
- 命令：`adb shell monkey -p &lt;package_name&gt; -v -v -v &lt;event_count&gt; &gt; &lt;log_file_path&gt;`
- 含义：在执行 Monkey 测试时，将详细的日志信息输出到指定文件中，便于后续分析。其中 `-v` 参数用于提高日志级别，最高可加三个 `-v`，表示最详细的日志信息。
- 示例：`adb shell monkey -p com.example.yourapp -v -v -v 100 &gt; D:\\log.txt`，将 Monkey 测试的详细日志输出到 `D:\\log.txt` 文件中。

#### 指定 Seed 值
- 命令：`adb shell monkey -s &lt;seed_value&gt; -p &lt;package_name&gt; -v -v -v &lt;event_count&gt; &gt; &lt;log_file_path&gt;`
- 含义：通过指定 Seed 值，使 Monkey 的随机事件序列可重复，便于复现问题。`&lt;seed_value&gt;` 是一个整数，用于初始化随机数生成器。
- 示例：`adb shell monkey -s 123 -p com.example.yourapp -v -v -v 100 &gt; D:\\log.txt`，指定 Seed 值为 123，执行 Monkey 测试并将日志输出到 `D:\\log.txt` 文件中。

#### 指定操作间隔
- 命令：`adb shell monkey -p &lt;package_name&gt; --throttle &lt;throttle_time&gt; &lt;event_count&gt; &gt; &lt;log_file_path&gt;`
- 含义：设置 Monkey 执行事件之间的间隔时间，单位为毫秒。
- 示例：`adb shell monkey -p com.example.yourapp --throttle 1000 200 &gt; D:\\log.txt`，设置 Monkey 执行事件之间的间隔时间为 1000 毫秒，执行 200 次随机事件，并将日志输出到 `D:\\log.txt` 文件中。

#### 忽略崩溃和超时
- 命令：`adb shell monkey --ignore-crashes --ignore-timeouts -p &lt;package_name&gt; &lt;event_count&gt;`
- 含义：在 Monkey 测试过程中，忽略应用的崩溃和超时情况，继续执行测试。
- 示例：`adb shell monkey --ignore-crashes --ignore-timeouts -p com.example.yourapp 500`，在 Monkey 测试过程中忽略应用的崩溃和超时情况，继续执行 500 次随机事件。

#### 指定事件类型比例
- 命令：`adb shell monkey --pct-touch &lt;touch_percent&gt; --pct-motion &lt;motion_percent&gt; -p &lt;package_name&gt; &lt;event_count&gt;`
- 含义：设置 Monkey 测试中不同类型事件的比例，如触摸事件和动作事件的比例。
- 示例：`adb shell monkey --pct-touch 50 --pct-motion 50 -p com.example.yourapp 1000`，设置触摸事件和动作事件各占 50% 的比例，执行 1000 次随机事件。

### 其他命令

#### 查看日志
- 命令：`adb logcat`
- 含义：查看设备的日志输出，可帮助开发者调试应用。
- 示例：`adb logcat`，执行后会显示设备的日志信息，可通过过滤等方式查看特定的日志内容。

#### 过滤日志
- 命令：`adb logcat | grep &lt;keyword&gt;`
- 含义：通过关键字过滤日志信息，便于快速定位问题。
- 示例：`adb logcat | grep "Error"`，过滤出包含 "Error" 关键字的日志信息。

#### 查看设备属性
- 命令：`adb shell getprop`
- 含义：查看设备的系统属性信息。
- 示例：`adb shell getprop`，执行后会列出设备的各种系统属性，如设备型号、Android 版本等。

#### 设置设备属性
- 命令：`adb shell setprop &lt;property_name&gt; &lt;property_value&gt;`
- 含义：设置设备的系统属性。
- 示例：`adb shell setprop debug.adb.wait-for-device 1`，设置设备的 `debug.adb.wait-for-device` 属性为 1。

#### 查看设备屏幕密度
- 命令：`adb shell wm density`
- 含义：查看设备的屏幕密度。
- 示例：`adb shell wm density`，执行后会显示设备的屏幕密度值，如 `Physical density: 480`。

#### 查看设备屏幕分辨率
- 命令：`adb shell wm size`
- 含义：查看设备的屏幕分辨率。
- 示例：`adb shell wm size`，执行后会显示设备的屏幕分辨率，如 `Physical size: 1080x1920`。

#### 查看设备电池状态
- 命令：`adb shell dumpsys battery`
- 含义：查看设备的电池状态信息。
- 示例：`adb shell dumpsys battery`，执行后会显示设备的电池状态，如电量百分比、充电状态等。

#### 查看设备内存信息
- 命令：`adb shell dumpsys meminfo`
- 含义：查看设备的内存使用情况。
- 示例：`adb shell dumpsys meminfo`，执行后会显示设备的内存信息，如总内存、可用内存等。

#### 查看设备 CPU 信息
- 命令：`adb shell dumpsys cpuinfo`
- 含义：查看设备的 CPU 使用情况。
- 示例：`adb shell dumpsys cpuinfo`，执行后会显示设备的 CPU 信息，如 CPU 核心数、CPU 使用率等。

#### 查看设备网络状态
- 命令：`adb shell dumpsys network`
- 含义：查看设备的网络连接状态。
- 示例：`adb shell dumpsys network`，执行后会显示设备的网络状态信息，如网络类型、网络连接状态等。

- 中动作事件的比例。





### 命令到TCP映射

| 命令名称                              | 功能描述                  | 命令格式                                                     | TCP层传输数据示例                                            | TCP层传输数据说明                                            |
| ------------------------------------- | ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| adb devices                           | 查看已连接的设备          | host:devices                                                 | `0010 host:devices`                                          | 0010表示命令长度为16字节，后接命令host:devices               |
| adb version                           | 查看ADB版本               | host:version                                                 | `000c host:version`                                          | 000c表示命令长度为12字节，后接命令host:version               |
| adb kill-server                       | 停止ADB服务器             | host:kill                                                    | `000c host:kill`                                             | 000c表示命令长度为12字节，后接命令host:kill                  |
| adb shell                             | 进入设备的command shell   | shell:<command>                                              | `0008 shell:ls`                                              | 0008表示命令长度为8字节，后接命令shell:ls                    |
| adb install                           | 安装应用                  | host:track-install:\<package\_path>                          | `0018 host:track-install:/path/to/app.apk`                   | 0018表示命令长度为24字节，后接命令host:track-install:/path/to/app.apk |
| adb forward                           | 端口转发                  | host:forward:<local>:<remote>                                | `0014 host:forward:tcp:8888,tcp:9999`                        | 0014表示命令长度为20字节，后接命令host:forward:tcp:8888,tcp:9999 |
| adb get-state                         | 查看设备状态              | host:get-state                                               | `0010 host:get-state`                                        | 0010表示命令长度为16字节，后接命令host:get-state             |
| adb reconnect                         | 重新连接设备              | host:reconnect:<serialnumber>                                | `0012 host:reconnect:1234567890`                             | 0012表示命令长度为18字节，后接命令host:reconnect:1234567890  |
| adb root                              | 以root权限运行ADB守护进程 | host:root                                                    | `000c host:root`                                             | 000c表示命令长度为12字节，后接命令host:root                  |
| adb reboot                            | 重启设备                  | host:reboot                                                  | `000e host:reboot`                                           | 000e表示命令长度为14字节，后接命令host:reboot                |
| adb logcat                            | 查看设备日志              | shell:logcat                                                 | `000a shell:logcat`                                          | 000a表示命令长度为10字节，后接命令shell:logcat               |
| adb bugreport                         | 获取设备的bug报告         | shell:bugreport                                              | `000c shell:bugreport`                                       | 000c表示命令长度为12字节，后接命令shell:bugreport            |
| adb pull                              | 从设备拉取文件            | host:pull:<source>:<destination>                             | `0018 host:pull:/sdcard/file.txt:/local/path`                | 0018表示命令长度为24字节，后接命令host:pull:/sdcard/file.txt:/local/path |
| adb push                              | 推送文件到设备            | host:push:<source>:<destination>                             | `0016 host:push:/local/file.txt:/sdcard`                     | 0016表示命令长度为22字节，后接命令host:push:/local/file.txt:/sdcard |
| adb uninstall                         | 卸载应用                  | host:uninstall:\<package\_name>                              | `0016 host:uninstall:com.example.app`                        | 0016表示命令长度为22字节，后接命令host:uninstall:com.example.app |
| adb tcpip                             | 设置设备监听TCP/IP连接    | host:tcpip:<port>                                            | `000e host:tcpip:5555`                                       | 000e表示命令长度为14字节，后接命令host:tcpip:5555            |
| adb connect                           | 连接设备                  | host:connect:\<device\_ip>:<port>                            | `0016 host:connect:192.168.1.5:5555`                         | 0016表示命令长度为22字节，后接命令host:connect:192.168.1.5:5555 |
| adb disconnect                        | 断开设备连接              | host:disconnect:\<device\_ip>:<port>                         | `0018 host:disconnect:192.168.1.5:5555`                      | 0018表示命令长度为24字节，后接命令host:disconnect:192.168.1.5:5555 |
| adb monitor                           | 监听设备事件              | host:monitor                                                 | `000e host:monitor`                                          | 000e表示命令长度为14字节，后接命令host:monitor               |
| adb events                            | 监听设备事件              | shell:getevent                                               | `000c shell:getevent`                                        | 000c表示命令长度为12字节，后接命令shell:getevent             |
| adb track-devices                     | 监听设备连接状态          | host:track-devices                                           | `0014 host:track-devices`                                    | 0014表示命令长度为20字节，后接命令host:track-devices         |
| adb start-server                      | 启动ADB服务               | host:start-server                                            | `0010 host:start-server`                                     | 0010表示命令长度为16字节，后接命令host:start-server          |
| adb shell screencap                   | 截图并保存到设备          | shell:screencap -p /sdcard/screenshot.png                    | `0024 shell:screencap -p /sdcard/screenshot.png`             | 0024表示命令长度为36字节，后接完整命令                       |
| adb shell pm get-package-info         | 查看指定应用的详细信息    | shell:pm get-package-info \<package\_name>                   | `0020 shell:pm get-package-info com.example.myapp`           | 0020表示命令长度为32字节，后接完整命令                       |
| adb shell am force-stop               | 强制停止应用              | shell:am force-stop \<package\_name>                         | `001e shell:am force-stop com.example.yourapp`               | 001e表示命令长度为30字节，后接完整命令                       |
| adb install -s                        | 安装应用到SD卡            | host:track-install:-s:\<path\_to\_apk>                       | `0022 host:track-install:-s:/path/to/app.apk`                | 0022表示命令长度为34字节，后接完整命令                       |
| adb shell pm get-install-location     | 查看应用安装位置          | shell:pm get-install-location                                | `001c shell:pm get-install-location`                         | 001c表示命令长度为28字节，后接命令                           |
| adb shell pm list packages            | 列出设备上所有应用包名    | shell:pm list packages                                       | `0016 shell:pm list packages`                                | 0016表示命令长度为22字节，后接命令                           |
| adb shell pm clear                    | 清除应用缓存              | shell:pm clear \<package\_name> --keep-data                  | `0022 shell:pm clear com.example.myapp --keep-data`          | 0022表示命令长度为34字节，后接完整命令                       |
| adb backup                            | 备份应用数据              | host:backup:\<backup\_file>:\<package\_name>                 | `0024 host:backup:/sdcard/backup.ab:com.example.yourapp`     | 0024表示命令长度为36字节，后接完整命令                       |
| adb restore                           | 恢复应用数据              | host:restore:\<backup\_file>                                 | `0016 host:restore:/sdcard/backup.ab`                        | 0016表示命令长度为22字节，后接命令                           |
| adb shell dumpsys package             | 查看应用权限              | shell:dumpsys package \<package\_name>                       | `0020 shell:dumpsys package com.example.yourapp`             | 0020表示命令长度为32字节，后接完整命令                       |
| adb shell am start                    | 启动指定Activity          | shell:am start -n \<package\_name>/\<activity\_name>         | `0028 shell:am start -n com.example.myapp/.MainActivity`     | 0028表示命令长度为40字节，后接完整命令                       |
| adb shell am force-stop               | 强制停止所有Activity      | shell:am force-stop \<package\_name>                         | `001e shell:am force-stop com.example.myapp`                 | 001e表示命令长度为30字节，后接完整命令                       |
| adb shell dumpsys activity top        | 获取前台Activity          | shell:dumpsys activity top                                   | `001c shell:dumpsys activity top`                            | 001c表示命令长度为28字节，后接命令                           |
| adb shell dumpsys activity activities | 获取前台所有Activity      | shell:dumpsys activity activities                            | `0020 shell:dumpsys activity activities`                     | 0020表示命令长度为32字节，后接命令                           |
| adb shell am broadcast                | 发送广播                  | shell:am broadcast -a \<action\_name>                        | `0022 shell:am broadcast -a android.intent.action.BOOT_COMPLETED` | 0022表示命令长度为34字节，后接完整命令                       |
| adb shell am startservice             | 启动Service               | shell:am startservice -n \<package\_name>/\<service\_name>   | `0028 shell:am startservice -n com.example.myapp/.MyService` | 0028表示命令长度为40字节，后接完整命令                       |
| adb shell am kill                     | 杀死进程                  | shell:am kill \<package\_name>                               | `0018 shell:am kill com.example.myapp`                       | 0018表示命令长度为24字节，后接命令                           |
| adb logcat                            | 查看设备日志              | shell:logcat                                                 | `000a shell:logcat`                                          | 000a表示命令长度为10字节，后接命令                           |
| adb logcat                            | 过滤日志                  | shell:logcat                                                 | `000a shell:logcat`，后续通过管道过滤                        | 000a表示命令长度为10字节，后接命令，过滤通过adb本地处理      |
| adb shell getprop                     | 查看设备属性              | shell:getprop                                                | `000c shell:getprop`                                         | 000c表示命令长度为12字节，后接命令                           |
| adb shell setprop                     | 设置设备属性              | shell:setprop \<property\_name> \<property\_value>           | `0022 shell:setprop debug.adb.wait-for-device 1`             | 0022表示命令长度为34字节，后接完整命令                       |
| adb shell wm density                  | 查看设备屏幕密度          | shell:wm density                                             | `0012 shell:wm density`                                      | 0012表示命令长度为18字节，后接命令                           |
| adb shell wm size                     | 查看设备屏幕分辨率        | shell:wm size                                                | `000e shell:wm size`                                         | 000e表示命令长度为14字节，后接命令                           |
| adb shell dumpsys battery             | 查看设备电池状态          | shell:dumpsys battery                                        | `0014 shell:dumpsys battery`                                 | 0014表示命令长度为20字节，后接命令                           |
| adb shell dumpsys meminfo             | 查看设备内存信息          | shell:dumpsys meminfo                                        | `0016 shell:dumpsys meminfo`                                 | 0016表示命令长度为22字节，后接命令                           |
| adb shell dumpsys cpuinfo             | 查看设备CPU信息           | shell:dumpsys cpuinfo                                        | `0016 shell:dumpsys cpuinfo`                                 | 0016表示命令长度为22字节，后接命令                           |
| adb shell dumpsys network             | 查看设备网络状态          | shell:dumpsys network                                        | `0016 shell:dumpsys network`                                 | 0016表示命令长度为22字节，后接命令                           |
| adb shell monkey                      | 随机事件模式              | shell:monkey \<event\_count>                                 | `0010 shell:monkey 100`                                      | 0010表示命令长度为16字节，后接命令shell:monkey 100           |
| adb shell monkey -p                   | 指定应用测试              | shell:monkey -p \<package\_name> \<event\_count>             | `0020 shell:monkey -p com.example.yourapp 100`               | 0020表示命令长度为32字节，后接完整命令                       |
| adb shell monkey -v                   | 日志输出                  | shell:monkey -p \<package\_name> -v -v -v \<event\_count>    | `002c shell:monkey -p com.example.yourapp -v -v -v 100`      | 002c表示命令长度为44字节，后接完整命令                       |
| adb shell monkey -s                   | 指定Seed值                | shell:monkey -s \<seed\_value> -p \<package\_name> -v -v -v \<event\_count> | `0030 shell:monkey -s 123 -p com.example.yourapp -v -v -v 100` | 0030表示命令长度为48字节，后接完整命令                       |
| adb shell monkey --throttle           | 指定操作间隔              | shell:monkey -p \<package\_name> --throttle \<throttle\_time> \<event\_count> | `002e shell:monkey -p com.example.yourapp --throttle 1000 200` | 002e表示命令长度为46字节，后接完整命令                       |
| adb shell monkey --ignore-crashes     | 忽略崩溃和超时            | shell:monkey --ignore-crashes --ignore-timeouts -p \<package\_name> \<event\_count> | `0032 shell:monkey --ignore-crashes --ignore-timeouts -p com.example.yourapp 500` | 0032表示命令长度为50字节，后接完整命令                       |
| adb shell monkey --pct-touch          | 指定事件类型比例          | shell:monkey --pct-touch \<touch\_percent> --pct-motion \<motion\_percent> -p \<package\_name> \<event\_count> | `0034 shell:monkey --pct-touch 50 --pct-motion 50 -p com.example.yourapp 1000` | 0034表示命令长度为52字节，后接完整命令                       |