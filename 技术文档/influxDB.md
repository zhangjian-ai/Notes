# influxDB 基础概念

Influxdb 是一个时间序列数据库。

influxdb里面有一些重要概念：database，timestamp，field key， field value， field set，tag key，tag value，tag set，measurement， retention policy ，series，point。结合下面的例子数据来说明这几个概念：

```
name: census
-————————————
time                     butterflies     honeybees     location   scientist
2015-08-18T00:00:00Z      12                23           1         langstroth
2015-08-18T00:00:00Z      1                 30           1         perpetua
2015-08-18T00:06:00Z      11                28           1         langstroth
2015-08-18T00:06:00Z      3                 28           1         perpetua
2015-08-18T05:54:00Z      2                 11           2         langstroth
2015-08-18T06:00:00Z      1                 10           2         langstroth
2015-08-18T06:06:00Z      8                 23           2         perpetua
2015-08-18T06:12:00Z      7                 22           2         perpetua
```

## timestamp

既然是时间序列数据库，influxdb的数据都有一列名为time的列，里面存储UTC时间戳。



## field key，field value，field set

butterflies和honeybees两列数据称为字段(fields)，influxdb的字段由field key和field value组成。其中butterflies和honeybees为field key，它们为string类型，用于存储元数据。

而butterflies这一列的数据12-7为butterflies的field value，同理，honeybees这一列的23-22为honeybees的field value。field value可以为string，float，integer或boolean类型。field value通常都是与时间关联的。

field key和field value对组成的集合称之为field set。如下：

```
butterflies = 12 honeybees = 23
butterflies = 1 honeybees = 30
butterflies = 11 honeybees = 28
butterflies = 3 honeybees = 28
butterflies = 2 honeybees = 11
butterflies = 1 honeybees = 10
butterflies = 8 honeybees = 23
butterflies = 7 honeybees = 22
```

**在influxdb中，字段必须存在。注意，字段是没有索引的。如果使用字段作为查询条件，会扫描符合查询条件的所有字段值，性能不及tag。类比一下，fields相当于SQL的没有索引的列。**



## tag key，tag value，tag set

location和scientist这两列称为标签(tags)，标签由tag key和tag value组成。location这个tag key有两个tag value：1和2，scientist有两个tag value：langstroth和perpetua。tag key和tag value对组成了tag set，示例中的tag set如下：

```
location = 1, scientist = langstroth
location = 2, scientist = langstroth
location = 1, scientist = perpetua
location = 2, scientist = perpetua
```

**tags是可选的，但是强烈建议你用上它，因为tag是有索引的，tags相当于SQL中的有索引的列。tag value只能是string类型** 如果你的常用场景是根据butterflies和honeybees来查询，那么你可以将这两个列设置为tag，而其他两列设置为field，tag和field依据具体查询需求来定。



## measurement

measurement是fields，tags以及time列的容器，measurement的名字用于描述存储在其中的字段数据，类似mysql的表名。如上面例子中的measurement为census。measurement相当于SQL中的表，本文中我在部分地方会用表来指代measurement。



## retention policy

retention policy指数据保留策略，示例数据中的retention policy为默认的autogen。它表示数据一直保留永不过期，副本数量为1。你也可以指定数据的保留时间，如30天。



## series

series是共享同一个retention policy，measurement以及tag set的数据集合。示例中数据有4个series，如下:

| Arbitrary series number | Retention policy | Measurement | Tag set                             |
| ----------------------- | ---------------- | ----------- | ----------------------------------- |
| series 1                | autogen          | census      | location = 1,scientist = langstroth |
| series 2                | autogen          | census      | location = 2,scientist = langstroth |
| series 3                | autogen          | census      | location = 1,scientist = perpetua   |
| series 4                | autogen          | census      | location = 2,scientist = perpetua   |



## point

point则是同一个series中具有相同时间的field set，points相当于SQL中的数据行。如下面就是一个point：

```
name: census
-----------------
time                  butterflies    honeybees   location    scientist
2015-08-18T00:00:00Z       1            30           1        perpetua
```



## database

上面提到的结构都存储在数据库中，示例的数据库为my_database。一个数据库可以有多个measurement，retention policy， continuous queries以及user。influxdb是一个无模式的数据库，可以很容易的添加新的measurement，tags，fields等。而它的操作却和传统的数据库一样，可以使用类SQL语言查询和修改数据。

influxdb不是一个完整的CRUD数据库，它更像是一个CR-ud数据库。它优先考虑的是增加和读取数据而不是更新和删除数据的性能，而且它阻止了某些更新和删除行为使得创建和读取数据更加高效。



# influxDB 基本语法

> 2.0.0 版本之前的基本操作语法

```shell
# 进入influx终端
influx

#创建用户
CREATE USER influx WITH PASSWORD 'influx' WITH ALL PRIVILEGES
#查看用户
SHOW USERS
#创建数据库
create database + name
drop database + name
#查看数据库
show databases
# 切换数据库
use database + name
# 查看表
# influxdb 不能直接创建表，只能通过插入数据时顺带创建
show measurements
drop measurement + name
# 插入数据
# Insert的时候如果没有带时间戳，InfluxDB会自动添加本地的当前时间作为它的时间戳。
# cpu表示 measurement，理解为数据库中的表；host 表示 tag，理解为索引列，可以有多个，也可以没有，为了提高查询效率，建议至少有一列。
INSERT cpu,host=192.168.1.1,load=0.1 usage=0.2
#查看数据
SELECT * FROM "cpu"
SELECT "host","load","usage" FROM "cpu" WHERE "host" = '192.168.1.1'
```





# influxDB 特色函数

influxdb函数分为聚合函数，选择函数，转换函数，预测函数等。除了与普通数据库一样提供了基本操作函数外，还提供了一些特色函数以方便数据统计计算，下面会一一介绍其中一些常用的特色函数。

- 聚合函数：`FILL()`, `INTEGRAL()`，`SPREAD()`， `STDDEV()`，`MEAN()` 求平均数, `MEDIAN()`等。
- 选择函数: `SAMPLE()`, `PERCENTILE()`, `FIRST()`, `LAST()`, `TOP()`, `BOTTOM()`等。
- 转换函数: `DERIVATIVE()`, `DIFFERENCE()`等。
- 预测函数：`HOLT_WINTERS()`。

先从官网导入测试数据（注：这里测试用的版本是1.3.1，最新版本是1.3.5）:



```dart
$ curl https://s3.amazonaws.com/noaa.water-database/NOAA_data.txt -o NOAA_data.txt
$ influx -import -path=NOAA_data.txt -precision=s -database=NOAA_water_database
$ influx -precision rfc3339 -database NOAA_water_database
Connected to http://localhost:8086 version 1.3.1
InfluxDB shell 1.3.1
> show measurements
name: measurements
name
----
average_temperature
distincts
h2o_feet
h2o_pH
h2o_quality
h2o_temperature

> show series from h2o_feet;
key
---
h2o_feet,location=coyote_creek
h2o_feet,location=santa_monica
```

下面的例子都以官方示例数据库来测试，这里只用部分数据以方便观察。measurement为`h2o_feet`，tag key为`location`，field key有`level description`和`water_level`两个。



```bash
> SELECT * FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z'
name: h2o_feet
time                 level description    location     water_level
----                 -----------------    --------     -----------
2015-08-18T00:00:00Z between 6 and 9 feet coyote_creek 8.12
2015-08-18T00:00:00Z below 3 feet         santa_monica 2.064
2015-08-18T00:06:00Z between 6 and 9 feet coyote_creek 8.005
2015-08-18T00:06:00Z below 3 feet         santa_monica 2.116
2015-08-18T00:12:00Z between 6 and 9 feet coyote_creek 7.887
2015-08-18T00:12:00Z below 3 feet         santa_monica 2.028
2015-08-18T00:18:00Z between 6 and 9 feet coyote_creek 7.762
2015-08-18T00:18:00Z below 3 feet         santa_monica 2.126
2015-08-18T00:24:00Z between 6 and 9 feet coyote_creek 7.635
2015-08-18T00:24:00Z below 3 feet         santa_monica 2.041
2015-08-18T00:30:00Z between 6 and 9 feet coyote_creek 7.5
2015-08-18T00:30:00Z below 3 feet         santa_monica 2.051
```



## GROUP BY，FILL()

如下语句中`GROUP BY time(12m),*` 表示以每12分钟和tag(location)分组(如果是`GROUP BY time(12m)`则表示仅每12分钟分组，**GROUP BY 参数只能是time和tag**)。然后fill(200)表示如果这个时间段没有数据，以200填充，mean(field_key)求该范围内数据的平均值(注意：这是依据series来计算。其他还有SUM求和，MEDIAN求中位数)。LIMIT 7表示限制返回的point(记录数)最多为7条，而SLIMIT 1则是限制返回的series为1个。

注意这里的时间区间，起始时间为整点前包含这个区间第一个12m的时间，比如这里为 `2015-08-17T:23:48:00Z`，第一条为 `2015-08-17T23:48:00Z <= t < 2015-08-18T00:00:00Z`这个区间的`location=coyote_creek`的`water_level`的平均值，这里没有数据，于是填充的200。第二条为 `2015-08-18T00:00:00Z <= t < 2015-08-18T00:12:00Z`区间的`location=coyote_creek`的`water_level`平均值，这里为 `（8.12+8.005）/ 2 = 8.0625`，其他以此类推。

而`GROUP BY time(10m)`则表示以10分钟分组，起始时间为包含这个区间的第一个10m的时间，即 `2015-08-17T23:40:00Z`。默认返回的是第一个series，如果要计算另外那个series，可以在SQL语句后面加上 `SOFFSET 1`。

那如果时间小于数据本身采集的时间间隔呢，比如`GROUP BY time(10s)`呢？这样的话，就会按10s取一个点，没有数值的为空或者FILL填充，对应时间点有数据则保持不变。



```csharp
## GROUP BY time(12m)
> SELECT mean("water_level") FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z' GROUP BY time(12m),* fill(200) LIMIT 7 SLIMIT 1
name: h2o_feet
tags: location=coyote_creek
time                 mean
----                 ----
2015-08-17T23:48:00Z 200
2015-08-18T00:00:00Z 8.0625
2015-08-18T00:12:00Z 7.8245
2015-08-18T00:24:00Z 7.5675

## GROUP BY time(10m)，SOFFSET设置为1
> SELECT mean("water_level") FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z' GROUP BY time(10m),* fill(200) LIMIT 7 SLIMIT 1 SOFFSET 1
name: h2o_feet
tags: location=santa_monica
time                 mean
----                 ----
2015-08-17T23:40:00Z 200
2015-08-17T23:50:00Z 200
2015-08-18T00:00:00Z 2.09
2015-08-18T00:10:00Z 2.077
2015-08-18T00:20:00Z 2.041
2015-08-18T00:30:00Z 2.051
```



## INTEGRAL(field_key, unit)

计算数值字段值覆盖的曲面的面积值并得到面积之和。测试数据如下：

```bash
> SELECT "water_level" FROM "h2o_feet" WHERE "location" = 'santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z'

name: h2o_feet
time                   water_level
----                   -----------
2015-08-18T00:00:00Z   2.064
2015-08-18T00:06:00Z   2.116
2015-08-18T00:12:00Z   2.028
2015-08-18T00:18:00Z   2.126
2015-08-18T00:24:00Z   2.041
2015-08-18T00:30:00Z   2.051
```

使用INTERGRAL计算面积。注意，这个面积就是这些点连接起来后与时间围成的不规则图形的面积，注意unit默认是以1秒计算，所以下面语句计算结果为`3732.66=2.028*1800+分割出来的梯形和三角形面积`。如果unit改为1分，则结果为`3732.66/60 = 62.211`。unit为2分，则结果为`3732.66/120 = 31.1055`。以此类推。

```bash
# unit为默认的1秒
> SELECT INTEGRAL("water_level") FROM "h2o_feet" WHERE "location" = 'santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z'
name: h2o_feet
time                 integral
----                 --------
1970-01-01T00:00:00Z 3732.66

# unit为1分
> SELECT INTEGRAL("water_level", 1m) FROM "h2o_feet" WHERE "location" = 'santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z'
name: h2o_feet
time                 integral
----                 --------
1970-01-01T00:00:00Z 62.211
```



## SPREAD(field_key)

计算数值字段的最大值和最小值的差值。

```csharp
> SELECT SPREAD("water_level") FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z' GROUP BY time(12m),* fill(18) LIMIT 3 SLIMIT 1 SOFFSET 1
name: h2o_feet
tags: location=santa_monica
time                 spread
----                 ------
2015-08-17T23:48:00Z 18
2015-08-18T00:00:00Z 0.052000000000000046
2015-08-18T00:12:00Z 0.09799999999999986
```



## STDDEV(field_key)

计算字段的标准差。influxdb用的是贝塞尔修正的标准差计算公式 ，如下：

- mean=(v1+v2+...+vn)/n;
- stddev = math.sqrt(((v1-mean)2 + (v2-mean)2 + ...+(vn-mean)2)/(n-1))

```csharp
> SELECT STDDEV("water_level") FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z' GROUP BY time(12m),* fill(18) SLIMIT 1;
name: h2o_feet
tags: location=coyote_creek
time                 stddev
----                 ------
2015-08-17T23:48:00Z 18
2015-08-18T00:00:00Z 0.08131727983645186
2015-08-18T00:12:00Z 0.08838834764831845
2015-08-18T00:24:00Z 0.09545941546018377
```



## PERCENTILE(field_key, N)

选取某个字段中大于N%的这个字段值。

如果一共有4条记录，N为10，则10%*4=0.4，四舍五入为0，则查询结果为空。N为20，则 20% * 4 = 0.8，四舍五入为1，选取的是4个数中最小的数。如果N为40，40% * 4 = 1.6，四舍五入为2，则选取的是4个数中第二小的数。由此可以看出N=100时，就跟`MAX(field_key)`是一样的，而当N=50时，与`MEDIAN(field_key)`在字段值为奇数个时是一样的。



```bash
> SELECT PERCENTILE("water_level",20) FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z' GROUP BY time(12m)
name: h2o_feet
time                 percentile
----                 ----------
2015-08-17T23:48:00Z 
2015-08-18T00:00:00Z 2.064
2015-08-18T00:12:00Z 2.028
2015-08-18T00:24:00Z 2.041

> SELECT PERCENTILE("water_level",40) FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z' GROUP BY time(12m)
name: h2o_feet
time                 percentile
----                 ----------
2015-08-17T23:48:00Z 
2015-08-18T00:00:00Z 2.116
2015-08-18T00:12:00Z 2.126
2015-08-18T00:24:00Z 2.051
```



## SAMPLE(field_key, N)

随机返回field key的N个值。如果语句中有`GROUP BY time()`，则每组数据随机返回N个值。

```csharp
> SELECT SAMPLE("water_level",2) FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z';
name: h2o_feet
time                 sample
----                 ------
2015-08-18T00:00:00Z 2.064
2015-08-18T00:12:00Z 2.028

> SELECT SAMPLE("water_level",2) FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z' GROUP BY time(12m);
name: h2o_feet
time                 sample
----                 ------
2015-08-18T00:06:00Z 2.116
2015-08-18T00:06:00Z 8.005
2015-08-18T00:12:00Z 7.887
2015-08-18T00:18:00Z 7.762
2015-08-18T00:24:00Z 7.635
2015-08-18T00:30:00Z 2.051
```



## CUMULATIVE_SUM(field_key)

计算字段值的递增和。

```bash
> SELECT CUMULATIVE_SUM("water_level") FROM "h2o_feet" WHERE time >= '2015-08-17T23:48:00Z' AND time <= '2015-08-18T00:30:00Z';
name: h2o_feet
time                 cumulative_sum
----                 --------------
2015-08-18T00:00:00Z 8.12
2015-08-18T00:00:00Z 10.184
2015-08-18T00:06:00Z 18.189
2015-08-18T00:06:00Z 20.305
2015-08-18T00:12:00Z 28.192
2015-08-18T00:12:00Z 30.22
2015-08-18T00:18:00Z 37.982
2015-08-18T00:18:00Z 40.108
2015-08-18T00:24:00Z 47.742999999999995
2015-08-18T00:24:00Z 49.78399999999999
2015-08-18T00:30:00Z 57.28399999999999
2015-08-18T00:30:00Z 59.334999999999994
```



## DERIVATIVE(field_key, unit) 和 NON_NEGATIVE_DERIVATIVE(field_key, unit)

计算字段值的变化比。unit默认为1s，即计算的是1秒内的变化比。

如下面的第一个数据计算方法是 `(2.116-2.064)/(6*60) = 0.00014..`，其他计算方式同理。虽然原始数据是6m收集一次，但是这里的变化比默认是按秒来计算的。如果要按6m计算，则设置unit为6m即可。

```bash
> SELECT DERIVATIVE("water_level") FROM "h2o_feet" WHERE "location" = 'santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z'
name: h2o_feet
time                 derivative
----                 ----------
2015-08-18T00:06:00Z 0.00014444444444444457
2015-08-18T00:12:00Z -0.00024444444444444465
2015-08-18T00:18:00Z 0.0002722222222222218
2015-08-18T00:24:00Z -0.000236111111111111
2015-08-18T00:30:00Z 0.00002777777777777842

> SELECT DERIVATIVE("water_level", 6m) FROM "h2o_feet" WHERE "location" = 'santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z'
name: h2o_feet
time                 derivative
----                 ----------
2015-08-18T00:06:00Z 0.052000000000000046
2015-08-18T00:12:00Z -0.08800000000000008
2015-08-18T00:18:00Z 0.09799999999999986
2015-08-18T00:24:00Z -0.08499999999999996
2015-08-18T00:30:00Z 0.010000000000000231
```

而DERIVATIVE结合GROUP BY time，以及mean可以构造更加复杂的查询，如下所示:

```csharp
> SELECT DERIVATIVE(mean("water_level"), 6m) FROM "h2o_feet" WHERE time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z' group by time(12m), *
name: h2o_feet
tags: location=coyote_creek
time                 derivative
----                 ----------
2015-08-18T00:12:00Z -0.11900000000000022
2015-08-18T00:24:00Z -0.12849999999999984

name: h2o_feet
tags: location=santa_monica
time                 derivative
----                 ----------
2015-08-18T00:12:00Z -0.00649999999999995
2015-08-18T00:24:00Z -0.015499999999999847
```

这个计算其实是先根据GROUP BY time求平均值，然后对这个平均值再做变化比的计算。因为数据是按12分钟分组的，而变化比的unit是6分钟，所以差值除以2(12/6)才得到变化比。如第一个值是 `(7.8245-8.0625)/2 = -0.1190`。

```csharp
> SELECT mean("water_level") FROM "h2o_feet" WHERE time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z' group by time(12m), *
name: h2o_feet
tags: location=coyote_creek
time                 mean
----                 ----
2015-08-18T00:00:00Z 8.0625
2015-08-18T00:12:00Z 7.8245
2015-08-18T00:24:00Z 7.5675

name: h2o_feet
tags: location=santa_monica
time                 mean
----                 ----
2015-08-18T00:00:00Z 2.09
2015-08-18T00:12:00Z 2.077
2015-08-18T00:24:00Z 2.0460000000000003
```

`NON_NEGATIVE_DERIVATIVE`与`DERIVATIVE`不同的是它只返回的是非负的变化比:

```csharp
> SELECT DERIVATIVE(mean("water_level"), 6m) FROM "h2o_feet" WHERE location='santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z' group by time(6m), *
name: h2o_feet
tags: location=santa_monica
time                 derivative
----                 ----------
2015-08-18T00:06:00Z 0.052000000000000046
2015-08-18T00:12:00Z -0.08800000000000008
2015-08-18T00:18:00Z 0.09799999999999986
2015-08-18T00:24:00Z -0.08499999999999996
2015-08-18T00:30:00Z 0.010000000000000231

> SELECT NON_NEGATIVE_DERIVATIVE(mean("water_level"), 6m) FROM "h2o_feet" WHERE location='santa_monica' AND time >= '2015-08-18T00:00:00Z' AND time <= '2015-08-18T00:30:00Z' group by time(6m), *
name: h2o_feet
tags: location=santa_monica
time                 non_negative_derivative
----                 -----------------------
2015-08-18T00:06:00Z 0.052000000000000046
2015-08-18T00:18:00Z 0.09799999999999986
2015-08-18T00:30:00Z 0.010000000000000231
```



# influxDB 连续查询

## 基本语法

连续查询(CONTINUOUS QUERY，简写为CQ)是指定时自动在实时数据上进行的InfluxQL查询，查询结果可以存储到指定的measurement中。基本语法格式如下：

```xml
CREATE CONTINUOUS QUERY <cq_name> ON <database_name>
BEGIN
  <cq_query>
END

cq_query格式：
SELECT <function[s]> INTO <destination_measurement> FROM <measurement> [WHERE <stuff>] GROUP BY time(<interval>)[,<tag_key[s]>]
```

CQ操作的是实时数据，它使用本地服务器的时间戳、GROUP BY time()时间间隔以及InfluxDB预先设置好的时间范围来确定什么时候开始查询以及查询覆盖的时间范围。注意CQ语句里面的WHERE条件是没有时间范围的，因为CQ会根据`GROUP BY time()`自动确定时间范围。

CQ执行的时间间隔和`GROUP BY time()`的时间间隔一样，它在InfluxDB预先设置的时间范围的起始时刻执行。如果`GROUP BY time(1h)`，则单次查询的时间范围为 `now()-GROUP BY time(1h)`到 `now()`，也就是说，如果当前时间为17点，这次查询的时间范围为 16:00到16:59.99999。

下面看几个示例，示例数据如下，这是数据库`transportation`中名为`bus_data`的measurement，每15分钟统计一次乘客数和投诉数。数据文件`bus_data.txt`如下：

```bash
# DDL
CREATE DATABASE transportation

# DML
# CONTEXT-DATABASE: transportation 

bus_data,complaints=9 passengers=5 1472367600
bus_data,complaints=9 passengers=8 1472368500
bus_data,complaints=9 passengers=8 1472369400
bus_data,complaints=9 passengers=7 1472370300
bus_data,complaints=9 passengers=8 1472371200
bus_data,complaints=7 passengers=15 1472372100
bus_data,complaints=7 passengers=15 1472373000
bus_data,complaints=7 passengers=17 1472373900
bus_data,complaints=7 passengers=20 1472374800
```

导入数据，命令如下：



```csharp
root@f216e9be15bf:/# influx -import -path=bus_data.txt -precision=s
root@f216e9be15bf:/# influx -precision=rfc3339 -database=transportation
Connected to http://localhost:8086 version 1.3.5
InfluxDB shell version: 1.3.5
> select * from bus_data
name: bus_data
time                 complaints passengers
----                 ---------- ----------
2016-08-28T07:00:00Z 9          5
2016-08-28T07:15:00Z 9          8
2016-08-28T07:30:00Z 9          8
2016-08-28T07:45:00Z 9          7
2016-08-28T08:00:00Z 9          8
2016-08-28T08:15:00Z 7          15
2016-08-28T08:30:00Z 7          15
2016-08-28T08:45:00Z 7          17
2016-08-28T09:00:00Z 7          20
```

### 示例1 自动缩小取样存储到新的measurement中

对单个字段自动缩小取样并存储到新的measurement中。



```ruby
CREATE CONTINUOUS QUERY "cq_basic" ON "transportation"
BEGIN
  SELECT mean("passengers") INTO "average_passengers" FROM "bus_data" GROUP BY time(1h)
END
```

这个CQ的意思就是对`bus_data`每小时自动计算取样数据的平均乘客数并存储到 `average_passengers`中。那么在2016-08-28这天早上会执行如下流程：



```bash
At 8:00 cq_basic 执行查询，查询时间范围 time >= '7:00' AND time < '08:00'.
cq_basic写入一条记录到 average_passengers:
name: average_passengers
------------------------
time                   mean
2016-08-28T07:00:00Z   7
At 9:00 cq_basic 执行查询，查询时间范围 time >= '8:00' AND time < '9:00'.
cq_basic写入一条记录到 average_passengers:
name: average_passengers
------------------------
time                   mean
2016-08-28T08:00:00Z   13.75

# Results
> SELECT * FROM "average_passengers"
name: average_passengers
------------------------
time                   mean
2016-08-28T07:00:00Z   7
2016-08-28T08:00:00Z   13.75
```

### 示例2 自动缩小取样并存储到新的保留策略（Retention Policy）中



```ruby
CREATE CONTINUOUS QUERY "cq_basic_rp" ON "transportation"
BEGIN
  SELECT mean("passengers") INTO "transportation"."three_weeks"."average_passengers" FROM "bus_data" GROUP BY time(1h)
END
```

与示例1类似，不同的是保留的策略不是`autogen`，而是改成了`three_weeks`(创建保留策略语法 `CREATE RETENTION POLICY "three_weeks" ON "transportation" DURATION 3w REPLICATION 1`)。



```css
> SELECT * FROM "transportation"."three_weeks"."average_passengers"
name: average_passengers
------------------------
time                   mean
2016-08-28T07:00:00Z   7
2016-08-28T08:00:00Z   13.75
```

### 示例3 使用后向引用(backreferencing)自动缩小取样并存储到新的数据库中



```bash
CREATE CONTINUOUS QUERY "cq_basic_br" ON "transportation"
BEGIN
  SELECT mean(*) INTO "downsampled_transportation"."autogen".:MEASUREMENT FROM /.*/ GROUP BY time(30m),*
END
```

使用后向引用语法自动缩小取样并存储到新的数据库中。语法 `:MEASUREMENT` 用来指代后面的表，而 `/.*/`则是分别查询所有的表。这句CQ的含义就是每30分钟自动查询`transportation`的所有表(这里只有bus_data一个表)，并将30分钟内数字字段(passengers和complaints)求平均值存储到新的数据库 `downsampled_transportation`中。

最终结果如下：



```css
> SELECT * FROM "downsampled_transportation."autogen"."bus_data"
name: bus_data
--------------
time                   mean_complaints   mean_passengers
2016-08-28T07:00:00Z   9                 6.5
2016-08-28T07:30:00Z   9                 7.5
2016-08-28T08:00:00Z   8                 11.5
2016-08-28T08:30:00Z   7                 16
```

### 示例4 自动缩小取样以及配置CQ的时间范围



```ruby
CREATE CONTINUOUS QUERY "cq_basic_offset" ON "transportation"
BEGIN
  SELECT mean("passengers") INTO "average_passengers" FROM "bus_data" GROUP BY time(1h,15m)
END
```

与前面几个示例不同的是，这里的`GROUP BY time(1h, 15m)`指定了一个时间偏移，也就是说 `cq_basic_offset`执行的时间不再是整点，而是往后偏移15分钟。执行流程如下:



```bash
At 8:15 cq_basic_offset 执行查询的时间范围 time >= '7:15' AND time < '8:15'.
name: average_passengers
------------------------
time                   mean
2016-08-28T07:15:00Z   7.75
At 9:15 cq_basic_offset 执行查询的时间范围 time >= '8:15' AND time < '9:15'.
name: average_passengers
------------------------
time                   mean
2016-08-28T08:15:00Z   16.75
```

最终结果:



```css
> SELECT * FROM "average_passengers"
name: average_passengers
------------------------
time                   mean
2016-08-28T07:15:00Z   7.75
2016-08-28T08:15:00Z   16.75
```

## 高级语法

InfluxDB连续查询的高级语法如下：



```xml
CREATE CONTINUOUS QUERY <cq_name> ON <database_name>
RESAMPLE EVERY <interval> FOR <interval>
BEGIN
  <cq_query>
END
```

与基本语法不同的是，多了`RESAMPLE`关键字。高级语法里CQ的执行时间和查询时间范围则与RESAMPLE里面的两个interval有关系。

高级语法中CQ以EVERY interval的时间间隔执行，执行时查询的时间范围则是FOR interval来确定。如果FOR interval为2h，当前时间为17:00，则查询的时间范围为`15:00-16:59.999999`。**RESAMPLE的EVERY和FOR两个关键字可以只有一个**。

示例的数据表如下，比之前的多了几条记录为了示例3和示例4的测试:



```css
name: bus_data
--------------
time                   passengers
2016-08-28T06:30:00Z   2
2016-08-28T06:45:00Z   4
2016-08-28T07:00:00Z   5
2016-08-28T07:15:00Z   8
2016-08-28T07:30:00Z   8
2016-08-28T07:45:00Z   7
2016-08-28T08:00:00Z   8
2016-08-28T08:15:00Z   15
2016-08-28T08:30:00Z   15
2016-08-28T08:45:00Z   17
2016-08-28T09:00:00Z   20
```

### 示例1 只配置执行时间间隔



```ruby
CREATE CONTINUOUS QUERY "cq_advanced_every" ON "transportation"
RESAMPLE EVERY 30m
BEGIN
  SELECT mean("passengers") INTO "average_passengers" FROM "bus_data" GROUP BY time(1h)
END
```

这里配置了30分钟执行一次CQ，没有指定FOR interval，于是查询的时间范围还是`GROUP BY time(1h)`指定的一个小时，执行流程如下：



```bash
At 8:00, cq_advanced_every 执行时间范围 time >= '7:00' AND time < '8:00'.
name: average_passengers
------------------------
time                   mean
2016-08-28T07:00:00Z   7
At 8:30, cq_advanced_every 执行时间范围 time >= '8:00' AND time < '9:00'.
name: average_passengers
------------------------
time                   mean
2016-08-28T08:00:00Z   12.6667
At 9:00, cq_advanced_every 执行时间范围 time >= '8:00' AND time < '9:00'.
name: average_passengers
------------------------
time                   mean
2016-08-28T08:00:00Z   13.75
```

需要注意的是，这里的 8点到9点这个区间执行了两次，第一次执行时时8:30，平均值是 `(8+15+15）/ 3 = 12.6667`，而第二次执行时间是9:00，平均值是 `(8+15+15+17) / 4=13.75`，而且最后第二个结果覆盖了第一个结果。[InfluxDB如何处理重复的记录可以参见这个文档](https://link.jianshu.com?t=https%3A%2F%2Fdocs.influxdata.com%2Finfluxdb%2Fv1.3%2Ftroubleshooting%2Ffrequently-asked-questions%2F%23how-does-influxdb-handle-duplicate-points)。

最终结果：



```css
> SELECT * FROM "average_passengers"
name: average_passengers
------------------------
time                   mean
2016-08-28T07:00:00Z   7
2016-08-28T08:00:00Z   13.75
```

### 示例2 只配置查询时间范围



```ruby
CREATE CONTINUOUS QUERY "cq_advanced_for" ON "transportation"
RESAMPLE FOR 1h
BEGIN
  SELECT mean("passengers") INTO "average_passengers" FROM "bus_data" GROUP BY time(30m)
END
```

只配置了时间范围，而没有配置EVERY interval。这样，执行的时间间隔与`GROUP BY time(30m)`一样为30分钟，而查询的时间范围为1小时，由于是按30分钟分组，所以每次会写入两条记录。执行流程如下：



```bash
At 8:00 cq_advanced_for 查询时间范围：time >= '7:00' AND time < '8:00'.
写入两条记录。
name: average_passengers
------------------------
time                   mean
2016-08-28T07:00:00Z   6.5
2016-08-28T07:30:00Z   7.5
At 8:30 cq_advanced_for 查询时间范围：time >= '7:30' AND time < '8:30'.
写入两条记录。
name: average_passengers
------------------------
time                   mean
2016-08-28T07:30:00Z   7.5
2016-08-28T08:00:00Z   11.5
At 9:00 cq_advanced_for 查询时间范围：time >= '8:00' AND time < '9:00'.
写入两条记录。
name: average_passengers
------------------------
time                   mean
2016-08-28T08:00:00Z   11.5
2016-08-28T08:30:00Z   16
```

需要注意的是，`cq_advanced_for`每次写入了两条记录，重复的记录会被覆盖。

最终结果：



```css
> SELECT * FROM "average_passengers"
name: average_passengers
------------------------
time                   mean
2016-08-28T07:00:00Z   6.5
2016-08-28T07:30:00Z   7.5
2016-08-28T08:00:00Z   11.5
2016-08-28T08:30:00Z   16
```

### 示例3 同时配置执行时间间隔和查询时间范围



```ruby
CREATE CONTINUOUS QUERY "cq_advanced_every_for" ON "transportation"
RESAMPLE EVERY 1h FOR 90m
BEGIN
  SELECT mean("passengers") INTO "average_passengers" FROM "bus_data" GROUP BY time(30m)
END
```

这里配置了执行间隔为1小时，而查询范围90分钟，最后分组是30分钟，每次插入了三条记录。执行流程如下：



```bash
At 8:00 cq_advanced_every_for 查询时间范围 time >= '6:30' AND time < '8:00'.
插入三条记录
name: average_passengers
------------------------
time                   mean
2016-08-28T06:30:00Z   3
2016-08-28T07:00:00Z   6.5
2016-08-28T07:30:00Z   7.5
At 9:00 cq_advanced_every_for 查询时间范围 time >= '7:30' AND time < '9:00'.
插入三条记录
name: average_passengers
------------------------
time                   mean
2016-08-28T07:30:00Z   7.5
2016-08-28T08:00:00Z   11.5
2016-08-28T08:30:00Z   16
```

最终结果：



```css
> SELECT * FROM "average_passengers"
name: average_passengers
------------------------
time                   mean
2016-08-28T06:30:00Z   3
2016-08-28T07:00:00Z   6.5
2016-08-28T07:30:00Z   7.5
2016-08-28T08:00:00Z   11.5
2016-08-28T08:30:00Z   16
```

### 示例4 配置查询时间范围和FILL填充



```ruby
CREATE CONTINUOUS QUERY "cq_advanced_for_fill" ON "transportation"
RESAMPLE FOR 2h
BEGIN
  SELECT mean("passengers") INTO "average_passengers" FROM "bus_data" GROUP BY time(1h) fill(1000)
END
```

在前面值配置查询时间范围的基础上，加上FILL填充空的记录。执行流程如下：



```csharp
At 6:00, cq_advanced_for_fill 查询时间范围：time >= '4:00' AND time < '6:00'，没有数据，不填充。

At 7:00, cq_advanced_for_fill 查询时间范围：time >= '5:00' AND time < '7:00'. 写入两条记录，没有数据的时间点填充1000。
------------------------
time                   mean
2016-08-28T05:00:00Z   1000          <------ fill(1000)
2016-08-28T06:00:00Z   3             <------ average of 2 and 4

[…] At 11:00, cq_advanced_for_fill 查询时间范围：time >= '9:00' AND time < '11:00'.写入两条记录，没有数据的点填充1000。
name: average_passengers
------------------------
2016-08-28T09:00:00Z   20            <------ average of 20
2016-08-28T10:00:00Z   1000          <------ fill(1000)     

At 12:00, cq_advanced_for_fill 查询时间范围：time >= '10:00' AND time < '12:00'。没有数据，不填充。
```

最终结果:



```css
> SELECT * FROM "average_passengers"
name: average_passengers
------------------------
time                   mean
2016-08-28T05:00:00Z   1000
2016-08-28T06:00:00Z   3
2016-08-28T07:00:00Z   7
2016-08-28T08:00:00Z   13.75
2016-08-28T09:00:00Z   20
2016-08-28T10:00:00Z   1000
```



# influxDB 数据保留策略

## 需求

在使用Telegraf+InfluxDB+Grafana监控服务器资源的时候，如果influxdb中的数据不设置超时过期的机制的话，那么数据就会默认一直保存。这样一直保存的话，数据量就会导致偏大。 这时候就要适当调整influxdb的数据存储时长，保留最近一段时间的数据即可。

## 1.基本概念说明

### 1.1 InfluxDB 数据保留策略说明

retention policy， 即数据保留策略，数据中的retention policy为默认的autogen。它表示数据一直保留永不过期，副本数量为1。你也可以指定数据的保留时间，如30天。

InfluxDB的数据保留策略(RP)用来定义数据在InfluxDB中存放的时间,或者定义保存某个期间的数据。 一个数据库可以有多个保留策略, 但每个策略必须是独一无二的。

### 1.2  InfluxDB数据保留策略目的

InfluxDB本身不提供数据的删除操作, 因此用来控制数据量的方式就是定义数据保留策略。 因此定义数据保留策略的目的是让InfluxDB能够知道可以丢弃哪些数据, 节省数据存储空间，避免数据冗余的情况。

## 2.操作示例

### 2.1 查看数据保留策略

```javascript
show retention policies on 数据库名
```

执行如下：

```javascript
# 选择使用telegraf数据库
> use telegraf;
Using database telegraf
> 
> 
# 查询数据保留策略
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        true
> 
```

从查询的结果来看，默认只有一个策略，而上面这个策略的说明了什么信息呢？

- name 策略名称：默认autogen
- duration 持续时间： 0s 代表无限制
- shardGroupDuration shardGroup数据存储时间：shardGroup是InfluxDB的一个基本存储结构, 应该大于这个时间的数据在查询效率上应该有所降低。
- replicaN 副本个数：1 代表只有一个副本
- default 是否默认策略：true 代表设置为该数据库的默认策略

### 2.2 新建数据保留策略

```javascript
# 新建一个策略
CREATE RETENTION POLICY "策略名称" ON 数据库名 DURATION 时长 REPLICATION 副本个数;

# 新建一个策略并且直接设置为默认策略
CREATE RETENTION POLICY "策略名称" ON 数据库名 DURATION 时长 REPLICATION 副本个数 DEFAULT;
```

下面直接新增一个新的默认策略看看，示例如下：

```javascript
# 创建新的默认策略之前的策略
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        true
> 
> 
# 创建新的默认策略role_01保留数据时长1小时
> CREATE RETENTION POLICY "role_01" ON telegraf DURATION 1h REPLICATION 1 DEFAULT;
> 
# 查看策略的变化
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        false
role_01 1h0m0s   1h0m0s             1        true
> 
```

因为默认策略已经修改为`role_01`，那么如果还想用之前的`autogen`策略来查询数据，则需要在查询表之前加上策略的名称：`"策略名".表名`，如下：

```javascript
> select * from "autogen".cpu limit 2;
name: cpu
time                cpu       host     usage_guest usage_guest_nice usage_idle        usage_iowait        usage_irq usage_nice usage_softirq usage_steal usage_system        usage_user
----                ---       ----     ----------- ---------------- ----------        ------------        --------- ---------- ------------- ----------- ------------        ----------
1574663960000000000 cpu-total locust03 0           0                99.44972486076016 0.05002501250678571 0         0          0             0           0.2501250625248291  0.2501250625430281
1574663960000000000 cpu0      locust03 0           0                99.59959959921699 0.10010010010243535 0         0          0             0           0.20020020020031867 0.10010010005008706
> 
```

### 2.3 修改数据保留策略

```javascript
ALTER RETENTION POLICY "策略名称" ON "数据库名" DURATION 时长

ALTER RETENTION POLICY "策略名称" ON "数据库名" DURATION 时长 DEFAULT
```

在这里示例修改`role_01`策略的时长为`2h`，如下：

```javascript
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        false
role_01 1h0m0s   1h0m0s             1        true
> 
> 
# 执行修改时长为2小时
> ALTER RETENTION POLICY "role_01" ON "telegraf" DURATION 2h
> 
# 可以看到role_01的duration为2h
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        false
role_01 2h0m0s   1h0m0s             1        true
> 
```

### 2.4 删除数据保留策略

```javascript
drop retention POLICY "策略名" ON "数据库名"
```

示例删除`role_01`策略，如下：

```javascript
# 查看当前的数据保留策略
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        false
role_01 2h0m0s   1h0m0s             1        true
> 
# 删除role_01的策略
> drop retention POLICY "role_01" ON "telegraf"
> 
# 查看删除后的策略，可以看到剩余的策略autogen并不会自动设置为默认default策略
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        false
> 
# 修改autogen策略为default策略
> ALTER RETENTION POLICY "autogen" ON "telegraf"  DEFAULT
> 
> show retention policies on telegraf
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 0s       168h0m0s           1        true
> 
```

## 3. 验证变更策略之后，存储数据是否会变少

默认的telegraf数据库的存储策略是一直保存数据，并无限制。那么为了节省数据存储，我下面创建一个保留1小时的策略，然后删除默认的策略，观察存储数据是否变少。

### 3.1 变更策略之前的数据存储大小

在变更策略之前，我特意运行了采集数据服务几天，查看目前的存储数据大小如下：

```javascript
[root@server influxdb]# du -h --max-depth=1 .
69M ./data
69M .
[root@server influxdb]# 
```

可以看到有69M的存储数据。

### 3.2 创建新策略，删除旧策略

```javascript
# 创建新策略
> CREATE RETENTION POLICY "rule_telegraf" ON telegraf DURATION 1h REPLICATION 1 DEFAULT;
> 
> show retention policies on telegraf
name          duration shardGroupDuration replicaN default
----          -------- ------------------ -------- -------
autogen       0s       168h0m0s           1        false
rule_telegraf 1h0m0s   1h0m0s             1        true
> 
# 删除历史策略
> drop retention POLICY "autogen" ON "telegraf";
> 
# 查看当前的数据策略
> show retention policies on telegraf
name          duration shardGroupDuration replicaN default
----          -------- ------------------ -------- -------
rule_telegraf 1h0m0s   1h0m0s             1        true
> 
```

### 3.3 删除旧策略之后，确认数据存储大小

```javascript
# 删除旧策略之前，数据有69M
[root@server influxdb]# du -h --max-depth=1 .
69M ./data
69M .
[root@server influxdb]# 
# 删除旧策略之后，数据只保留15M
[root@server influxdb]# du -h --max-depth=1 .
15M ./data
15M .
[root@server influxdb]# 
```

从上面的结果来看，只需要配置管理数据保留策略，就可以控制好数据的存储空间。



# Python 操作 InfluxDB

安装influxdb-python ：

```bash
pip install influxdb 
```

实际上py的influx官方包的doc也已经足够详细，值得过一遍：[py-influxdb](https://influxdb-python.readthedocs.io/en/latest/include-readme.html)

## 基本操作

使用InfluxDBClient类操作数据库，示例如下：

```python
# 初始化
client = InfluxDBClient('localhost', 8086, 'your_username', 'yuor_password', 'your_dbname') 
```

- 显示已存在的所有数据库

　　使用get_list_database函数，示例如下：

　　`print client.get_list_database() # 显示所有数据库名称`

- 创建新数据库

　　使用create_database函数，示例如下：

　　`client.create_database('testdb') # 创建数据库`

- 删除数据库

　　使用drop_database函数，示例如下：

　　`client.drop_database('testdb') # 删除数据库`

数据库操作完整示例如下：

```python
from influxdb import InfluxDBClient

# 初始化（指定要操作的数据库）
client = InfluxDBClient('localhost', 8086, 'your_username', 'yuor_password', 'your_dbname') 
print(client.get_list_database()) # 显示所有数据库名称
client.create_database('testdb') # 创建数据库
print(client.get_list_database()) # 显示所有数据库名称
client.drop_database('testdb') # 删除数据库
print(client.get_list_database()) # 显示所有数据库名称
```



## 表操作

InfluxDBClient中要指定连接的数据库，示例如下：

```python
client = InfluxDBClient('localhost', 8086, 'your_username', 'yuor_password', 'your_dbname') 
```

- 显示指定数据库中已存在的表

　　可以通过influxql语句实现，示例如下：

```python
result = client.query('show measurements;') # 显示数据库中的表
print("Result: {0}".format(result))
```

- 创建新表并添加数据

InfluxDB没有提供单独的建表语句，可以通过并添加数据的方式建表，示例如下：

```python
current_time = datetime.datetime.utcnow().isoformat("T")
body = [
    {
        "measurement": "students",
        "time": current_time,
        "tags": {
            "class": 1
        },
        "fields": {
            "name": "Hyc",
            "age": 3
        },
    }
]

res = client.write_points(body)
```

- 删除表

可以通过influx sql语句实现，示例如下：

```
client.query("drop measurement students") # 删除表
```

数据表操作完整示例如下：

```python
import datetime
from influxdb import InfluxDBClient


client = InfluxDBClient('localhost', 8086, 'your_username', 'yuor_password', 'your_dbname') 
current_time = datetime.datetime.utcnow().isoformat("T")
body = [
    {
        "measurement": "students",
        "time": current_time,
        "tags": {
            "class": 1
        },
        "fields": {
            "name": "Hyc",
            "age": 3
        },
    }
]
res = client.write_points(body)
client.query("drop measurement students")
```

## 数据操作

InfluxDBClient中要指定连接的数据库，示例如下：

```
# 初始化（指定要操作的数据库）
client = InfluxDBClient('localhost', 8086, 'your_username', 'yuor_password', 'your_dbname')  
```

- 添加

可以通过write_points实现，示例如下：

```python
body = [
    {
        "measurement": "students",
        "time": current_time,
        "tags": {
            "class": 1
        },
        "fields": {
            "name": "Hyc",
            "age": 3
        },
    }，
    {
        "measurement": "students",
        "time": current_time,
        "tags": {
            "class": 2
        },
        "fields": {
            "name": "Ncb",
            "age": 21
        },
    }，
]
res = client.write_points(body)
```

- 查询

可以通过influxql语句实现，示例如下：

```python
result = client.query('select * from students;')
print("Result: {0}".format(result))
```

- 更新

tags 和 timestamp相同时数据会执行覆盖操作，相当于InfluxDB的更新操作。

- 删除

使用influxql语句实现，delete语法，示例如下：

```python
client.query('delete from students;') # 删除数据
```