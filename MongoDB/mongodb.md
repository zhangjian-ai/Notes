# 环境搭建

## 1.1. 配置docker-compose.yml

mongod.conf内容如下，一般只需要修改`wiredTiger.engineConfig.cacheSizeGB`，具体大小请查考官方文档。

```yaml
# mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# Where and how to store data.
storage:
  dbPath: /data/db
  journal:
    enabled: true
  directoryPerDB: true
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 8
      directoryForIndexes: true

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

# network interfaces
net:
  port: 27017
  bindIp: 0.0.0.0

# how the process runs
processManagement:
  timeZoneInfo: /usr/share/zoneinfo

#replication:
#replication:
#   oplogSizeMB: 51200
#   replSetName: rs0
   
security:
  authorization: enabled
```

创建文件夹用来持久化数据

```bash
# db存放数据库文件，log存放mongodb日志，config存放mongodb配置文件
mkdir db log config
# 由于log文件夹需要被容器读写，所以要授权
chmod 777 -R log
```

目前是副本集模式，需要拷贝该文件，修改其中`container_name`, `ports`和`volumes`

```yaml
version: '3.8'

services:
  mongo:
    image: mongo
    container_name: mongo1
    restart: always
    command: --config /etc/mongo/mongod.conf
    ports:
      - 27001:27017
    volumes:
      # 挂载数据目录
      - /home/docker-compose/mongo1/db:/data/db
      # 挂载日志目录
      - /home/docker-compose/mongo1/log:/var/log/mongodb
      # 挂载配置目录
      - /home/docker-compose/mongo1/config:/etc/mongo
```



## 1.2. 启动程序

mongodb部署在`172.17.0.3:/home/docker-compose`

```bash
# 程序后台启动
docker-compose up -d
```



## 1.3. 配置副本集

使用mongo连接服务器

```bash
./mongo --port 27017
```

进入mongodb后，使用命令设置副本集成员
 `_id`也就是副本集名称在**mongod.conf**指定了

```js
rs.initiate( {
   _id : "rs0",
   members: [
      { _id: 0, host: "172.17.0.3:27001" },
      { _id: 1, host: "172.17.0.3:27002" },
      { _id: 2, host: "172.17.0.3:27003", arbiterOnly: true }
   ]
})
// 查看目前节点的属性，一般为PRIMARY，SECONDARY和ARBITER三种
rs.status()
```



## 1.4. 开启用户权限配置

### 1.4.1. 创建用户

> 1. 数据库用户角色：read、readWrite;
> 2. 数据库管理角色：dbAdmin、dbOwner、userAdmin；
> 3. 集群管理角色：clusterAdmin、clusterManager、clusterMonitor、hostManager；
> 4. 备份恢复角色：backup、restore；
> 5. 所有数据库角色：readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase
> 6. 超级用户角色：root
> 7. // 这里还有几个角色间接或直接提供了系统超级用户的访问（dbOwner 、userAdmin、userAdminAnyDatabase）
> 8. 内部角色：__system

```bash
./mongo --port 27001
# 切换到admin数据库，做授权
use admin
# 查看内建的角色
show roles

# 创建角色
db.createUser({user:"xz_test", pwd: "admin#123", roles: [{role: "root", db: "admin"}]})

# 修改角色权限
db.updateUser("xz_test", { roles: [ {role: "readWrite", db: "autotest"}]})
```



### 1.4.2. 停止节点

使用`docker-compose stop`命令依次停止从节点mongo2，仲裁节点mongo3，主节点mongo1



### 1.4.3. 创建节点间认证文件

根据官方文档所述，副本集和分片集群间的节点之间需要认证。

> Replica sets and sharded clusters require internal authentication between members when access control is enabled.
>  For more details, please see Internal/Membership Authentication.

```bash
# 使用openssl在当前目录生成keyfile
openssl rand -base64 756 > keyfile
# 因为该文件是root用户创建，所以要变更用户为mongodb用户systemd-coredump和读权限
# 如果权限过大，mongodb启动后会报错permissions on XXXX are too open
chmod 400 keyfile
chown systemd-coredump keyfile
# 将该文件拷贝到其他mongodb节点上
cp keyfile /home/docker-compose/mongo1/config/
cp keyfile /home/docker-compose/mongo2/config/
cp keyfile /home/docker-compose/mongo3/config/
```



### 1.4.4. 修改mongod.conf配置

添加以下内容

```yaml
security:
  keyFile: /etc/mongo/keyfile
  authorization: enabled
```



### 1.4.5. 重新启动副本集

使用`docker-compose start`命令依次启动主节点mongo1，仲裁节点mongo3和从节点mongo2



## 1.5. 停止程序

```bash
# 停止容器并删除容器
docker-compose down
```



## 1.6. 升级程序

```bash
# 停止程序并删除镜像
docker-compose down --rmi all
# 拉取新的镜像
docker-compose pull
# 启动程序
docker-compose up -d
```



## 1.7. 卸载程序

要想完全卸载，需要删除docker镜像和数据

```bash
# 停止容器并删除容器、镜像
docker-compose down --rmi all
# 删除镜像
docker rmi mongo
# 删除本地文件
rm -r /home/docker-compose/mongo1
```

