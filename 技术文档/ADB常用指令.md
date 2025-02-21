### 基础命令

#### 1. 查看 ADB 版本及安装路径

- **命令**：`adb version`
- **含义**：查看 ADB 的版本信息及安装路径。
- **示例**：`adb version`，成功执行后会显示 ADB 的版本号及安装路径等信息，如 `Android Debug Bridge version 1.0.41`。

#### 2. 查看已连接设备

- **命令**：`adb devices`
- **含义**：查看当前已连接到计算机的 Android 设备。
- **示例**：`adb devices`，执行后会列出已连接的设备，如 `List of devices attached` 下方显示设备的序列号。

#### 3. 启动/关闭 ADB 服务

- **启动服务**：`adb start-server`
- **关闭服务**：`adb kill-server`
- **含义**：分别用于启动和关闭 ADB 服务。
- **示例**：`adb start-server` 用于启动 ADB 服务，`adb kill-server` 用于关闭 ADB 服务。

#### 4. 截图

- **命令**：`adb shell screencap -p /sdcard/screenshot.png`，然后使用 `adb pull /sdcard/screenshot.png` 将截图文件从设备中拉取到本地。
- **含义**：通过 ADB 命令实现对设备屏幕的截图，并将截图文件保存到指定位置。
- **示例**：执行上述命令后，设备的屏幕截图会被保存到设备的 `/sdcard/` 目录下，并可通过 `adb pull` 命令将截图文件拉取到本地指定目录。

#### 5. 文件传输

- **从设备复制文件到本地**：`adb pull <remote> <local>`
- **将本地文件复制到设备**：`adb push <local> <remote>`
- **含义**：`adb pull` 命令用于将设备中的文件复制到本地计算机，`adb push` 命令用于将本地计算机的文件复制到设备中。
- **示例**：`adb pull /sdcard/yourfile.txt /path/to/local/directory/` 将设备中的 `yourfile.txt` 文件复制到本地的 `/path/to/local/directory/` 目录下；`adb push /path/to/local/file.txt /sdcard/` 将本地的 `file.txt` 文件复制到设备的 `/sdcard/` 目录下。

#### 6. 安装 APK

- **命令**：`adb install <apk_path>`
- **含义**：在设备上安装指定路径的 APK 文件。
- **示例**：`adb install -r -t -d xxx/yyy.apk`，其中 `-r` 表示覆盖安装，保留数据，`-t` 允许安装测试 APK，即开发常常用到的 debug 版本，`-d` 允许版本降级安装，即要安装的版本低于手机里的应用版本。

### ADB Shell 工具命令

#### 1. 查看设备信息

- **命令**：`adb shell pm get-package-info <package_name>`
- **含义**：查看指定应用的详细信息，包括其安装位置、权限等。
- **示例**：`adb shell pm get-package-info com.example.myapp | grep dataDir`，可查看指定应用的数据目录路径。

#### 2. 强制停止应用

- **命令**：`adb shell am force-stop <package_name>`
- **含义**：强制停止指定应用的运行。
- **示例**：`adb shell am force-stop com.example.yourapp`，用于强制停止 `com.example.yourapp` 应用的运行。

#### 3. 安装应用到 SD 卡

- **命令**：`adb install -r -s <path_to_apk>`
- **含义**：将 APK 文件强制安装到设备的 SD 卡上。
- **示例**：`adb install -r -s /path/to/your/app.apk`，将 `/path/to/your/app.apk` 安装到设备的 SD 卡上。

#### 4. 查看应用安装位置

- **命令**：`adb shell pm get-install-location | grep -w [internal|external]`
- **含义**：检查应用是安装在内部存储还是外部存储。
- **示例**：`adb shell pm get-install-location | grep -w [internal|external]`，通过该命令可查看应用的安装位置是在内部存储还是外部存储。

#### 5. 查询应用包名列表

- **命令**：`adb shell pm list packages`
- **含义**：列出设备上安装的所有应用的包名。
- **示例**：`adb shell pm list packages`，执行后会列出设备上所有已安装应用的包名。

#### 6. 清除应用缓存

- **命令**：`adb shell pm clear <package_name> --keep-data`
- **含义**：清除指定应用的缓存，但保留其数据。
- **示例**：`adb shell pm clear <package_name> --keep-data`，用于清除指定应用的缓存，但保留其数据。

#### 7. 备份应用数据

- **命令**：`adb backup -f <backup_file> <package_name>`
- **含义**：备份指定应用的数据。
- **示例**：`adb backup -f /sdcard/backup.ab com.example.yourapp`，将 `com.example.yourapp` 应用的数据备份到 `/sdcard/backup.ab` 文件中。

#### 8. 恢复应用数据

- **命令**：`adb restore <backup_file>`
- **含义**：从备份文件中恢复应用数据。
- **示例**：`adb restore /sdcard/backup.ab`，从 `/sdcard/backup.ab` 备份文件中恢复应用数据。

#### 9. 查看应用权限

- **命令**：`adb shell dumpsys package <package_name> | grep -A 10 "requested permissions"`
- **含义**：显示指定应用请求的权限列表。
- **示例**：`adb shell dumpsys package <package_name> | grep -A 10 "requested permissions"`，通过该命令可查看指定应用请求的权限列表。

#### 10. 启动 Activity

- **命令**：`adb shell am start -n <package_name>/<activity_name>`
- **含义**：启动指定应用的 Activity。
- **示例**：`adb shell am start -n com.example.myapp/.MainActivity`，启动 `com.example.myapp` 应用的 `MainActivity`。

#### 11. 停止 Activity

- **命令**：`adb shell am force-stop <package_name>`
- **含义**：强制停止指定应用的所有 Activity。
- **示例**：`adb shell am force-stop com.example.myapp`，强制停止 `com.example.myapp` 应用的所有 Activity。

#### 12. 获取当前前台 Activity

- **命令**：`adb shell dumpsys activity top`
- **含义**：获取当前设备上运行的前台 Activity。
- **示例**：`adb shell dumpsys activity top`，执行后会显示当前设备上运行的前台 Activity。

#### 13. 获取当前前台所有 Activity

- **命令**：`adb shell dumpsys activity activities | grep mResumedActivity`
- **含义**：获取当前设备上运行的前台 Activity。
- **示例**：`adb shell dumpsys activity activities | grep mResumedActivity`，执行后会显示当前设备上运行的前台 Activity。

#### 14. 发送广播

- **命令**：`adb shell am broadcast -a <action_name>`
- **含义**：发送指定的广播。
- **示例**：`adb shell am broadcast -a android.intent.action.BOOT_COMPLETED`，发送设备启动完成的广播。

#### 15. 启动 Service

- **命令**：`adb shell am startservice -n <package_name>/<service_name>`
- **含义**：启动指定应用的 Service。
- **示例**：`adb shell am startservice -n com.example.myapp/.MyService`，启动 `com.example.myapp` 应用的 `MyService`。

#### 16. 杀死进程

- **命令**：`adb shell am kill <package_name>`
- **含义**：杀死指定应用的所有进程。
- **示例**：`adb shell am kill com.example.myapp`，杀死 `com.example.myapp` 应用的所有进程。

### ADB Monkey 工具命令

#### 1. 随机事件模式

- **命令**：`adb shell monkey <event_count>`
- **含义**：让 Monkey 在设备上执行指定次数的随机事件，用于测试应用的稳定性。
- **示例**：`adb shell monkey 100`，让 Monkey 在设备上执行 100 次随机事件。

#### 2. 指定应用测试

- **命令**：`adb shell monkey -p <package_name> <event_count>`
- **含义**：让 Monkey 仅针对指定应用执行随机事件测试。
- **示例**：`adb shell monkey -p com.example.yourapp 100`，让 Monkey 仅针对 `com.example.yourapp` 应用执行 100 次随机事件。

#### 3. 日志输出

- **命令**：`adb shell monkey -p <package_name> -v -v -v <event_count> > <log_file_path>`
- **含义**：在执行 Monkey 测试时，将详细的日志信息输出到指定文件中，便于后续分析。其中 `-v` 参数用于提高日志级别，最高可加三个 `-v`，表示最详细的日志信息。
- **示例**：`adb shell monkey -p com.example.yourapp -v -v -v 100 > D:\\log.txt`，将 Monkey 测试的详细日志输出到 `D:\\log.txt` 文件中。

#### 4. 指定 Seed 值

- **命令**：`adb shell monkey -s <seed_value> -p <package_name> -v -v -v <event_count> > <log_file_path>`
- **含义**：通过指定 Seed 值，使 Monkey 的随机事件序列可重复，便于复现问题。`<seed_value>` 是一个整数，用于初始化随机数生成器。
- **示例**：`adb shell monkey -s 123 -p com.example.yourapp -v -v -v 100 > D:\\log.txt`，指定 Seed 值为 123，执行 Monkey 测试并将日志输出到 `D:\\log.txt` 文件中。

#### 5. 指定操作间隔

- **命令**：`adb shell monkey -p <package_name> --throttle <throttle_time> <event_count> > <log_file_path>`
- **含义**：设置 Monkey 执行事件之间的间隔时间，单位为毫秒。
- **示例**：`adb shell monkey -p com.example.yourapp --throttle 1000 200 > D:\\log.txt`，设置 Monkey 执行事件之间的间隔时间为 1000 毫秒，执行 200 次随机事件，并将日志输出到 `D:\\log.txt` 文件中。

#### 6. 忽略崩溃和超时

- **命令**：`adb shell monkey --ignore-crashes --ignore-timeouts -p <package_name> <event_count>`
- **含义**：在 Monkey 测试过程中，忽略应用的崩溃和超时情况，继续执行测试。
- **示例**：`adb shell monkey --ignore-crashes --ignore-timeouts -p com.example.yourapp 500`，在 Monkey 测试过程中忽略应用的崩溃和超时情况，继续执行 500 次随机事件。

#### 7. 指定事件类型比例

- **命令**：`adb shell monkey --pct-touch <touch_percent> --pct-motion <motion_percent> -p <package_name> <event_count>`
- **含义**：设置 Monkey 测试中不同类型事件的比例，如触摸事件和动作事件的比例。
- **示例**：`adb shell monkey --pct-touch 50 --pct-motion 50 -p com.example.yourapp 1000`，设置触摸事件和动作事件各占 50% 的比例，执行 1000 次随机事件。

### 其他常用命令

#### 1. 查看日志

- **命令**：`adb logcat`
- **含义**：查看设备的日志输出，可帮助开发者调试应用。
- **示例**：`adb logcat`，执行后会显示设备的日志信息，可通过过滤等方式查看特定的日志内容。

#### 2. 过滤日志

- **命令**：`adb logcat | grep <keyword>`
- **含义**：通过关键字过滤日志信息，便于快速定位问题。
- **示例**：`adb logcat | grep "Error"`，过滤出包含 "Error" 关键字的日志信息。

#### 3. 查看设备属性

- **命令**：`adb shell getprop`
- **含义**：查看设备的系统属性信息。
- **示例**：`adb shell getprop`，执行后会列出设备的各种系统属性，如设备型号、Android 版本等。

#### 4. 设置设备属性

- **命令**：`adb shell setprop <property_name> <property_value>`
- **含义**：设置设备的系统属性。
- **示例**：`adb shell setprop debug.adb.wait-for-device 1`，设置设备的 `debug.adb.wait-for-device` 属性为 1。

#### 5. 查看设备屏幕密度

- **命令**：`adb shell wm density`
- **含义**：查看设备的屏幕密度。
- **示例**：`adb shell wm density`，执行后会显示设备的屏幕密度值，如 `Physical density: 480`。

#### 6. 查看设备屏幕分辨率

- **命令**：`adb shell wm size`
- **含义**：查看设备的屏幕分辨率。
- **示例**：`adb shell wm size`，执行后会显示设备的屏幕分辨率，如 `Physical size: 1080x1920`。

#### 7. 查看设备电池状态

- **命令**：`adb shell dumpsys battery`
- **含义**：查看设备的电池状态信息。
- **示例**：`adb shell dumpsys battery`，执行后会显示设备的电池状态，如电量百分比、充电状态等。

#### 8. 查看设备内存信息

- **命令**：`adb shell dumpsys meminfo`
- **含义**：查看设备的内存使用情况。
- **示例**：`adb shell dumpsys meminfo`，执行后会显示设备的内存信息，如总内存、可用内存等。

#### 9. 查看设备 CPU 信息

- **命令**：`adb shell dumpsys cpuinfo`
- **含义**：查看设备的 CPU 使用情况。
- **示例**：`adb shell dumpsys cpuinfo`，执行后会显示设备的 CPU 信息，如 CPU 核心数、CPU 使用率等。

#### 10. 查看设备网络状态

- **命令**：`adb shell dumpsys network`
- **含义**：查看设备的网络连接状态。
- **示例**：`adb shell dumpsys network`，执行后会显示设备的网络状态信息，如网络类型、网络连接状态等。

### 部分参数解释

#### 1. `-v` 参数

- **含义**：提高日志级别，用于显示更详细的日志信息。在 Monkey 测试中，最高可加三个 `-v`，表示最详细的日志信息。

#### 2. `-p` 参数

- **含义**：指定包名，用于指定 Monkey 测试的目标应用。

#### 3. `-s` 参数

- **含义**：指定设备序列号，用于在有多个设备连接时，指定要操作的设备。

#### 4. `-r` 参数

- **含义**：覆盖安装，保留数据。在安装 APK 时，如果应用已存在，使用 `-r` 参数可以覆盖安装，同时保留应用的数据。

#### 5. `-t` 参数

- **含义**：允许安装测试 APK，即开发常常用到的 debug 版本。

#### 6. `-d` 参数

- **含义**：允许版本降级安装，即要安装的版本低于手机里的应用版本。

#### 7. `--throttle` 参数

- **含义**：设置 Monkey 执行事件之间的间隔时间，单位为毫秒。

#### 8. `--ignore-crashes` 参数

- **含义**：在 Monkey 测试过程中，忽略应用的崩溃情况，继续执行测试。

#### 9. `--ignore-timeouts` 参数

- **含义**：在 Monkey 测试过程中，忽略应用的超时情况，继续执行测试。

#### 10. `--pct-touch` 参数

- **含义**：设置 Monkey 测试中触摸事件的比例。

#### 11. `--pct-motion` 参数

- **含义**：设置 Monkey 测试中动作事件的比例。