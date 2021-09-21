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
