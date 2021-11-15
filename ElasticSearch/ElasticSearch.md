# 基础入门

## 入门介绍

Elasticsearch 是一个分布式可扩展的实时搜索和分析引擎,一个建立在全文搜索引擎 Apache Lucene(TM) 基础上的搜索引擎.当然 Elasticsearch 并不仅仅是 Lucene 那么简单，它不仅包括了全文搜索功能，还可以进行以下工作:

- 分布式实时文件存储，并将每一个字段都编入索引，使其可以被搜索。
- 实时分析的分布式搜索引擎。
- 可以扩展到上百台服务器，处理PB级别的结构化或非结构化数据。

### 基本概念

先说Elasticsearch的文件存储，Elasticsearch是面向文档型数据库，一条数据在这里就是一个文档，用JSON作为文档序列化的格式，比如下面这条用户数据，就是一个文档：

```
{
    "name" :     "John",
    "sex" :      "Male",
    "age" :      25,
    "birthDate": "1990/05/01",
    "about" :    "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
```

用Mysql这样的数据库存储就会容易想到建立一张User表，有name、sex等字段，在Elasticsearch里这就是一个 **文档** ，当然这个文档会属于一个User的 **类型** ，各种各样的类型存在于一个 **索引** 当中。这里有一份简易的将Elasticsearch和关系型数据术语对照表:

```
关系型数据库			⇒ 数据库				 ⇒ 表					⇒ 行    					⇒ 列(Columns)

Elasticsearch		⇒ 索引(Index)		⇒ 类型(type)  ⇒ 文档(Docments)  ⇒ 字段(Fields)  
```

一个 Elasticsearch 集群可以包含多个索引(数据库)，索引中包含了很多类型(表)（类型的概念将在 8.x 版本完全弃用，7.x 还可以使用但是已经开始提示即将弃用。那么之后 一个索引中就只有一个类型），这些类型中包含了很多的文档(行)，然后每个文档中又包含了很多的字段(列)。Elasticsearch的交互，可以使用Java API，也可以直接使用HTTP的Restful API方式，比如我们打算插入一条记录，可以简单发送一个HTTP的请求：

```
# 创建 索引为：megacorp  类型为：employee 文档ID为 1 的文档
PUT /megacorp/employee/1 
{
    "name" :     "John",
    "sex" :      "Male",
    "age" :      25,
    "about" :    "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
```

更新，查询也是类似这样的操作，具体操作手册可以参见[Elasticsearch权威指南](http://www.learnes.net/data/README.html)



### 模型相关概念

- 集群Cluster：所谓集群，就是多个服务节点的集合，集群意味着这些节点是能够相互交流的，不然无法进行数据交互。集群的默认名称是"elasticsearch"，**多个提供服务的节点会根据集群名来自动加入集群**。
- 节点Node：节点是集群的一部分，是集群的最小单元，是可以提供服务的节点。
- 分片shard：分片位于节点上，分片是elasticsearch数据存储的单元，elasticsearch中的数据会存储在分片中。分片可以存储在任意一个节点上。分片分为主分片Primary Shard和副本分片Replica Shard。
- 主分片Primary Shard：当存储一个文档document的时候，会先存储到主分片中，然后再复制到其他的副本分片Replica Shard中。
- 副本分片Replica Shard：副本分片是主分片的复制（备份）。默认情况下，主分片有一个副本分片，主分片不能修改，但副本分片可以后续再增加。
  - 为了保证数据的不丢失，通常来说**Replica Shard不能与其对应的Primary Shard处于同一个节点中**。【因为万一这个节点损坏了，那么存储在这个节点上的原数据（primary shard）和备份数据（replica shard）就全部丢失了】
  - 当主分片挂掉的时候，会选择一个副本分片作为主分片。
  - 查询可以在主分片或副本分片上进行查询，这样可以提供查询效率。【但数据的修改只发生在主分片上。】
  - 一个Primary Shard可以有多个Replica Shard，默认创建是1个。



### 数据存储相关概念

数据存储在shard中，shard中的数据是以文档document为单位的。document存储在index和type划分的逻辑空间中。document以json为格式，每一个key-value中key可以称为域Field。

- 索引Index：索引是存储具有相同结构的document的集合，意义上有点类似关系型数据库中的数据库，用于存储一系列数据，比如可以说“商品”索引，一般都是个大类，小逻辑划分由Type处理。

- 类型Type：类型是索引的逻辑分区，意义有点类似关系型数据库中的数据表。用来划分索引下不同子类型的数据，比如商品（索引）可以有电子产品（类型），药品（类型）。在同一个分类下的数据一般都具有同种特征，用来定义数据的字段的数量一般也是相同的。每一个document都有一个type和一个id，在存储文档的时候需要指定索引、类型和ID。

  在ES的新版本中，每个索引将只允许存在一个类型，默认为 **_doc** 类型。

- 文档Document：类似于关系型数据库中的记录，是ElasticSearch的数据存储的基本单位，格式与JSON相同。

  - **文档元数据**

    - _index: 代表当前的索引名（唯一标识索引的数据）

    - `_type`：代表数据的type类型，7.x后默认_doc

    - _id:  文档的唯一id，可以自定义：`put /index/type/66`，但是不能重复；也可以由ES自动生成：`put /index/type`。ES生成的id长度为20个字符，使用的是base64编码，URL安全，使用的是GUID算法，分布式下并发生成id值时不会冲突。

    - _version：文档的版本号，如果进行更新等操作，会增加版本数。
    - _shards:  分片信息。

    - _seq_no：严格递增的顺序号。保证后写入的Doc的seqno比之前的大。

    - _primary_term: 代表主分片上数据重新分配的次数。比如重启节点，重新分配都会触发这个参数累加。

    - _routing: 路由规则，写入和查询要保证路由是一致。

    - _source: 文档数据明细信息。

      ```json
      # 创建 索引：小张、类型：默认 _doc、文档id：1 的文档数据
      PUT /xiaozhang/_doc/1
      {
        "name": "zhangjian",
        "age": 18
      }
      
      # 响应结果
      {
        "_index" : "xiaozhang",
        "_type" : "_doc",
        "_id" : "1",
        "_version" : 1,
        "result" : "created",  # 由于是首次put这个ID的文档，所以是 create，再次put相同id就是 update 了。
        "_shards" : {
          "total" : 2,
          "successful" : 1,
          "failed" : 0
        },
        "_seq_no" : 0,
        "_primary_term" : 1
      }
      ```

- 域Field：类似于关系型数据库中的字段。

- elasticsearch是面向restful的，下面是restful请求与elasticsearch操作的对应：

  | 请求方法 | 对应操作 |        说明        |
  | :------: | :------: | :----------------: |
  |   GET    |   读取   |      获取数据      |
  |   POST   |   新增   |      新增数据      |
  |   PUT    |   修改   | 修改数据或增加数据 |
  |  DELETE  |   删除   |      删除数据      |

- 索引用来存储数据，分片也是用来存储数据，它们是怎么对应的？一个索引存储在多个分片上，默认情况下，一个索引有五个主分片，五个副本分片。主分片的数量一旦定下来就不能再修改，但副本分片的数量还可以修改。



## 映射

>我们讲到了 Mapping 类似于数据库中的表结构的定义 ，它有以下几个作用：
>
>- **定义索引中的字段的名称**
>- **定义字段的数据类型**，比如字符串、数字、布尔
>- **字段，倒排索引的相关配置**，比如设置某个字段为不被索引、记录 position 等

tip：实例中会使用到基础的CRUD操作，建议先看 文档操作-基础CRUD部分。



### 数据类型

#### 一、核心数据类型

- 字符串：`text`, `keyword`
- 数值型：`long`, `integer`, `short`, `byte`, `double`, `float`, `half_float`, `scaled_float`
- 布尔型：`boolean`
- 日期型：`date`, `date_nanos`
- 二进制：`binary`
- 范围型：`integer_range`, `float_range`, `long_range`, `double_range`, `date_range`

##### 1. 字符串

###### [text](https://link.segmentfault.com/?enc=HPwtHyRUKESfXI5VoYSh2A%3D%3D.LQcZZz014ZVuMbnXIwKLTWsnPqg%2B2BCbWzn2XIRoe6B9m7yrqHgzfYuAGFhCIQcJK79ghMZlgRPshaTw1BSLDE%2B0%2Fw6RVMOWmO5zAF84WW0%3D)

text 类型的字段数据会被分词，在生成倒排索引以前，字符串会被分词器分成一个一个词项。
text 类型的字段不用于排序，很少用于聚合(termsAggregation除外)。
如果一个字段需要被全文搜索或模糊匹配，比如文章内容、产品描述、新闻内容等，应该使用text类型。

###### [keyword](https://link.segmentfault.com/?enc=VVGTABi2%2BCHymZ%2FJoQcxfQ%3D%3D.mJ424MsSNdZ1VYT%2FwgrDGQ64KhOWiubJTeJJh%2BCI0DxAELP1xaA5X15A3%2FSotUK1vYgmrJn3Q86wHIFjCF2uszA1I%2FRD6NdBvuKT9UYcNQ4%3D)

keyword 类型的字段内容不会被分词，整体作为一个 term 并创建 倒排索引。
keyword 类型的字段只能通过精确值搜索到，用于过滤、排序、聚合。
适用于索引结构化的字段，比如IP地址、性别和地区等。

##### 2. [数值型](https://link.segmentfault.com/?enc=cB%2BQ6e8wqbYm7MD%2B36V%2B%2BA%3D%3D.XjcpVhW8YaR2Aem4mmsqqHPzKWJy2SjoFofzEYVYfSGkPYJyeIzvPWdeGoNHlB6vtvgmFsgttFS52FTfPut5c5%2FF%2BvagpPiaRU%2FIjGfQvAc%3D)

###### 整数

| 类型    | 最小值                         | 最大值                        | 说明                                                       |
| ------- | ------------------------------ | ----------------------------- | ---------------------------------------------------------- |
| byte    | -128                           | 127                           | 8 位有符号整数（1个字节），相当于MySQL中有符号的 tinyint   |
| short   | -32768                         | 32767                         | 16 位有符号整数（2个字节），相当于MySQL中有符号的 smallint |
| integer | -2147483648 (-2^31^)           | 2147483647 (2^31^-1)          | 32 位有符号整数（4个字节），相当于MySQL中有符号的 int      |
| long    | -9223372036854775808) (-2^63^) | 9223372036854775807 (2^63^-1) | 64 位有符号整数（8个字节），相当于MySQL中有符号的 bigint   |

对于整数类型的字段，在满足需求的情况下，要尽可能选择范围小的数据类型。比如某个字段的取值最大值不会超过100，那么选择byte类型即可。迄今为止,吉尼斯世界记录的人类的年龄的最大值为134岁，对于年龄字段，short足矣。字段的长度越短，索引和搜索的效率越高。



###### 小数

| 类型         | 最小值   | 最大值             | 说明             |
| ------------ | -------- | ------------------ | ---------------- |
| half_float   | 2^-24^   | 65504              | 16位半精度浮点数 |
| float        | 2^-149^  | (2-2^-23^)·2^127^  | 32位单精度浮点数 |
| double       | 2^-1074^ | (2-2^-52^)·2^1023^ | 64位双精度浮点数 |
| scaled_float |          |                    | 缩放类型浮点数   |

处理浮点数时，优先考虑使用scaled float类型。scaled float 是通过缩放因子把浮点数变成long类型，比如价格只需要精确到分，price字段的取值为57.34，设置放大因子为100，存储起来就是5734，所有的API都会把price的取值当作浮点数，事实上Elasticsearch底层存储的是整数类型，因为压缩整数比压缩浮点数更加节省存储空间。

##### 3. [布尔型](https://link.segmentfault.com/?enc=Tt4TikV5lZiFQfUOdmWDkQ%3D%3D.c6oc10ORgFQYUjEyB8TwLS9lXTHuE7zERl7Xc3blrdWoFurGpB%2BTdpcgPYvmhP6aUTT68HxMoArHu%2BGl0jUJJCxGFI2yPl60B3gttMZnM6M%3D)

如果一个字段是布尔类型，可接受的值为 `true`, `false`。
Elasticsearch 5.4版本以前，可以接受可被解释为 `true` 或 `false` 的字符串和数字。
5.4版本以后只接受 `true`, `false`, `"true"`, `"false"`。

##### 4. 日期型

###### [date](https://link.segmentfault.com/?enc=Qoc%2B1wrBTKlsgM3fl0hUTA%3D%3D.k9JFoCHG0gI0ohzvYZVfkH5l0Ia9fP6%2FRWkGALYtETXAB4ZaBsYrjhRcZnuPrwUgzCWYJ3NMrQCUCYpO3D8SZsgwOb2fAyZI37opThlYAGY%3D)

JSON 没有日期型数据类型，所以在Elasticsearch中，日期可以是：

- 包含格式化日期的字符串，例如"2015-01-01"或者"2015/01/01 12:10:30"
- 代表时间毫秒数的长整型数字。
- 代表时间秒数的整数。

Elasticsearch内部会把日期转换为 UTC （世界标准时间），并将其存储为代表时间毫秒数的长整数。
日期格式可以自定义，如果没有指定格式，则使用默认值：

```1c
"strict_date_optional_time||epoch_millis"
```

这种情况下可以解析下面三种日期格式：

```subunit
"2020-05-01"
"2020-05-01T12:10:30Z"
1591234567890
```

###### [date_nanos](https://link.segmentfault.com/?enc=7EmhJ3lxX%2Fe7t6v4B5oAiQ%3D%3D.WY7ioD0r4g%2B9NmQWM6Zy6noms5YAuwprbP9otPrmvJrMTR26x8yCLWj%2FkX0qgNgmxgjDTUGEV5ylAPOBAni%2FkAqTTZ%2FazUt3CvRUkC1xfII%3D)

此数据类型是对日期数据类型的补充。现有的 date 类型可以存储毫秒级时间。而 date_nanos 可以存储纳秒级时间。

##### 5. 二进制

###### [binary](https://link.segmentfault.com/?enc=Hv0TwqgmqBgW5n17p%2BTQ5Q%3D%3D.kMyXxGBJ8W1LSsbLjf84YbREzppr4rGmR3ovnujgkjLtg5a1IAB1ICu%2Bn6jWmPjC0tfVlljOuLkgI9uddLEIfYmC0ABfz7OvRIkzo2DLrzY%3D)

二进制数据类型接受Base64编码字符串的二进制值。字段不以默认方式存储而且不能搜索。
Base64编码二进制值不能嵌入换行符`\n`

##### 6. [范围型](https://link.segmentfault.com/?enc=ui4E31rCPGVTmICTLLTuEA%3D%3D.wVJTADAsDtncYGnWm0IPYmAGyVdKTGlLzvsWS1FhE87zQs2lFARQdFrnoXIAaUAgpejHOvHVX2iODx8b8m4Dbdi3xOCqixPAYic7M%2Fy9eGg%3D)

| 类型            | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| `integer_range` | 32 位有符号整数的范围值，-2^31^ ~ 2^31^-1                    |
| `long_range`    | 62 位有符号整数的范围值，-2^63^ ~ 2^63^-1                    |
| `float_range`   | 32位单精度浮点数范围值                                       |
| `double_range`  | 64位单精度浮点数范围值                                       |
| `date_range`    | 以64位无符号整数形式表示的日期值范围                         |
| `ip_range`      | [IPv4](https://link.segmentfault.com/?enc=GoO0bU%2BZp4wQiLtV4zySiA%3D%3D.f0kyZQccLY4mMb1z9031FKRO5V9azEkA0OfvTgjb01%2FZYbtMND8%2BFgrFTu1%2FEw2h) 或 [IPv6](https://link.segmentfault.com/?enc=ZlMxvi%2BDbZ7TItN44j3%2Byw%3D%3D.w5lpJP7xy4lf%2Fcl6C61fGub%2BZggFHHJXO362JRhp45DIU8CKg9CmGSVwY0sIJIeW) 的范围值 |



#### 二、复合数据类型

##### 1. 对象类型

[object](https://link.segmentfault.com/?enc=%2FatdQaRvyuwRC8KNLfXXTw%3D%3D.LkBMDUQJI0V%2FPvJ7JGx7l%2FkWf9eLWV4ypo2gvFjkFO3BWzT5Ie1G68xktuQkpQfxz6XOQTShLYyVCcd%2BzmQ4XC4L80oNRuSKSog6pr9O89c%3D)

用于存储单个JSON对象。
JSON本质上具有层级关系，文档包含内部对象，内部对象本身还可以包含内部对象。

##### 2. 嵌套类型

[nested](https://link.segmentfault.com/?enc=8ijTlPJllc2XwRKgQy1Qrg%3D%3D.Xo%2FUlPGjcdZuYKSycx53FZonHLZ0QNVVOJPd2rBN7vdYlDLLIzXzbiWiENvSxwqTU6IFzyjts0wUyQfKRI5J7N%2BIklVOK7CYWLTnvq9Fnrw%3D)

用于存储多个JSON对象组成的数组。
`nested` 类型是 `object` 类型中的一个特例，可以让对象数组独立索引和查询。Lucene没有内部对象的概念，所以Elasticsearch将对象层次扁平化，转化成字段名字和值构成的简单列表。



#### 三、地理位置类型

##### 1. 地理坐标类型

[geo_point](https://link.segmentfault.com/?enc=86pvqNOZRC1VtXHBqZ3tkQ%3D%3D.GR6cfCzhnJf2paqdaCzGnooAdYf9Wna4QlC9woV%2BxiJ%2BcfUWPQ9aNf0vUH5TeGCYMs3%2B6R8qCW3eSwk0hIxzt5K8hcC8P7qvCbQ1gbjl1yQ%3D)

用于存储经纬度坐标对，可用来
查找一定范围内的地理点,这个范围可以是相对于一个中心点的固定距离,也可以是多边形或者地理散列单元。
通过地理位置或者相对于中心点的距离聚合文档。
整合距离到文档的相关性评分中。

用于存储地理位置信息的经纬度坐标对，可用于以下几种场景：

- 查找一定范围内的地理位置。
- 通过地理位置或者相对中心点的距离来聚合文档。
- 把距离因素整合到文档的评分中。
- 通过距离对文档排序。

##### 2. 地理形状类型

[geo_shape](https://link.segmentfault.com/?enc=EqLi5GrIHDqf3oxTpXbbQA%3D%3D.SFMiTSJ5n2zuuN5wU8dTKqOpxOkW652bqDnL246SFde7FVGEDrr2%2F5698PE5mMl%2FWkuN2P4tL38uspUe47jIaJMBqeb9xVRa5ewBGTCCPRg%3D)

地理形状数据类型有利于索引和搜索任意地理形状，例如矩形、三角形或者其他多边形。无论是数据被索引还是在查询执行的过程中，都可以使用地理形状数据类型在地理点的基础上包含地理形状。
Elasticsearch 使用 `GeoJSON` 格式来表示地理形状。
`GeoJSON` 是一种对各种地理数据结构进行编码的格式，对象可以表示几何、特征或者特征集合,支持点、线、面、多点、多线、多面等几何类型。
`GeoJSON` 里的特征包含一个几何对象和其他属性，特征集合表示一系列特征。
想了解更多关于 `GeoJSON` 的资料可参考[《GeoJSON格式规范说明》](https://link.segmentfault.com/?enc=opf7HnW%2FIHNu9suutwp0BQ%3D%3D.%2Bv2NdwO3qqmZQ3VLZv5ydBDLh3vbubYElrJvBaK3iDaXTtnz6akccqFquoI4xVjk)



#### 四、特殊类型

##### [IP](https://link.segmentfault.com/?enc=vdWIpDpvMPjUk8g7SRbyMA%3D%3D.nAER%2F8AYoRQe14kaDRF%2B%2FrRWIcQs%2FPYEIl%2FGbULZSz%2FpbMWrxMz7wVKgcwVMHUc4ZVe0c1K6kxreo5eGiw1H63GMB0fI4rmwItv3T5iQ724%3D)

IP地址类型，存储 IPv4 和 IPv6 地址

##### [Completion datatype](https://link.segmentfault.com/?enc=wnVCMZVSslQA%2B0qJsYHJrA%3D%3D.0qFFpcMvrB4jYci%2BfBKPuavWhsfyy74f28Nis%2Farun24nGmAR6cOzDmwm5RmdHfDkDvOPmiMZo9tZDOi3dof0Y9HFWT%2BXgvAII5MyDV5nIGiJArWlx2GzB1YyhOLhkEu2p7Py%2FGxfhMwmjHe9qZNDg%3D%3D)

`completion` 提供自动补全建议

##### [Token count](https://link.segmentfault.com/?enc=1OwRtwax87fUY%2BsnfEz%2FRQ%3D%3D.9Ylv9%2FENYTplGfEntauW%2FgW%2B7sA51lnj2P2NpFWD5qM17IcJy%2BwYYkCRdt%2BEcih6cQu7R6dl%2Bg10trB1IHGwpujx9Rb8TPZ0QUds7%2F5HgAHvUAouJg1m3Bju%2FeAEbcLV)

`token_count` 用于统计字符串分词后的词项个数，本质上是一个整数型字段。
例如：映射中指定 name 为 text 类型，增加 name_length 字段用于统计分词后词项的长度，类型为 token_count，分词器为标准分词器。

##### [`mapper-murmur3`](https://link.segmentfault.com/?enc=8lyDzEyrd%2F5T%2FBcaTk91hg%3D%3D.A0wsfsIve3LRuJl0AZv5VQ6Dp8BmoPtez4P4JC0Ss15gocd%2FS048dOTEbzM0A%2B1ZEG224geV6qtzHOs%2FNss0dYfX9581kUIRq9%2BMM%2FDv6so%3D)

`murmur3` 在索引时计算值的哈希值并将它们存储在索引中

##### [`mapper-annotated-text`](https://link.segmentfault.com/?enc=%2BXdUP3YGkl78YzTb2%2FiNJw%3D%3D.PBrCPlEGJB%2Bu3y3RISUOU0O3z4onsMcS8wpTSLuFUNoAJkI290MSnlIryUKay6JV9Fqe95S6CrMPkhGcElaCIXKQKjt0OUUXNR4QYf6Fzq%2FQ%2B7Db9ceYuLrqTJatsV7L)

`annotated-text` 索引包含特殊标记的文本（通常用于标识命名实体）

##### [Percolator](https://link.segmentfault.com/?enc=Y3IWzgXysUK29z4vkDdYFg%3D%3D.cvk71Jl6MPcBPmzyQypm4ZHG2NaHYJxGbcQNk4BwmcM3bSgaDbGBfzHNbN6Ju%2FLLGtVV55nFh1zrflaB1gZfmyL3XBDalavBEDiD8F1zyQQ%3D)

接受来自 `query-dsl` 的查询

##### [Join](https://link.segmentfault.com/?enc=fWHatOOjEEIUsEVjO2A42Q%3D%3D.1FvfxwqetKEPomUFImQTZeWw%2BaF8%2Bkpl%2FtTsQRwn5mqB4tXfZkuWOvajL%2Be5IG7RZtPtng5GN%2FTGka4oOBcq5WYbUHe7c5U6oYaqyUgRgar66Dp3Wf9cxIYWx6jTuoKu)

为同一索引中的文档定义父/子关系

##### [Rank feature](https://link.segmentfault.com/?enc=jCzDGEVFqRjTJDN8cckeXw%3D%3D.hmw3xtmwEVWUt7XfiezJO5KjBnQ0UW6QCSAS9c9qBTBQtLuWGJVkFfMQOdO4Mvsy8iPuS%2BBzoe2cMDuU3Vx3Tzuh0HwmtXYegmBR2B0ipCQZFb%2Bw%2F52Ux4FqO4TqwAuW)

##### [Rank features](https://link.segmentfault.com/?enc=9M8Wsqkzf3fE%2BXERM9flLA%3D%3D.uSbbPR15a62qDn9IQSxWQ0csITO5IN%2FaesjXCPErtS4dTUZPubKQazBwD90fMdjje2sIvk3%2F5gRBWedqMkcJICe7hbBx2vWon8LOKHU76%2FCN%2FXwbsMjfzEeQUEk7Mg5X)

排名功能，记录数字特性以提高查询时的命中率

##### [Dense vector](https://link.segmentfault.com/?enc=s68xipZtUXKUovMWBqXX2Q%3D%3D.VAF0lGGbMUlCEv%2Ff%2B%2FYcrfjx%2F40C1emUFbSr2NeFXfIjK6BzWYTwAf4O7q7uByKNwvRIslvQEK%2F5QkzuZpCufNIbaAwx1Y50xGbpfRMsoSRa3JXxyKhrLszGtH7U7HQM)

密集向量，记录浮点值的密集向量

##### [Sparse vector](https://link.segmentfault.com/?enc=N%2FEbArCyEeguY1SciRpjxg%3D%3D.xH5g1%2BvxWy%2FqtJ%2BOWJSl6cMruRnTV5yqwDdYSu3NQOY7Pmi7%2FMDtqqQmyT1G4YQje6x0zXCLmMTcGxOmkrNWLDDuBuTxL7Xht1hN5Q9z66IpDRrfF16l3OcGVJD%2FMB1O)

稀疏向量，记录浮点值的稀疏向量

##### [Search-as-you-type](https://link.segmentfault.com/?enc=CcKshla6PeLcPyx82EIDgg%3D%3D.V1G38UcC7IoSU9BD0Isb9GwwFI53eXw6XwywmL9sye0qwcyXUWRm7j%2ByU6XIcNn2xNkN%2BfBtxZ1HAXLOVJnYwe9ZFkC4zq6w5oNzmtZwN34ezVTBFWmA1llC8vpnFKUy)

按类型搜索，类似文本的字段，为查询进行优化，以实现按类型完成

##### [Alias](https://link.segmentfault.com/?enc=vrKrVIlnhyq%2B3kagNwWmXg%3D%3D.Rtl%2BIN%2BoITGg1K90Y9xNKF5NUXvFt4ZaSFlWqX64KbqrSeQabFmLPUQIDgF4aveUWQzzKUaBHSbGTuktIqsbhGQfjV80LpU2wyQzuxezdXc%3D)

别名，定义现有字段的别名

##### [Flattened](https://link.segmentfault.com/?enc=4I1mUACmSO2D3CJ6NZsZXg%3D%3D.hK4IjYc6LMtFYaBBhSMGQpW%2BfvhXDm0xUX3kTkUDccQWe41HarbYM%2BbWgBgTbf5JEAlt4vcjePYfVja%2F632Ed1Spc2OozYm1bLQsESWN1FE%3D)

允许将整个JSON对象作为单个字段编入索引。

##### [Shape](https://link.segmentfault.com/?enc=maY7lBbm%2BotPZuaffC19Dg%3D%3D.Xb8XqgRb6KJqeCrOe26ByPOKdLVaDt98tZ5dt%2F5a3jIeXZK6PNKlaQweBDy0txs3%2BAMKPOwQdHthP4oO8Twan5wF3rhRFJWltqkVZ7oRgxI%3D)

`shape` for arbitrary cartesian geometries.

##### [Histogram](https://link.segmentfault.com/?enc=epQuOHwpgPIc692S3Hx3vw%3D%3D.sVfkNPwDDEwqEmlPMFFh9xhyLEcRSBbGg49z3EcQSC4IAKvgkVP8BcP6syrHfvjpG%2BrDSsCI185eP5RYNVApCbwAA6i%2Fk5I7%2BBBoGNzuKw0%3D)

`histogram` for pre-aggregated numerical values for percentiles aggregations.



#### 五、数组类型

数组类型不需要专门指定数组元素的类型，任何字段类型都可以包含在数组内，但是数组中的所有值必须具有相同的数据类型。

- 字符型数组: `["one", "two"]`
- 整型数组：`[1, 2]`
- 数组型数组：`[1, [2, 3]]` 等同于 `[1, 2, 3]`
- 对象数组：`[{"name": "Mary", "age": 12}, {"name": "John", "age": 10}]`





### 创建映射

映射（Mapping）可以手动创建，如果在添加文档之前没有手动创建映射，那么将在添加文档时，自动根据添加字段的类型创建映射。

**示例：查看映射**

```json
GET users/_mapping

{
  "users" : {
    "mappings" : {
      "properties" : {
        "age" : {
          "type" : "long"
        },
        "date" : {
          "type" : "date"
        },
        "height" : {
          "type" : "long"
        },
        "message" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "tag" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "user" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}
```



**示例：手动创建**

```json
# 创建PUT demo
{
  "mappings": {
        "properties": {
          "name":{
            "type": "text"
          },
          "age":{
            "type": "long"
          },
          "tag":{
            "type": "keyword"
          }
        }
  }
}

# 查看
GET demo/_mapping

{
  "demo" : {
    "mappings" : {
      "properties" : {
        "age" : {
          "type" : "long"
        },
        "name" : {
          "type" : "text"
        },
        "tag" : {
          "type" : "keyword"
        }
      }
    }
  }
}
```



### 映射参数

1. **ignore_above**

   > 创建 mapping 时，可以为字符串（专指 keyword） 指定 ignore_above ，用来限定字符长度。超过 ignore_above 的字符会被存储，但不会被索引。
   >
   > 注意，是字符长度，一个英文字母是一个字符，一个汉字也是一个字符。
   >
   > 在动态生成的 mapping 中，keyword类型会被设置ignore_above: 256。

   ```json
   # 创建索引及映射
   PUT demo1
   {
     "mappings": {
       "properties": {
         "name":{
           "type": "keyword",
           "ignore_above": 5
         }
       }
     }
   }
   
   # 创建文档，字符长度为3，此时按 name 可查询到文档
   POST demo1/_create/2
   {
     "name": "阿克苏"
   }
   
   GET demo1/_search
   {
     "query": {
       "match": {
         "name": "阿克苏"
       }
     }
   }
   
   # 修改字段name的值，使其长度大于5。此时再通过那么去匹配，查询结果为空
   POST demo1/_update/2
   {
     "doc": {
       "name": "罗罗左亚-索隆"
     }
   }
   
   GET demo1/_search
   {
     "query": {
       "match": {
         "name": "罗罗左亚-索隆"
       }
     }
   }
   ```

2. **index**

   > index 参数默认值为true，如果设置为 false，那么 elasticsearch 不会为该属性创建索引，也就是说无法被当作住查询条件。

   ```json
   # 创建映射
   PUT demo2
   {
     "mappings": {
       "properties": {
         "title":{
           "type": "text",
           "index": true
         },
         "sub_title":{
           "type": "text",
           "index": false
         }
       }
     }
   }
   
   # 添加数据
   POST demo2/_create/1
   {
     "title": "母猪的产前保养",
     "sub_title": "母猪的产后护理"
   }
   
   # 查询
   GET demo2/_search
   {
     "query": {
       "match": {
         "title": "母猪"  # 可以正常查询到值
       }
     }
   }
   
   GET demo2/_search
   {
     "query": {
       "match": {
         "sub_title": "母猪"  # status:400;"reason" : "Cannot search on field [sub_title] since it is not indexed."
       }
     }
   }
   ```

3. **copy_to**

   > copy_to 作用是将该字段的值复制到目标字段，实现类似 _all 的作用，它不会出现在 _source 中，只用来搜索。

   ```json
   # 创建映射。copy_to可以接受多个字段的拷贝
   PUT demo3
   {
     "mappings": {
       "properties": {
         "first_name":{
           "type": "text",
           "copy_to": "full_name"
         },
         "last_name":{
           "type": "text",
           "copy_to": "full_name"
         }
       }
     }
   }
   
   # 新增文档
   POST demo3/_create/1
   {
     "first_name": "zhang",
     "last_name": "bairen"
   }
   
   # 通过copy_to字段查询
   GET demo3/_search
   {
     "query": {
       "match": {
         "full_name": "zhang"
       }
     }
   }
   ```

   

### **动态映射**

Dynamic Mapping 机制使我们不需要手动定义 Mapping，ES 会**自动根据文档信息来判断字段合适的类型**，但是有时候也会推算的不对，比如地理位置信息有可能会判断为 Text，当类型如果设置不对时，会导致一些功能无法正常工作，比如 Range 查询。

| 原始字段类型     |              ES字段类型 |                备注                 |
| :--------------- | ----------------------: | :---------------------------------: |
| null             |                  无字段 |                                     |
| true/false       |            boolean 类型 |                                     |
| 123.22           |              float 类型 |                                     |
| 122              |               long 类型 |                                     |
| object           |         object 对象类型 |                                     |
| array            |             object 类型 |        基于第一条数据的类型         |
| string           | text/keyword 双字段类型 | 5.x之后就是双字段类型，es没有string |
| date格式的字符串 |               date 类型 |                                     |



如果是新增加的字段，根据 Dynamic 的设置分为以下三种状况：

- 当 Dynamic 设置为 true 时，一旦有新增字段的文档写入，Mapping 也同时被更新。
- 当 Dynamic 设置为 false 时，索引的 Mapping 是不会被更新的，新增字段的数据无法被索引，也就是无法被搜索，但是信息会出现在 _source 中。
- 当 Dynamic 设置为 strict 时，文档写入时包含新增字段时，会写入失败。

另外一种是字段已经存在，这种情况下，ES 是不允许修改字段的类型的，因为 ES 是根据 Lucene 实现的倒排索引，一旦生成后就不允许修改，如果希望改变字段类型，必须使用 Reindex API 重建索引。

不能修改的原因是如果修改了字段的数据类型，会导致已被索引的无法被搜索，但是如果是增加新的字段，就不会有这样的影响。



**示例：以 dynamic 为 false 演示**

```json
# 创建映射
PUT demo4
{
  "mappings": {
    "properties": {
      "name":{
        "type": "text"
      }
    },
    "dynamic": false
  }
}

# 创建文档，添加新字段
POST demo4/_create/1
{
  "name": "xiaozhang",
  "sex": "man"
}

# 查询结果
GET demo4/_search
{
  "query": {
    "match": {
      "name": "xiaozhang"  # 查询到结果
    }
  }
}

GET demo4/_search
{
  "query": {
    "match": {
      "sex": "man"  # 查询结果为空
    }
  }
}
```



### 嵌套映射

> 当 field 的值是一个 json 对象，且需要制定具体的字段类型时需要使用 嵌套映射。

```json
# 创建映射
PUT demo5
{
  "mappings": {
    "properties": {
      "name":{
        "type": "text"
      },
      "sex":{
        "type": "boolean"
      },
      "score":{
        "properties": {
          "math":{
            "type": "byte"
          },
          "english":{
            "type": "byte"
          }
        }
      }
    }
  }
}

# 新增文档
POST demo5/_create/1
{
  "name": "zhangjian",
  "sex": true,
  "score": {
    "math": 95,
    "english": 98
  }
}

# 使用内层 field 查询
GET demo5/_search
{
  "query": {
    "match": {
      "score.math": 95
    }
  }
}

# ------------更好的选择是，使用 object 类型来表示json对象，不用担心内部值的类型--------
PUT demo6 
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "sex": {
        "type": "boolean"
      },
      "score": {
        "type": "object"
      }
    }
  }
}

POST demo6/_create/1
{
  "name": "zhangjian",
  "sex": true,
  "score": {
    "math": 95,
    "english": 98
  }
}

GET demo6/_search
{
  "query": {
    "match": {
      "score.math": 95
    }
  }
}
```



### 分片设置

> 索引的主分片和复制分片和mapping一样，是可以在创建索引时，主动配置的。
>
> 索引创建后，主分片的数量不可以再修改，复制分片可以继续增加。
>
> 索引创建后，在集群中默认的主分片是5，复制分片是1。

```json
# 创建索引并设置分片
PUT demo7
{
  "mappings": {
    "properties": {
      "name":{
        "type": "text"
      }
    }
  },
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 3
  }
}

# 查询分片信息
GET demo7/_settings

# 修改复制分片
PUT demo7/_settings
{
  "number_of_replicas": 5  # 如果这里更换为主分片 field ，修改会失败报错
}
```



## 索引

Elasticsearch最关键的就是提供强大的索引能力了，其实InfoQ的这篇[时间序列数据库的秘密(2)——索引](http://www.infoq.com/cn/articles/database-timestamp-02?utm_source=infoq&utm_medium=related_content_link&utm_campaign=relatedContent_articles_clk)写的非常好，我这里也是围绕这篇结合自己的理解进一步梳理下，也希望可以帮助大家更好的理解这篇文章。

Elasticsearch索引的精髓：

> 一切设计都是为了提高搜索的性能

另一层意思：为了提高搜索的性能，难免会牺牲某些其他方面，比如插入/更新，否则其他数据库不用混了。前面看到往Elasticsearch里插入一条记录，其实就是直接PUT一个json的对象，这个对象有多个fields，比如上面例子中的*name, sex, age, about, interests*，那么在插入这些数据到Elasticsearch的同时，Elasticsearch还默默[1](http://blog.pengqiuyuan.com/ji-chu-jie-shao-ji-suo-yin-yuan-li-fen-xi/#fn:1)的为这些字段建立索引--倒排索引，因为Elasticsearch最核心功能是搜索。

InfoQ那篇文章里说Elasticsearch使用的倒排索引比关系型数据库的B-Tree索引快，为什么呢？



### B-Tree索引

上大学读书时老师教过我们，二叉树查找效率是logN，同时插入新的节点不必移动全部节点，所以用树型结构存储索引，能同时兼顾插入和查询的性能。因此在这个基础上，再结合磁盘的读取特性(顺序读/随机读)，传统关系型数据库采用了B-Tree/B+Tree这样的数据结构：

<img src="./image-20211101155227593.png" alt="image-20211101155227593" style="zoom:67%;" />

为了提高查询的效率，减少磁盘寻道次数，将多个值作为一个数组通过连续区间存放，一次寻道读取多个数据，同时也降低树的高度。

### 倒排索引

<img src="./image-20211101155421996.png" alt="image-20211101155421996" style="zoom:67%;" />

示例:

```
| ID | Name | Age  |  Sex     |
| -- |:------------:| -----:| -----:| 
| 1  | Kate         | 24 | Female
| 2  | John         | 24 | Male
| 3  | Bill         | 29 | Male
```

ID是Elasticsearch自建的文档id，那么Elasticsearch建立的索引如下:

**Name:**

```
| Term | Posting List |
| -- |:----:|
| Kate | 1 |
| John | 2 |
| Bill | 3 |
```

**Age:**

```
| Term | Posting List |
| -- |:----:|
| 24 | [1,2] |
| 29 | 3 |
```

**Sex:**

```
| Term | Posting List |
| -- |:----:|
| Female | 1 |
| Male | [2,3] |
```

##### Posting List

Elasticsearch分别为每个field都建立了一个倒排索引，Kate, John, 24, Female这些叫term，而[1,2]就是**Posting List**。Posting list就是一个int的数组，存储了所有符合某个term的文档id。

看到这里，不要认为就结束了，精彩的部分才刚开始...

通过posting list这种索引方式似乎可以很快进行查找，比如要找age=24的同学，爱回答问题的小明马上就举手回答：我知道，id是1，2的同学。但是，如果这里有上千万的记录呢？如果是想通过name来查找呢？

##### Term Dictionary

Elasticsearch为了能快速找到某个term，将所有的term排个序，二分法查找term，logN的查找效率，就像通过字典查找一样，这就是**Term Dictionary**。现在再看起来，似乎和传统数据库通过B-Tree的方式类似啊，为什么说比B-Tree的查询快呢？

##### Term Index

B-Tree通过减少磁盘寻道次数来提高查询性能，Elasticsearch也是采用同样的思路，直接通过内存查找term，不读磁盘，但是如果term太多，term dictionary也会很大，放内存不现实，于是有了**Term Index**，就像字典里的索引页一样，A开头的有哪些term，分别在哪页，可以理解term index是一颗树：

<img src="./20211101155841.jpg" alt="aa" style="zoom:67%;" />

这棵树不会包含所有的term，它包含的是term的一些前缀。通过term index可以快速地定位到term dictionary的某个offset，然后从这个位置再往后顺序查找。

<img src="./20211101160024.jpg" alt="aa" style="zoom:67%;" />

所以term index不需要存下所有的term，而仅仅是他们的一些前缀与Term Dictionary的block之间的映射关系，再结合FST(Finite State Transducers)的压缩技术，可以使term index缓存到内存中。从term index查到对应的term dictionary的block位置之后，再去磁盘上找term，大大减少了磁盘随机读的次数。



> FSTs are finite-state machines that **map** a **term (byte sequence)** to an arbitrary **output**.
>
> FST是将一个 词语（字节序列）映射到任意输出的有限状态机。

假设我们现在要将mop, moth, pop, star, stop and top(term index里的term前缀)映射到序号：0，1，2，3，4，5(term dictionary的block位置)。最简单的做法就是定义个Map<string, integer="">，大家找到自己的位置对应入座就好了，但从内存占用少的角度想想，有没有更优的办法呢？答案就是：**FST**([理论依据在此，但我相信99%的人不会认真看完的](http://www.cs.nyu.edu/~mohri/pub/fla.pdf))

<img src="./20211101160121.jpg" alt="Alt text" style="zoom:67%;" />

⭕️表示一种状态

-->表示状态的变化过程，上面的字母/数字表示状态变化和权重

将单词分成单个字母通过⭕️和-->表示出来，0权重不显示。如果⭕️后面出现分支，就标记权重，最后整条路径上的权重加起来就是这个单词对应的序号。

FST以字节的方式存储所有的term，这种压缩方式可以有效的缩减存储空间，使得term index足以放进内存，但这种方式也会导致查找时需要更多的CPU资源。



### 压缩技巧

Elasticsearch里除了上面说到用FST压缩term index外，对posting list也有压缩技巧。 
小明喝完咖啡又举手了:"posting list不是已经只存储文档id了吗？还需要压缩？"

嗯，我们再看回最开始的例子，如果Elasticsearch需要对同学的性别进行索引(这时传统关系型数据库已经哭晕在厕所……)，会怎样？如果有上千万个同学，而世界上只有男/女这样两个性别，每个posting list都会有至少百万个文档id。 Elasticsearch是如何有效的对这些文档id压缩的呢？

##### Frame Of Reference

> 增量编码压缩，将大数变小数，按字节存储

首先，Elasticsearch要求posting list是有序的(为了提高搜索的性能，再任性的要求也得满足)，这样做的一个好处是方便压缩，看下面这个图例： <img src="./20211101160520.jpg" alt="Alt text" style="zoom:67%;" />

如果数学不是体育老师教的话，还是比较容易看出来这种压缩技巧的。

原理就是通过增量，将原来的大数变成小数仅存储增量值，再精打细算按bit排好队，最后通过字节存储，而不是大大咧咧的尽管是2也是用int(4个字节)来存储。

##### Roaring bitmaps（加强版 bitmap）

说到Roaring bitmaps，就必须先从bitmap说起。Bitmap是一种数据结构，假设有某个posting list：

[1,3,4,7,10]

对应的bitmap就是：

[1,0,1,1,0,0,1,0,0,1]

非常直观，用0/1表示某个值是否存在，比如10这个值就对应第10位，对应的bit值是1，这样用一个字节就可以代表8个文档id，旧版本(5.0之前)的Lucene就是用这样的方式来压缩的，但这样的压缩方式仍然不够高效，如果有1亿个文档，那么需要12.5MB的存储空间，这仅仅是对应一个索引字段(我们往往会有很多个索引字段)。于是有人想出了Roaring bitmaps这样更高效的数据结构。

Bitmap的缺点是存储空间随着文档个数线性增长，Roaring bitmaps需要打破这个魔咒就一定要用到某些指数特性：

将posting list按照65535为界限分块，比如第一块所包含的文档id范围在0~65535之间，第二块的id范围是65536~131071，以此类推。再用<商，余数>的组合表示每一组id，这样每组里的id范围都在0~65535内了，剩下的就好办了，既然每组id不会变得无限大，那么我们就可以通过最有效的方式对这里的id存储。

<img src="./20211101160557.jpg" alt="Alt text" style="zoom:67%;" />

细心的小明这时候又举手了:"为什么是以65535为界限?"

程序员的世界里除了1024外，65535也是一个经典值，因为它=2^16-1，正好是用2个字节能表示的最大数，一个short的存储单位，注意到上图里的最后一行“If a block has more than 4096 values, encode as a bit set, and otherwise as a simple array using 2 bytes per value”，如果是大块，用节省点用bitset存，小块就豪爽点，2个字节我也不计较了，用一个short[]存着方便。



### 联合索引

上面说了半天都是单field索引，如果多个field索引的联合查询，倒排索引如何满足快速查询的要求呢？

- 利用跳表(Skip list)的数据结构快速做“与”运算，或者
- 利用上面提到的bitset按位“与”

先看看跳表的数据结构：

<img src="./image-20211101160824782.png" alt="Alt text" style="zoom:67%;" />

将一个有序链表level0，挑出其中几个元素到level1及level2，每个level越往上，选出来的指针元素越少，查找时依次从高level往低查找，比如55，先找到level2的31，再找到level1的47，最后找到55，一共3次查找，查找效率和2叉树的效率相当，但也是用了一定的空间冗余来换取的。

假设有下面三个posting list需要联合索引：

<img src="./20211101160912.jpg" alt="Alt text" style="zoom:67%;" />

如果使用跳表，对最短的posting list中的每个id，逐个在另外两个posting list中查找看是否存在，最后得到交集的结果。

如果使用bitset，就很直观了，直接按位与，得到的结果就是最后的交集。



### 总结和思考

Elasticsearch的索引思路:

> 将磁盘里的东西尽量搬进内存，减少磁盘随机读取次数(同时也利用磁盘顺序读特性)，结合各种奇技淫巧的压缩算法，用及其苛刻的态度使用内存。

所以，对于使用Elasticsearch进行索引时需要注意:

- 不需要索引的字段，一定要明确定义出来，因为默认是自动建索引的
- 同样的道理，对于String类型的字段，不需要analysis的也需要明确定义出来，因为默认也是会analysis的
- 选择有规律的ID很重要，随机性太大的ID(比如java的UUID)不利于查询

关于最后一点，个人认为有多个因素:

其中一个(也许不是最重要的)因素: 上面看到的压缩算法，都是对Posting list里的大量ID进行压缩的，那如果ID是顺序的，或者是有公共前缀等具有一定规律性的ID，压缩比会比较高；

另外一个因素: 可能是最影响查询性能的，应该是最后通过Posting list里的ID到磁盘中查找Document信息的那步，因为Elasticsearch是分Segment存储的，根据ID这个大范围的Term定位到Segment的效率直接影响了最后查询的性能，如果ID是有规律的，可以快速跳过不包含该ID的Segment，从而减少不必要的磁盘读次数，具体可以参考这篇[如何选择一个高效的全局ID方案](http://blog.mikemccandless.com/2014/05/choosing-fast-unique-identifier-uuid.html)



## 分析器

### 1. 分析过程

分析(analysis)过程如下：

- 首先，将一个文本块划分为适用于倒排索引的独立的词条(term)
- 然后对这些词进行标准化，提高它们的’可搜索性’或’查全率’ 上面的工作就是由分析器(Analyzer)来完成的。

### 2. 分析器组成

分析器（Analyzer） 一般由三部分构成，字符过滤器（Character Filters）、分词器（Tokenizers）、分词过滤器（Token filters）。

<img src="./20211106192008.jpg" style="zoom:67%;" />

#### 2.1 字符过滤器

首先字符串要按顺序依次经过几个字符过滤器(Character Filter)。它们的任务就是在分词前对字符串进行一次处理。字符过滤器能够剔除HTML标记，或者转换 `&` 为 `and`。

#### 2.2 分词器

下一步，字符串经过分词器(Tokenizers)被分词成独立的词条(term)。一个简单的分词器可以根据空格或逗号将文本分成词条。

#### 2.3 分词过滤器

最后，每个词条都要按顺序依次经过几个分词过滤器(Token Filters)。这个过程可能会改变词条（例如，将 `Quick` 转为小写），删除词条（例如，删除像 `a`、`and`、`the` 这样的停用词），或者增加词条（例如，像 `jump` 和 `leap` 这样的同义词）。



几种常用分词器如下：

| 分词器           | 分词方式 |
| ---------------- | -------- |
| StandardAnalyzer | 单字分词 |
| CJKAnalyzer      | 二分法   |
| IKAnalyzer       | 词库分词 |

其中常用的是IKAnalyzer，但IK是第三方插件，需要安装。

IK分词器主要是针对 ES 内置的分词器对中文分词不友好，会讲中文每个字都分成一个 term，导致检索出很多低匹配度的文档。

ik分词器有以下两种模式：

- **ik_max_word**: 会将文本做最细粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合；
- **ik_smart**: 会做最粗粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”。





# 环境搭建



## 安装ES

1. 下载镜像

   ```shell
   docker pull elasticsearch:7.6.2
   ```

2. 创建挂载的目录

   ```shell
   mkdir -p /var/local/myapp/elasticsearch/config
   mkdir -p /var/local/myapp/elasticsearch/data
   mkdir -p /var/local/myapp/elasticsearch/plugins
   
   # 创建配置文件，添加如下内容
   echo "http.host: 0.0.0.0" >> /var/local/myapp/elasticsearch/config/elasticsearch.yml
   ```

3. 创建容器并启动

   ```shell
   docker run --name elasticsearch -p 9200:9200 -p 9300:9300  -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms256m -Xmx512m" -v /var/local/myapp/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /var/local/myapp/elasticsearch/data:/usr/share/elasticsearch/data -v /var/local/myapp/elasticsearch/plugins:/usr/share/elasticsearch/plugins -d elasticsearch:7.6.2
   
   其中elasticsearch.yml是挂载的配置文件，data是挂载的数据，plugins是es的插件，如ik，而数据挂载需要权限，需要设置data文件的权限为可读可写,需要下边的指令。
   chmod -R 777 要修改的路径
   
   -e "discovery.type=single-node" 设置为单节点
   特别注意：
   -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \ 测试环境下，设置ES的初始内存和最大内存，过大导致启动不了ES
   ```

4. 访问es

   http://121.4.47.229:9200/

   ```json
   {
     "name" : "fcfdae6beffa",
     "cluster_name" : "elasticsearch",
     "cluster_uuid" : "duhRwY6jSXewnyRlVcA8YA",
     "version" : {
       "number" : "7.6.2",
       "build_flavor" : "default",
       "build_type" : "docker",
       "build_hash" : "ef48eb35cf30adf4db14086e8aabd07ef6fb113f",
       "build_date" : "2020-03-26T06:34:37.794943Z",
       "build_snapshot" : false,
       "lucene_version" : "8.4.0",
       "minimum_wire_compatibility_version" : "6.8.0",
       "minimum_index_compatibility_version" : "6.0.0-beta1"
     },
     "tagline" : "You Know, for Search"
   }
   ```



## 安装Kibana

> kibana 是一款适用于 es 的 **数据可视化和管理工具**, 可以提供实时的直方图、线形图、饼状图和地图。
>
> 支持用户安全权限体系, 支持各种纬度的插件, 通常搭配 es、logstash 一起使用。

1. 下载镜像

   ```shell
   # kibana 的版本尽量和 es版本保持一致
   docker pull kibana:7.6.2
   ```

2. 启动镜像

   ```shell
   # 第一条添加了汉化环境变量
   # docker run -d --name kibana --link elasticsearch:elasticsearch -e "I18N_LOCALE=zh-CN" -p 5601:5601 kibana:7.6.2
   
   docker run -d --name kibana --link elasticsearch:elasticsearch -p 5601:5601 kibana:7.6.2
   ```

3. 访问kibana

   http://121.4.47.229:5601/app/kibana 



## 开启Basic权限认证

> es 7.x  版本开始，默认安装了 x-pack ，需要配置权限认证，其他端才可以访问es的node信息。

1. 修改 elastic search.yml 配置文件，加入如下信息

   ```shell
   action.destructive_requires_name: true
   xpack.security.enabled: true
   xpack.license.self_generated.type: basic
   xpack.security.transport.ssl.enabled: true
   
   # 跨域相关配置
   http.cors.enabled: true
   http.cors.allow-origin: "*"
   http.cors.allow-headers: Authorization,X-Requested-With,Content-Length,Content-Type
   
   # action.destructive_requires_name: true: 设置之后只限于使用特定名称来删除索引，使用_all 或者通配符来删除索引无效
   ```

2. 进入es容器内部，配置身份认证

   ```shell
   #系统自动生成密码
   ./bin/elasticsearch-setup-passwords auto
   
   #自定义密码，执行该命令后，会让你配置密码
   ./bin/elasticsearch-setup-passwords interactive
   ```

3. 重启elasticsearch服务

   ```shell
   docker restart xxxxxxxx
   
   # 再次访问是就需要加权限认证
   http://121.4.47.229:9200/?auth_user=elastic&auth_password=123456
   
   # 指定用户名和密码
   auth_user
   auth_password
   ```

4. 从新启动一个kibana容器，把认证信息给带上

   ```shell
   # 下面的启动方式带上了认证的账号密码，可以避免kibana使用时还要再web上输入密码。
   docker run --name kibana -e ELASTICSEARCH_HOSTS=http://elastic:Zj1340026934@121.4.47.229:9200 -p 5601:5601 -d kibana:7.6.2
   ```

5. 在kibana容器内部，修改配置

   ```shell
   vi config/kibana.yml
   
   # 为kibana访问es添加身份认证信息
   elasticsearch.username: "elastic"
   elasticsearch.password: "Zj1340026934"
   ```

6. 重启kibana服务



## IK分词器安装及使用

IK分词是 ES 的一个插件，下载插件在 plugins 目录解压，然后重启 ES 即可。

- 下载 ik分词器

  下载插件包： https://github.com/medcl/elasticsearch-analysis-ik/releases

  保持插件和 ES 的版本一致。

  如果在服务器端可直接wget下载即可：

  ```shell
  # 把版本号修改成自己需要的
  wget https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.6.2/elasticsearch-analysis-ik-7.6.2.zip
  ```

- 解压安装包

  ```shell
  # create plugin folder 
  cd your-es-root/plugins/ && mkdir ik
  
  # unzip plugin to folder 
  your-es-root/plugins/ik
  ```

- 重启服务器后，查看我们已经安装的插件

  ```shell
  # 重启es容器
  docker restart 容器名/容器号
  
  # kibana 查看插件
  GET _cat/plugins
  
  # ----返回值-----
  19407acd6473 analysis-ik 7.6.2
  ```

- 使用ik分词器示例

  ```json
  # 分析演示一：ik_smart
  POST _analyze
  {
    "text": "我喜欢听音乐",
    "analyzer": "ik_smart"
  }
  
  {
    "tokens" : [
      {
        "token" : "我",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "CN_CHAR",
        "position" : 0
      },
      {
        "token" : "喜欢",
        "start_offset" : 1,
        "end_offset" : 3,
        "type" : "CN_WORD",
        "position" : 1
      },
      {
        "token" : "听音乐",
        "start_offset" : 3,
        "end_offset" : 6,
        "type" : "CN_WORD",
        "position" : 2
      }
    ]
  }
  
  # 分析演示二：ik_max_word
  POST _analyze
  {
    "text": "我喜欢听音乐",
    "analyzer": "ik_max_word"
  }
  
  {
    "tokens" : [
      {
        "token" : "我",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "CN_CHAR",
        "position" : 0
      },
      {
        "token" : "喜欢",
        "start_offset" : 1,
        "end_offset" : 3,
        "type" : "CN_WORD",
        "position" : 1
      },
      {
        "token" : "听音乐",
        "start_offset" : 3,
        "end_offset" : 6,
        "type" : "CN_WORD",
        "position" : 2
      },
      {
        "token" : "听音",
        "start_offset" : 3,
        "end_offset" : 5,
        "type" : "CN_WORD",
        "position" : 3
      },
      {
        "token" : "音乐",
        "start_offset" : 4,
        "end_offset" : 6,
        "type" : "CN_WORD",
        "position" : 4
      }
    ]
  }
  
  # 创建映射演示
  # analyzer:指定添加数据的时候应该使用什么样的分词器
  # search_analyzer:使用关键词搜索的时候,应该使用什么样的分词器
  # 建立索引的分词器必须和搜索的分词器严格一致
  PUT demo_ik
  {
    "settings": {
      "analysis": {
        "analyzer": {
          "ik": {
            "tokenizer": "ik_max_word"
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "content":{
          "type": "text",
          "analyzer": "ik_max_word",  
          "search_analyzer": "ik_max_word"  
        }
      }
    }
  }
  
  ## 添加文档
  POST demo_ik/_create/1
  {
    "content": "北京欢迎你"
  }
  
  POST demo_ik/_create/2
  {
    "content": "中国的首都是北京"
  }
  
  ## 查询文档
  GET demo_ik/_search
  {
    "query": {
      "bool": {
        "must": [
          {
            "match_phrase": {
              "content": "北京"  # 成功匹配出两条文档
            }
          }
        ]
      }
    }
  }
  ```
  
  





## 遇到的问题

1. kibana 报错 Data too large

   ```json
   {"type":"error","@timestamp":"2020-09-27T05:26:12Z","tags":["warning","stats-collection"],
   "pid":426971,"level":"error","error":{"message":"[circuit_breaking_exception]
    [parent] Data too large, data for [<http_request>] would be [25712457296/23.9gb],
    which is larger than the limit of [24481313587/22.7gb], real usage: [25712456936/23.9gb],
    new bytes reserved: [360/360b], usages
   ```

   考虑是es空间不够，没有及时清理es的缓存，先清理一波：

   ```shell
   curl --user username:pwd  -XPOST 'http://es服务器的IP:9200/_cache/clear'
   ```

   然后配置elastic search.yml，并重启服务：

   ```shell
   # 避免发生OOM，发生OOM对集群影响很大的
   indices.breaker.total.limit: 55%
   
   # 有了这个设置，最久未使用（LRU）的 fielddata 会被回收为新数据腾出空间   
   indices.fielddata.cache.size: 25%
   
   # fielddata 断路器默认设置堆的  作为 fielddata 大小的上限。
   indices.breaker.fielddata.limit: 40%
   
   # request 断路器估算需要完成其他请求部分的结构大小，例如创建一个聚合桶，默认限制是堆内存
   indices.breaker.request.limit: 40%
   ```





# 文档操作

## 基础CRUD

| 操作类型 | 示例                                                   |
| -------- | ------------------------------------------------------ |
| Index    | PUT my_index/_doc/1                                    |
| Create   | PUT `my_index/_create/1` <br />POST `my_index/_create` |
| Read     | GET my_index/_doc/1                                    |
| Update   | POST my_index/_update/1                                |
| Delete   | Delete my_index/_doc/1                                 |

说明：

- Type 名，约定都用 _doc
- Create - 如果ID已经存在，会失败
- Index - 如果ID不存在，创建新的文档。否则，先删除现有的文档，再创建新的文档，版本会增加
- Update - 文档必须已经存在，更新只会对相应字段做增量修改



**示例：创建**

> - 支持自动生成文档ID和指定文档ID两种方式
> - 通过调用 `post /users/_doc` , 系统会自动生成 document id
> - 使用 `HTTP PUT user/_create/1` 创建时，URL中显示指定`_create`，此时如果该id已经存在，操作失败。
> - Index 和 Create 不一样的地方：如果文档不存在，就索引新的文档。否则现有的文档会被删除，新的文档被索引。版本信息 +1。

```json
# ----------指定文档id------------
PUT users/_create/1
{
  "user": "Jack",
  "date": "2021-11-03",
  "message": "A Singer"
}
{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}

# ----------自动生成文档id------------
POST users/_doc
{
  "user": "Tom",
  "date": "2021-11-03",
  "message": "A Postman"
}
{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "cljq43wBFG2xTUvurZOt",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 4,
  "_primary_term" : 1
}

# ----------使用 `HTTP PUT user/_create/1` 创建时，URL中显示指定`_create`，此时如果该id已经存在，操作失败-------
PUT users/_create/1
{
  "user": "Jack",
  "date": "2021-11-03",
  "message": "A Singer"
}
{
  "error" : {
    "root_cause" : [
      {
        "type" : "version_conflict_engine_exception",
        "reason" : "[1]: version conflict, document already exists (current version [1])",
        "index_uuid" : "tiwzb8GAT2mF2Ntaq1C2gg",
        "shard" : "0",
        "index" : "users"
      }
    ],
    "type" : "version_conflict_engine_exception",
    "reason" : "[1]: version conflict, document already exists (current version [1])",
    "index_uuid" : "tiwzb8GAT2mF2Ntaq1C2gg",
    "shard" : "0",
    "index" : "users"
  },
  "status" : 409
}

# -----------Index方式再次创建id为1的文档-------------
PUT users/_doc/1
{
  "user": "Jack Johns",
  "date": "2021-11-03",
  "message": "A Singer"
}
{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 2, # 版本更新
  "result" : "updated",  # 操作行为变成 updated，不再是 created，因为已经创建过
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 5,
  "_primary_term" : 1
}
```



**示例：查询**

> - 找到文档，返回 HTTP 200
>   - `_index/_type/_id`
>   - `_version`版本信息，同一个ID的文档，即使被删除，Version 号也会不断增加
>   - _scourc 中默认包含了文档的所有原始信息
> - 找不到文档，返回 HTTP 404

```json
# --------查询指定id的文档---------
GET users/_doc/1

{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 2,
  "_seq_no" : 5,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "user" : "Jack Johns",
    "date" : "2021-11-03",
    "message" : "A Singer"
  }
}

# --------查询指定id的文档的部分字段信息，多个field之间不能有空格---------
GET users/_doc/1?_source=user,message

{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 2,
  "_seq_no" : 5,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "message" : "A Singer",
    "user" : "Jack Johns"
  }
}

# ---------查询索引内部全部文档-----------
GET users/_search

GET users/_search # 查询全部文档时，下面 match_all 可以不写
{
  "query": {
    "match_all": {}
  }
}

{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "users",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "user" : "Jack Johns3",
          "date" : "2021-11-03",
          "message" : "A Singer",
          "age" : 20,
          "tag" : "帅气"
        }
      },
      {
        "_index" : "users",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "user" : "Jack Johns2",
          "date" : "2021-11-03",
          "message" : "A Singer",
          "age" : 19,
          "tag" : "有钱"
        }
      },
      {
        "_index" : "users",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "user" : "Jack Johns",
          "date" : "2021-11-03",
          "message" : "A Singer",
          "age" : 18,
          "tag" : "善良"
        }
      }
    ]
  }
}

# ---------按条件查询 match 匹配，不支持多个field同匹配----------
GET users/_search  # 查询 age=18 的文档
{
  "query": {
    "match": {
      "age": 18 
    }
  }
}

GET users/_search  # 查询 tag= 有钱 or 帅气 的文档
{
  "query": {
    "match": {
      "tag": "有钱 帅气"  # 文本类型的值可以在同一字符串中，用空格隔开，来匹配同一条件的多个值
    }
  }
}
```



**示例：更新**

> - PUT 方法更新，如果相同id的文档已经存在，那么将删除原文档，再重新创建一个
> - Update 方法不会删除原有的文档，而是实现真正的数据更新
> - POST 方法 /PayLoad 需要包含在 "doc" 中

```json
# --------直接使用PUT，将覆盖原来已有的数据------------
PUT users/_doc/1
{
  "user": "yuqiuyu"
}

GET users/_doc/1
{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 3,
  "_seq_no" : 9,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "user" : "yuqiuyu"
  }
}

# ----------使用POST update，将实现真正意义上的更新-----------
POST users/_update/1
{
  "doc": {
    "message": "Fucking"
  }
}

GET users/_doc/1
{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 4,
  "_seq_no" : 10,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "user" : "yuqiuyu",
    "message" : "Fucking"
  }
}
```



**示例：删除**

```json
# ----------------删除一个文档------------
DELETE users/_doc/1
{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 5,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 11,
  "_primary_term" : 1
}

GET users/_doc/1
{
  "_index" : "users",
  "_type" : "_doc",
  "_id" : "1",
  "found" : false
}

# ---------------删除一个索引------------
DELETE users
{
  "acknowledged" : true
}
```



## 批量创建

> _bulk 批量插入文档。每条指令包含两行：
>
> - 第一行指定请求与索引和类型,可以选择的请求有"create","index","delete","update", `_index`指定索引名, `_type`指定类型名, `_id`指定文档id
> - 第二行指定插入的内容，json 文本，包含文档的字段

示例：以批量新增作为演示

```json
# 创建一个索引
PUT demo9
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ik": {
          "tokenizer": "ik_max_word"
        }
      }
    }
  }, 
  "mappings": {
    "properties": {
      "name": {
        "type": "keyword"
      },
      "age": {
        "type": "byte"
      },
      "content": {
        "type": "text",
        "analyzer": "ik_smart"
      }
    }
  }
}

# 批量新增
POST demo9/_bulk
{"create": {"_id": 1}}
{"name": "阿强", "age": 18, "content": "今天是个好日子"}
{"create": {"_index": "demo9","_id": 2}}              # url 里面已经指明了 index 所以写不写都可以，type 也是默认的
{"name": "王也", "age": 18, "content": "风后奇门牛逼"}
{"create": {"_id": 3}}                                # id 也可以不写，但是系统生成的ID不方便后续使用和管理
{"name": "老天师", "age": 18, "content": "金光咒护体"}

POST demo9/_bulk
{"create": {"_id": 4}}
{"name": "武侯", "age": 18, "content": "诸葛武侯奇门异术"}
{"update": {"_id": 2}}
{"doc": {"content": "风后奇门继承人"}}  # 注意：update时要多一层 "doc"，和基础CRUD是一样的
```



## DSL高级检索

DSL 查询使用 JSON 格式的请求体与 Elasticsearch 交互，可以实现各种各样的查询需求。

DSL 查询主要包含两种类型的查询语句：

叶子查询语句 ： 用于查询特殊字段的特殊值，例如：match, term, range 等。
复合查询语句 ： 可以合并其他的叶子查询或复合查询，从而实现非常复杂的查询逻辑。

查询语句的执行结果依赖于它们是用于查询语境还是过滤语境。



### **全文查询（match）**

#### match_all

> match_all：全部匹配。match_all: {} ,全部匹配时，match_all 可省略不写

```json
# --------全部匹配，也就是查询ALL----------
GET users/_search
{
  "query": {
    "match_all": {}
  }
}

# 同上一条等价
GET users/_search
```



#### match

match 查询可操作文本、数值和日期类型的数据，分析它们并构建查询语句。

```json
GET users/_search
{
  "query": {
    "match": {
      "user": "Jack Johns"
    }
  }
}
```

**说明：**

- Elasticsearch 会先使用分析器分析 "John Smith" 为两个独立的项 "Jack" 和 "Johns"，然后再去构建查询，这里的 user 字段可以替换为任何你想查询的字段甚至是 _all 字段。

- match 属于 boolean 的类型，也就是说，分析器会对提供的查询文本进行分析并构建 boolean 查询语句。

- match 构建的 boolean 查询语句默认是逻辑或（or），即 "Jack" 和 "Johns"中任意一个词语匹配上都会被查询出来。

- 我们可以通过 operator 参数来改变这个默认行为，见下面示例：

  ```json
  GET users/_search
  {
    "query": {
      "match": {
        "user": {
          "query": "Jack Johns",
          "operator": "and"
        }
      }
    }
  }
  
  # user 是字段名称，query 参数的值是提供的查询文本，operator 参数用于设置 match 的逻辑（or 还是 and）。
  ```



#### match_phrase

match_phrase，即短语（词组）匹配，它会分析提供的查询文本并构建一个 phrase 查询。

match_phrase 用于精准的 phase 匹配。

```json
GET users/_search
{
  "query": {
    "match_phrase": {
      "user": "Jack Johns2"  # 精准的 phase 匹配，就意味着 Jack Johns2 被作为一个整体进行匹配
    }
  }
}
```



- **analyzer（分析器）**

  如果没有指定，默认使用字段的显式 mapping 中的定义，或者默认的 search analyzer。

  ```json
  GET users/_search
  {
    "query": {
      "match_phrase": {
        "user": {
          "query": "Jack Johns2",
          "analyzer": "standard"
        }
      }
    }
  }
  
  # 查看分析器分析结果
  GET _analyze
  {
    "analyzer": "standard", 
    "text": "中国"
  }
  
  {
    "tokens" : [
      {
        "token" : "中",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "<IDEOGRAPHIC>",
        "position" : 0
      },
      {
        "token" : "国",
        "start_offset" : 1,
        "end_offset" : 2,
        "type" : "<IDEOGRAPHIC>",
        "position" : 1
      }
    ]
  }
  ```

  

- **slop**

  指定词组之间的间隔最大是多少个字符，匹配文本中多个词组时使用。

  ```json
  POST users/_update/1
  {
    "doc": {
        "tag": "人之初性本善"
    }
  }
  
  GET users/_search
  {
    "query": {
      "match_phrase": {
        "tag": {
          "query": "人善",
          "slop": 4  # 刚好4个间隔是可以查到
        }
      }
    }
  }
  ```

  

#### match_phrase_prefix

match_phrase_prefix 和 match_phrase 类似，但 match_phrase_prefix 不是精准匹配，而是前缀匹配，它会对查询文本的最后一个字符后的内容进行通配符搜索。

```json
GET users/_search
{
  "query": {
    "match_phrase_prefix": {
      "user": "John"  # 此处能够匹配第二个字符的前缀。如果换成 ohn 那么久匹配不到结果了。
    }
  }
}
```



#### multi_match

multi_match 用于多字段匹配查询。即每个字段都要需要包含查询文本。

```json
PUT classmate/_doc/2
{
  "desc1": "张朝阳 创办搜狐",
  "desc2": "张雪峰 入职搜狐",
  "desc3": "李师师 是个美女",
  "desc4": "柳如是 是个义士"
}

GET classmate/_search
{
  "query": {
    "multi_match": {
      "query": "搜狐",
      "fields": ["desc1", "desc2"]
    }
  }
}
```



### Term-level 查询

我们知道，全文查询在执行查询之前，会先对提供的查询文本进行分析。

然而，Term-level 查询是直接查询倒排索引中的确切的值。

Term-level 查询通常用于结构化的数据，如数值、日期、枚举值或关键字，而不是文本（text）。



#### term

term 用于查询指定字段的倒排索引包含某个确切值的记录。

```json
# 创建索引映射
PUT demo8
{
  "mappings": {
    "properties": {
      "name":{
        "type": "keyword"
      },
      "sex": {
        "type": "boolean"
      }
    }
  }
}
# 新增文档
POST demo8/_create/1
{
  "name": "王重阳",
  "sex": true
}
# term查询
GET demo8/_search
{
  "query": {
    "term": {
      "name": {
        "value": "王重阳"
      }
    }
  }
}
```



#### terms

terms 和 term 类似，只不过提供的确切的值是数组。类似于 MySQL 的 in 条件。

```json
POST demo8/_create/2
{
  "name": "李莫愁",
  "sex": false
}

# terms查询
GET demo8/_search
{
  "query": {
    "terms": {
      "name": [
        "王重阳",
        "李莫愁"
      ]
    }
  }
}
```



#### exists

exists 返回term字段值不为 null 的记录。

```json
GET demo8/_search
{
  "query": {
    "exists": {
      "field": "name"  # 查询name字段部位null的文档
    }
  }
}
```



#### prefix

prefix 返回字段的 term 以确切的前缀（前缀不会被分析）开头的记录。

```json
GET demo8/_search
{
  "query": {
    "prefix": {
      "name": {
        "value": "王"  # 查询name字段以 王 开头的文档
      }
    }
  }
}
```



#### range

> range范围可供组合的选项：
>
> - gt : 大于
>
> - lt : 小于
>
> - gte : 大于等于
>
> - lte :小于等于

```json
GET users/_search
{
  "query": {
    "range": {
      "age": {
        "gt": 18
      }
    }
  }
}
```



#### wildcard

wildcard 指的是通配符查询。

支持的通配符主要有：

- \* 匹配 0 个或多个任意字符
- ? 匹配 1 个任意字符

```json
GET demo8/_search
{
  "query": {
    "wildcard": {
      "name": {
        "value": "王*"
      }
    }
  }
}
```



#### regexp

regexp 指的是正则查询。

```json
POST demo8/_create/3
{
  "name": "姬昌",
  "sex": true
}

GET demo8/_search
{
  "query": {
    "regexp": {
      "name": {
        "value": ".{3}"  # 匹配 name 是三个字符的文档
      }
    }
  }
}
```



#### fuzzy

fuzzy 指的是容差查询，即可以容忍确切的值和倒排索引中的 term 之间有误差。

```json
GET demo8/_search
{
  "query": {
    "fuzzy": {
      "name": {
        "boost": 2,
        "fuzziness": 2,
        "prefix_length": 0,
        "value": "阳"
      }
    }
  }
}
```



#### ids

ids 查询指的是根据文档的 id 来查询。

```json
GET demo8/_search
{
  "query": {
    "ids": {
      "values": [1, 2, 3]
    }
  }
}
```





### **bool查询**

> bool查询包含四种操作符，分别是**must,should,must_not,filter**。它们均是一种数组，数组里面是对应的判断条件。
>
> - must：必须匹配，与and等价。贡献算分
>
> - must_not：必须不匹配，与not等价，常过滤子句用，但不贡献算分
>
> - should：选择性匹配，至少满足一条，与 OR 等价。贡献算分
>
> - filter：过滤子句，必须匹配，但不贡献算分
>
>   过滤器，会查询对结果进行缓存，不会计算相关度，避免计算分值，执行速度非常快
>
>   filter也常和range范围查询一起结合使用，实现范围过滤

```json
# ------must查询-----------
GET users/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "age": 18
          }
        },
        {
          "match": {
            "message": "A Singer"
          }
        }
      ]
    }
  }
}

# -------must not查询--------
GET users/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "match": {
            "age": "18"
          }
        }
      ]
    }
  }
}

# --------should 查询---------
GET users/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "tag": "善良"
          }
        },
        {
          "match": {
            "age": 20
          }
        }
      ]
    }
  }
}

# ------- filter 查询----------
GET users/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "A Singer"
          }
        }
      ],
      "filter": [
        {
          "range": {
            "age": {
              "lt": 20
            }
          }
        }
      ]
    }
  }
}
```



### 指定返回字段

> 上面的查询都等价于 select * ，_source 的作用就是显示指定查询的字段。

```json
GET users/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "tag": "善良"
          }
        }
      ]
    }
  },
  "_source": ["user", "age"]
}
```



### **结果排序**

> sort 关键字

```json
GET users/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "age": {
        "order": "desc"  # 降序：desc；生序：asc。  不是所有数据类型都支持排序，text 就不支持
      }
    }
  ]
}
```



### 指定返回条数

> size 关键字

```json
GET users/_search
{
  "query": {
    "match": {
      "message": "A Singer"
    }
  },
  "size": 3  # 同limit
}
```



### 分页查询

> from 关键字指定起始位置，配合 size 关键字实现分页查询

```json
GET users/_search
{
  "query": {
    "match_all": {}
  },
  "from": 2,  # 从第几条开始，索引从0开始，包含。
  "size": 2   # 取几条。
}
```



### 高亮查询

> **highlight 关键字**: 可以让符合条件的文档中的 关键词 高亮
>
> **自定义高亮html标签**: 设置高亮html标签，默认是`<em>`标签，可以在highlight中使用`pre_tags`和`post_tags`属性自定义高亮显示的html标签，去替代默认的em标签。
>
> **多字段高亮:** 使用`require_field_match`设置为false，开启多个字段高亮，默认为true。

```json
GET users/_search
{
  "query": {
    "match": {
      "tag": "善良"
    }
  },
  "highlight": {
    "pre_tags": "<font style='color:red;'>",
    "post_tags": "</font>",
    "require_field_match": "false",  # 如果为true，则只会高亮上面 match 语句中的字段
    "fields": {
      "*": {}  # 高亮具体的字段。例如 "tag": {}，就只高亮tag，如果match中还有其他字段就不会高亮
    }
   }
  }
}
```



### 解决查询限制

- max_result_window：默认值是 10000，意味着查询参数中，from + size 不能大于 10000。修改参数配置，或在创建索引时直接设置。

  ```json
  PUT cars_news/_settings
  {
    "max_result_window": 99999999
  }
  ```

- Hits.total.value: 该值最大为 10000。是因为 track_total_hits 参数默认为 false。

  1. 如果需要精确知道命中的文档数量，此时应把track_total_hits设置为true,但用户需要清楚的明白，如果命中的文档数量很大，会影响查询性能，而且会消耗大量的内存，甚至存在内存异常的风险。
  2. 如果你确切知道不需要知道命中的结果数，则把track_total_hits设为false，这会提升查询性能。

  ```json
  GET cars_news/_search
  {
    "query": {
      "match_all": {}
    },
    "track_total_hits": true  // 查询时，显示指定该值为true
  }
  ```

  





## **聚合函数**

> *官方对聚合有四个关键字：`Metric(指标)、Bucket(桶)、Matrix(矩阵)、Pipeline(管道)`，在查询请求体中以aggregations语法来定义聚合分析，也可简写成aggs*
>
> ```text
> Metric(指标)：指标分析类型，如计算最大值、最小值、平均值等（对桶内的文档进行聚合分析的操作）
> Bucket(桶)：分桶类型，类似sql中的group by语法（满足特定条件的文档的集合）
> Pipeline(管道)：管道分析类型，基于上一级的聚合分析结果进行再分析
> Matrix(矩阵)：矩阵分析类型（聚合是一种面向数值型的聚合，用于计算一组文档字段中的统计信息）
> ```



### **指标（Mertric）聚合**

> ```text
> #1、单值分析，只输出一个分析结果
> min, max, avg, sum, cardinality
> 
> #2、多值分析，输出多个分析结果
> stats, extended_stats, percentile_rank, top hits
> ```

- **sum, avg关键字:** 计算从聚合文档中提取的数值的平均值

  ```json
  GET users/_search
  {
    "query": {
      "match": {
        "date": "2021-11-03"
      }
    },
    "aggs": {
      "my_sum": {  # 聚合的名字，自定义
        "sum": {	# 聚合的类型 min, max, avg, sum, cardinality 等
          "field": "age"  # 聚合的字段
        }
      },
      "my_avg":{
        "avg": {
          "field": "height"
        }
      }
    }
  }
  ```

- **min, max关键字：**求最大值、最小值

  ```json
  GET users/_search
  {
    "query": {
      "match": {
        "date": "2021-11-03"
      }
    },
    "aggs": {
      "my_max": {
        "max": {
          "field": "height"
        }
      },
      "my_min":{
        "min": {
          "field": "age"
        }
      }
    }
  }
  ```

- **stats 关键字**: 统计，请求后会直接显示各种聚合结果

  ```json
  GET users/_search
  {
    "query": {
      "match_all": {}
    },
    "aggs": {
      "my_stats": {
        "stats": {
          "field": "age"  # 只能是可以进行聚合分析的字段，比如 long、date等
        }
      }
    }
  }
  
  # 部分返回结果
    "aggregations" : {
      "my_stats" : {
        "count" : 4,
        "min" : 18.0,
        "max" : 20.0,
        "avg" : 18.75,
        "sum" : 75.0
      }
  ```

- **cardinality 关键字**: 求唯一值，即不重复的字段有多少（相当于sql中的distinct）

  ```json
  GET users/_search
  {
    "query":{
      "match_all": {}
    },
    "aggs": {
      "my_cardinality": {
        "cardinality": {
          "field": "tag.keyword"  # field 的类型不能是 text 类型
        }
      }
    }
  }
  ```

- **Percentiles 关键字**: 对指定字段的值按从小到大累计每个值对应的文档数的占比，返回指定占比比例对应的值，默认按照[1,5,25,50,75,95,99]来统计

  ```json
  GET users/_search
  {
    "query": {
      "match_all": {}
    },
    "aggs": {
      "my_percent": {
        "percentiles": {
          "field": "age",
          "percents": [
            50,
            99
          ],
          "keyed": false  # 默认情况下，keyed标志设置为true，它将唯一的字符串键与每个存储桶相关联，并将范围作为哈希而不是数组返回
        }
      }
    }
  }
  ```

  

### **分桶（Bucket）聚合**

> **Bucket**可以理解为一个桶，它会遍历文档中的内容，凡是符合某一要求的就放在一个桶中，分桶相当于sql中的group by, 关键字有Terms Aggregation，Filter Aggregation，Histogram Aggregation， Date Aggregation，Range Aggregation

- **Range Aggregation关键字:** 根据用户传递的范围参数作为桶，进行相应的聚合。在同一请求中，请求传递多组范围，每组范围作为一个桶

  ```json
  GET users/_search
  {
    "query": {
      "match": {
        "date": "2021-11-03"
      }
    },
    "aggs": {
      "my_bucket": {
        "range": {
          "field": "height",
          "ranges": [
            {
              "from": 170,
              "to": 178
            },
            {
              "from": 178,
              "to": 185
            }
          ]
        }
      }
    }
  }
  ```

- **Terms Aggregation关键字:** 根据某一项的每个唯一的值来聚合，每个 term 作为一个桶

  ```json
  GET users/_search
  {
    "query": {
      "match_all": {}
    },
    "aggs": {
      "my_ducket": {
        "terms": {
          "field": "user.keyword",
          "size": 3
        }
      }
    }
  }
  # 部分返回结果
    "aggregations" : {
      "my_ducket" : {
        "doc_count_error_upper_bound" : 0,
        "sum_other_doc_count" : 1,
        "buckets" : [
          {
            "key" : "Jack Johns",
            "doc_count" : 1
          },
          {
            "key" : "Jack Johns2",
            "doc_count" : 1
          },
          {
            "key" : "Jack Johns3",
            "doc_count" : 1
          }
        ]
      }
    }
  ```

- **Filter Aggregation关键字:** 指具体的域和具体的值，可以在Terms Aggregation 的基础上进行了过滤，只对特定的值进行了聚合

  ```json
  GET users/_search
  {
    "aggs": {
      "my_filter": {
        "filter": {
          "term": {
            "tag.keyword": "善良"
          }
        },
        "aggs": {
          "my_avg": {
            "avg": {
              "field": "age"
            }
          }
        }
      }
    }
  }
  ```

- **Filters Aggregation关键字:** Filter Aggregation 只能指定一个过滤条件，响应也只是单个桶。如果要对特定多个值进行聚合，使用Filters Aggragation

- **Histogram Aggregation关键字:** Histogram与Terms聚合类似，都是数据分组，区别是Terms是按照Field的值分组，而Histogram可以按照指定的间隔对Field进行分组

- **Date Aggregation关键字:** 分为Date Histogram Aggregation 和 Date Range Aggregation

  - **Date Histogram关键字:** 针对时间格式数据的直方图聚合，基本特性与Histogram Aggregation一致
  - **Date Range关键字:** 针对时间格式数据的直范围聚合，基本特性与Range Aggregation一致



### 聚合嵌套

```json
GET users/_search
{
  "query": {
    "match": {
      "date": "2021-11-03"
    }
  },
  "aggs": {
    "my_bucket": {
      "range": {
        "field": "age",
        "ranges": [
          {
            "from": 16,
            "to": 25
          }
        ]
      },
      "aggs": {
        "my_max": {
          "max": {
            "field": "height"
          }
        }
      }
    }
  }
}
```



## 索引操作

### 索引

查看服务器索引统计信息

```
GET _cat/indices?v  # 参数 v 表示显示title
```

![img](file:///Users/zhangjian/PycharmProjects/Practice/ElasticSearch/20211106185957.jpg?lastModify=1636780286)



### 插件

查看当前已经安装的插件

```
GET _cat/plugins?v

# 返回结果
name         component   version
19407acd6473 analysis-ik 7.6.2
```



### 映射

查看索引的映射信息

```
# 语法
GET 索引名/_mapping

# 示例
GET demo8/_mapping
{
  "demo8" : {
    "mappings" : {
      "properties" : {
        "name" : {
          "type" : "keyword"
        },
        "sex" : {
          "type" : "boolean"
        }
      }
    }
  }
}
```



### 配置

查看索引的映射信息

```
# 语法
GET 索引名/_settings

# 示例
GET demo8/_settings

{
  "demo8" : {
    "settings" : {
      "index" : {
        "creation_date" : "1636189857982",
        "number_of_shards" : "1",
        "number_of_replicas" : "1",
        "uuid" : "FDf9PNJlQg-JrUUXFJWZng",
        "version" : {
          "created" : "7060299"
        },
        "provided_name" : "demo8"
      }
    }
  }
}
```







# ES建议器

目前为止，浏览器都已经具备`Suggest as you type`功能，即在我们输入搜索的过程中，进行自动的补全或者纠错功能，协助用户输入更精确的关键词，提高搜索阶段的文档匹配程度。

**和聚合函数`aggs`不同的是，`suggest`是可以独立进行查询的，不需要依赖`query`**



## 建议器种类

根据需求不同elasticsearch设计了4种suggester，分别是：

- **词条建议器（term suggester）**：主要做纠正。对于给定文本的每个词条，该键议器从索引中抽取要建议的关键词，这对于短字段（如分类标签）很有效。
- **词组建议器（phrase suggester）**：主要做纠正。我们可以认为它是词条建议器的扩展，为整个文本（而不是单个词条）提供了替代方案，它考虑了各词条彼此临近出现的频率，使得该建议器更适合较长的字段，比如商品的描述。
- **完成建议器（completion suggester）**：该建议器根据词条的前缀，提供自动完成的功能（智能提示，有点最左前缀查询的意思），为了实现这种实时的建议功能，它得到了优化，工作在内存中。所以，速度要比之前说的match_phrase_prefix快的多！
- **上下文建议器（context suggester）**：它是完成建议器的扩展，允许我们根据词条或分类亦或是地理位置对结果进行过滤。

## 词条建议器（`term suggester`）

词条建议器接收输入的文本，对其进行分析并且分为词条，然后为每个词条提供一系列的建议。

```json
// 创建
PUT s1
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "standard"
      }
    }
  }
}

// 创建文档
POST s1/_bulk
{"create": {"_id": 1}}
{"title": "Lucene is cool"}
{"create": {"_id": 2}}
{"title": "elasticsearch builds on top of lucene"}
{"create": {"_id": 3}}
{"title": "Elasticsearch rocks"}
{"create": {"_id": 4}}
{"title": "elk rocks"}
{"create": {"_id": 5}}
{"title": "elasticsearch is rock solid"}
{"create": {"_id": 6}}
{"title": "elastic is a company behind ELK stack"}

// term 建议器查询
GET s1/_search
{
  "suggest": {
    "s1_suggest": {
      "text": "lune",
      "term": {
        "field": "title"
      }
    }
  }
}

// 相关返回结果
"suggest" : {
    "s1_suggest" : [
      {
        "text" : "lune",
        "offset" : 0,
        "length" : 4,
        "options" : [
          {
            "text" : "lucene",  // 建议结果是 lucene
            "score" : 0.5,
            "freq" : 2
          }
        ]
      }
    ]
  }
```

**建议器中的字段：**

- text：建议文本，建议文本是必需的选项，可以通过全局（多个建议器中查询相同的内容）或者按照单个建议器的格式来。
- field：从field字段中获取候选建议的字段。这是一个必需的选项，需要全局设置或根据建议设置。
- analyzer：用于分析建议文本的分析器。默认为建议字段的搜索分析器。
- size：建议文本标记返回的最大条目数，即返回结果options中的条数，默认是5条。
- sort：定义如何根据建议文本术语对建议进行排序。它有两个可能的值。
  - score，先按分数排序，然后按文档频率排序，再按术语本身排序。
  - frequency，首先按文档频率排序，然后按相似性分数排序，然后按术语本身排序。也可以理解为按照流行度排
- suggest_mode：控制建议的模式，有3个模式可选择。
  - missing，仅为不在索引中的建议文本术语提供建议。这是默认值。
  - popular，仅建议在比原始建议文本术语更多的文档中出现的建议。也就是说提供比原有输入词频更高的词条。
  - always，根据建议文本中的条款建议任何匹配的建议。说白了就是无论如何都会提供建议。
- lowercase_terms：在文本分析之后降低建议文本术语的大小写。
- min_word_length：建议文本术语必须具有的最小长度才能包含在内。默认为4.（旧名称min_word_len已弃用）。
- shard_size：设置从每个单独分片中检索的最大建议数。在减少阶段，仅根据size选项返回前N个建议。默认为该 size选项。将此值设置为高于该值的值size可能非常有用，以便以性能为代价获得更准确的拼写更正文档频率。由于术语在分片之间被划分，因此拼写校正频率的分片级文档可能不准确。增加这些将使这些文档频率更精确。
- max_inspections：用于乘以的因子， shards_size以便在碎片级别上检查更多候选拼写更正。可以以性能为代价提高准确性。默认为5。
- string_distance：用于比较类似建议术语的字符串距离实现。
- internal，默认值基于damerau_levenshtein，但高度优化用于比较索引中术语的字符串距离。
- damerau_levenshtein，基于Damerau-Levenshtein算法的字符串距离算法。
- levenshtein，基于Levenshtein编辑距离算法的字符串距离算法。
- jaro_winkler，基于Jaro-Winkler算法的字符串距离算法。
- ngram，基于字符n-gram的字符串距离算法。

**选择哪些词条被建议**

​		词条建议器使用了Lucene的错拼检查器模块，该模块会根据给定词条的编辑距离（es使用了叫做Levenstein edit distance的算法，其核心思想就是一个词改动多少字符就可以和另外一个词一致），从索引中返回最大编辑距离不超过某个值的那些词条。比如说为了从mik得到mick，需要加入一个字母（也就是说需要至少要改动一次），所以这两个词的编辑距离就是1。我们可以通过配置一系列的选项，来均衡灵活和性能：

- max_edits：最大编辑距离候选建议可以具有以便被视为建议。只能是介于1和2之间的值。任何其他值都会导致抛出错误的请求错误。默认为2。
- prefix_length：必须匹配的最小前缀字符的数量才是候选建议。默认为1.增加此数字可提高拼写检查性能。通常拼写错误不会出现在术语的开头。（旧名prefix_len已弃用）。
- min_doc_freq：建议应出现的文档数量的最小阈值。可以指定为绝对数字或文档数量的相对百分比。这可以仅通过建议高频项来提高质量。默认为0f且未启用。如果指定的值大于1，则该数字不能是小数。分片级文档频率用于此选项。
- max_term_freq：建议文本令牌可以存在的文档数量的最大阈值，以便包括在内。可以是表示文档频率的相对百分比数（例如0.4）或绝对数。如果指定的值大于1，则不能指定小数。默认为0.01f。这可用于排除高频术语的拼写检查。高频术语通常拼写正确，这也提高了拼写检查的性能。分片级文档频率用于此选项。

​        小结，term suggester首先将输入文本经过分析器（所以，分析结果由于采用的分析器不同而有所不同）分析，处理为单个词条，然后根据单个词条去提供建议，并不会考虑多个词条之间的关系。然后将每个词条的建议结果（有或没有）封装到options列表中。最后由建议器统一返回。



## 词组建议器（`phrase suggester`）

词组建议器和词条建议器一样，不过它不再为单个词条提供建议，而是为整个文本提供建议。

`phrase suggester`在`term suggester`的基础上，会考虑多个`term`之间的关系，比如是否同时出现索引的原文中，临近程度，词频等。

```json
// 使用上面创建的数据演示
// phrase suggest
GET s1/_search
{
  "suggest": {
    "s1_suggest": {
      "text": "lucen elasicseach rock",
      "phrase": {
        "field": "title",
        "highlight": {  // 词组建议器支持将建议结果高亮，这里的自定义标签是pre_tag和post_tag，区别于 query 的高亮。
          "pre_tag": "<font style='color: red;'>",
          "post_tag": "</font>"
        }
      }
    }
  }
}

// 结果
  "suggest" : {
    "s1_suggest" : [
      {
        "text" : "lucen elasicseach rock",
        "offset" : 0,
        "length" : 22,
        "options" : [
          {
            "text" : "lucene elasticsearch rock",
            "highlighted" : "<font style='color: red;'>lucene elasticsearch</font> rock",
            "score" : 0.025617568
          },
          {
            "text" : "lucen elasticsearch rock",
            "highlighted" : "lucen <font style='color: red;'>elasticsearch</font> rock",
            "score" : 0.017129304
          },
          {
            "text" : "lucene elasicseach rock",
            "highlighted" : "<font style='color: red;'>lucene</font> elasicseach rock",
            "score" : 0.014970658
          }
        ]
      }
    ]
  }
```



## 完成建议器（`completion suggester`）

完成建议器和上下文建议器可以帮助用户构建更快的 自动完成（一种功能，可以在用户输入时引导用户查看相关结果，从而提高搜索精度。），它们是基于`Lucene`的`suggest`建议模块而构建的，将数据保存在内存中的有限状态转移机中（FST）。FST实际上是一种图。它可以将词条以压缩和易于检索的方式来存储。

**为了告诉ES我们准备将建议存储在自动完成的FST中，需要在映射中定义一个字段并将其type类型设置为completion。在该类型的映射中还支持以下字段配置：**

- analyzer，要使用的索引分析器，默认为simple。
- search_analyzer，要使用的搜索分析器，默认值为analyzer。
- preserve_separators，保留分隔符，默认为true。 如果禁用，想找到以Foo Fighters开头的字段，建议使用foof。
- preserve_position_increments，启用位置增量，默认为true。如果禁用并使用停用词分析器The Beatles，如果您建议，可以从一个字段开始b。注意：您还可以通过索引两个输入来实现此目的，Beatles并且 The Beatles，如果您能够丰富数据，则无需更改简单的分析器。
- max_input_length，限制单个输入的长度，默认为50UTF-16代码点。此限制仅在索引时使用，以减少每个输入字符串的字符总数，以防止大量输入膨胀基础数据结构。大多数用例不受默认值的影响，因为前缀完成很少超过前缀长于少数几个字符。
  

```json
// 创建mapping
PUT s3
{
  "mappings": {
    "properties": {
      "title": {
        "type": "completion",
        "analyzer": "standard"
      }
    }
  }
}

POST s3/_bulk
{"create": {"_id": 1}}
{"title": "Lucene is cool"}
{"create": {"_id": 2}}
{"title": "elasticsearch builds on top of lucene"}
{"create": {"_id": 3}}
{"title": "Elasticsearch rocks"}
{"create": {"_id": 4}}
{"title": "elk rocks"}
{"create": {"_id": 5}}
{"title": "elasticsearch is rock solid"}
{"create": {"_id": 6}}
{"title": "elastic is a company behind ELK stack"}

// completion suggest
GET s3/_search
{
  "suggest": {
    "s3_suggest": {
      "text": "elk",
      "completion": {
        "field": "title"
      }
    }
  }
}

// 结果
  "suggest" : {
    "s3_suggest" : [
      {
        "text" : "elk",
        "offset" : 0,
        "length" : 3,
        "options" : [
          {
            "text" : "elk rocks",
            "_index" : "s3",
            "_type" : "_doc",
            "_id" : "4",
            "_score" : 1.0,
            "_source" : {
              "title" : "elk rocks"
            }
          }
        ]
      }
    ]
  }
```



### 在索引阶段提升相关性

在进行普通的索引时，输入的文本在索引和搜索阶段都会被分析。我们可以通过定义字段的多字段，配合`analyzer`和`search_analyzer`选项来进一步控制分析过程。

```json
// 创建映射
PUT s5 
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "suggest": {  // 该多字段的值和 title 是一样的，但数据类型和分析器单独定义，以便于后续建议
            "type": "completion",
            "analyzer": "keyword",
            "search_analyzer": "keyword"
          }
        }
      }
    }
  }
}

// 插入文档
POST s5/_create/1
{
  "title": "KFC"
}

POST s5/_create/2
{
  "title": "kfc"
}

// 查询
GET s5/_search
{
  "suggest": {
    "s5_suggest": {
      "text": "k",
      "completion": {
        "field": "title.suggest"
      }
    }
  }
}

// 结果
  "suggest" : {
    "s5_suggest" : [
      {
        "text" : "k",
        "offset" : 0,
        "length" : 1,
        "options" : [
          {  // 因为指定了索引和查询的解析器，都是按 keyword 索引和查询，所以 建议结果很精确。
            "text" : "kfc",
            "_index" : "s5",
            "_type" : "_doc",
            "_id" : "2",
            "_score" : 1.0,
            "_source" : {
              "title" : "kfc"
            }
          }
        ]
      }
    ]
  }
```

多数的情况下，我们将在单独的字段中、单独的索引中甚至是单独的集群中保存建议。这对于主搜索引擎的性能提升和扩展建议器都是非常有利的。

除此之外，还可以使用`input`和可选的`weight`属性，`input`是建议查询匹配的预期文本，`weight`是建议评分方式（也就是权重）。

```json
// 准备数据
PUT s6
{
  "mappings": {
    "properties": {
      "title": {
        "type": "completion"
      }
    }
  }
}

POST s6/_create/1
{
  "title": {
    "input": "blow",
    "weight": 5
  }
}

POST s6/_create/2
{
  "title": {
    "input": "block",
    "weight": 3
  }
}

GET s6/_search
{
  "suggest": {
    "s6_suggest": {
      "text": "blo",
      "completion": {
        "field": "title"
      }
    }
  }
}

// 查询结果
  "suggest" : {
    "s6_suggest" : [
      {
        "text" : "blo",
        "offset" : 0,
        "length" : 3,
        "options" : [  // 建议结果将按照权重排序返回
          { 
            "text" : "blow",
            "_index" : "s6",
            "_type" : "_doc",
            "_id" : "1",
            "_score" : 5.0,
            "_source" : {
              "title" : {
                "input" : "blow",
                "weight" : 5
              }
            }
          },
          {
            "text" : "block",
            "_index" : "s6",
            "_type" : "_doc",
            "_id" : "2",
            "_score" : 3.0,
            "_source" : {
              "title" : {
                "input" : "block",
                "weight" : 3
              }
            }
          }
        ]
      }
    ]
  }
```



### 在搜索阶段提升相关性

当在运行建议的请求时，可以决定出现哪些建议。

- **fuzzy**

  设置模糊建议，以对拼写进行容错。当开启模糊建议之后，可以设置下列参数来完成建议：
  - fuzziness，可以指定所允许的最大编辑距离。

  - min_length，指定什么长度的输入文本可以开启模糊查询。

  - prefix_length，假设若干开始的字符是正确的（比如block，如果输入blaw，该字段也认为之前输入的是对的），这样可以通过牺牲灵活性提升性能。

    ```json
    GET s6/_search
    {
      "suggest": {
        "s6_suggest": {
          "text": "bl",
          "completion": {
            "field": "title",
            "fuzzy": {
              "fuzziness": 2,
              "min_length": 3,
              "prefix_length": 2
            }
          }
        }
      }
    }
    ```

- **size**

  `size`参数指定返回建议数（默认为5），需要注意的是，`size must be positive`，也就是说`size`参数必须是积极的——非0非负数！

  ```json
  GET s6/_search
  {
    "suggest": {
      "s6_suggest": {
        "text": "bl",
        "completion": {
          "field": "title",
          "size": 1
        }
      }
    }
  }
  ```

- **_source**

  和`query`查询中的`_source`使用方式一样，控制返回哪些字段。

- **skip_duplicates**

  我们的建议可能是来自不同的文档，这其中就会有一些重复建议项，我们可以通过设置`skip_duplicates:true`来修改此行为，如果为`true`则会过滤掉结果中的重复建议文档：

  ```json
  GET s6/_search
  {
    "suggest": {
      "s6_suggest": {
        "text": "bl",
        "completion": {
          "field": "title",
          "skip_duplicates": true
        }
      }
    }
  }
  // 需要注意的是，该参数设置为true的话，可能会降低搜索速度，因为需要访问更多的建议结果项，才能过滤出来前N个。
  ```

- **prefix**

  前缀匹配建议。在进行suggest查询时，建议使用 `prefix` 替换 `text` ，区别于 query 查询。

  ```json
  GET s6/_search
  {
    "suggest": {
      "s6_suggest": {
        "prefix": "bl",
        "completion": {
          "field": "title"
        }
      }
    }
  }
  ```

- **正则**

  建议器除了支持常规的文本匹配，还支持正则匹配。这里上述的 text 转换成正则建议查询。

  ```json
  // suggest
  GET s6/_search
  {
    "suggest": {
      "s6_suggest": {
        "regex": "blo[w|ck]",
        "completion": {
          "field": "title"
        }
      }
    }
  }
  
  // 建议结果
    "suggest" : {
      "s6_suggest" : [
        {
          "text" : "blo[w|ck]",
          "offset" : 0,
          "length" : 9,
          "options" : [
            {
              "text" : "blow",
              "_index" : "s6",
              "_type" : "_doc",
              "_id" : "1",
              "_score" : 5.0,
              "_source" : {
                "title" : {
                  "input" : "blow",
                  "weight" : 5
                }
              }
            },
            {
              "text" : "block",
              "_index" : "s6",
              "_type" : "_doc",
              "_id" : "2",
              "_score" : 3.0,
              "_source" : {
                "title" : {
                  "input" : "block",
                  "weight" : 3
                }
              }
            }
          ]
        }
      ]
    }
  ```

  



# ES集群

## 相关概念

### Cluster 集群

一个 Elasticsearch 集群由一个或多个节点（Node）组成，每个集群都有一个共同的集群名称作为标识。



### Node 节点

一个 Elasticsearch 实例即一个 Node，一台机器可以有多个实例，正常使用下每个实例应该会部署在不同的机器上。Elasticsearch 的配置文件中可以通过 node.master、node.data 来设置节点类型。

- **node.master**：表示节点是否具有成为主节点的资格。真正的主节点，是由多个具有主节点资格的节点进行选举产生。
- **node.data**：表示节点是否存储数据。



### Shard 分片

每个索引有一个或多个分片，每个分片存储不同的数据。分片可分为主分片（ primary shard）和复制分片（replica shard），复制分片是主分片的拷贝。默认每个主分片有一个复制分片（默认一个索引创建后会有5个主分片，即：5主+5复制=10个分片），一个索引的复制分片的数量可以动态地调整，复制分片从不与它的主分片在同一个节点上（防止单点故障）。

复制分片有两个作用：

1. 提高恢复能力：当主分片挂掉时，某个复制分片可以变成主分片；

2. 提高性能：get 和 search 请求既可以由主分片又可以由复制分片处理；



### Health 健康

- **green**：所有主要分片和复制分片都可用

- **yellow**：所有主要分片可用，但不是所有复制分片都可用

- **red**：不是所有的主要分片都可用

> 当集群状态为 red，它仍然正常提供服务，它会在现有存活分片中执行请求，我们需要尽快修复故障分片，防止查询数据的丢失；



## 集群搭建

> 基于Docker

### 配置文件

> 准备 elasticsearch.yml 

- Master 结点配置

  ```shell
  # 集群名称，默认是 elasticsearch
  cluster.name: es-cluster
  
  # 节点名称
  node.name: node_01
  
  # 是否具有成为主节点的资格，默认 true
  node.master: true
  
  # 是否作为集群的数据节点，默认 true
  node.data: true
  
  # 配置访问本节点的地址，基于容器时，按如下配置
  network.host: 0.0.0.0
  network.publish_host: 121.4.47.229
  
  # 设置对外服务的http端口，默认为9200
  http.port: 9200
  
  # 当前节点用于集群间通信端口号，默认是9300
  transport.tcp.port: 9300
  
  # 配置所有用来组建集群的机器的IP地址
  discovery.zen.ping.unicast.hosts: ["121.4.47.229:9300", "121.4.47.229:9301","121.4.47.229:9302"]
  
  # 避免脑裂，集群节点数最少为 ceil(结点数/2) + 1。
  # 脑裂：split brain。意思是一个集群因为故障出现多个master，添加如下配置表示集群中至少有多个个结点才能选举出master，否则就会寻# 找新的集群加入。
  discovery.zen.minimum_master_nodes: 2
  
  # 解决跨域问题
  http.cors.enabled: true
  http.cors.allow-origin: "*"
  
  # 指定初始主结点从哪个结点启动
  cluster.initial_master_nodes: node_01
  ```

- Slave结点

  ```shell
  # 集群名称，要和主结点名称一样
  cluster.name: es-cluster
  node.name: node_02
  
  node.master: true
  node.data: true
  
  network.host: 0.0.0.0
  network.publish_host: 121.4.47.229
  
  # 端口不能和主结点重复
  http.port: 9201
  transport.tcp.port: 9301
  
  discovery.zen.ping.unicast.hosts: ["121.4.47.229:9300", "121.4.47.229:9301","121.4.47.229:9302"]
  discovery.zen.minimum_master_nodes: 2
  
  http.cors.enabled: true
  http.cors.allow-origin: "*"
  
  cluster.initial_master_nodes: node_01
  ```

  ```shell
  # 集群名称，要和主结点名称一样
  cluster.name: es-cluster
  node.name: node_03
  
  node.master: true
  node.data: true
  
  network.host: 0.0.0.0
  network.publish_host: 121.4.47.229
  
  http.port: 9202
  transport.tcp.port: 9302
  
  discovery.zen.ping.unicast.hosts: ["121.4.47.229:9300", "121.4.47.229:9301","121.4.47.229:9302"]
  discovery.zen.minimum_master_nodes: 2
  
  http.cors.enabled: true
  http.cors.allow-origin: "*"
  
  cluster.initial_master_nodes: node_01
  ```



### 启动容器

> 启动容器之前为 data 的挂在目录添加读写权限
>
> [root@VM-0-10-centos elasticsearch]# chmod -R 777 cluster/

```shell
# 主结点
docker run --name es01 -p 9200:9200 -p 9300:9300 -e ES_JAVA_OPTS="-Xms128m -Xmx128m" -v /var/local/myapp/elasticsearch/cluster/node_01/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /var/local/myapp/elasticsearch/cluster/node_01/data:/usr/share/elasticsearch/data -v /var/local/myapp/elasticsearch/cluster/node_01/plugins:/usr/share/elasticsearch/plugins -d elasticsearch:7.6.2

# 从结点
docker run --name es02 -p 9201:9201 -p 9301:9301 -e ES_JAVA_OPTS="-Xms128m -Xmx128m" -v /var/local/myapp/elasticsearch/cluster/node_02/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /var/local/myapp/elasticsearch/cluster/node_02/data:/usr/share/elasticsearch/data -v /var/local/myapp/elasticsearch/cluster/node_02/plugins:/usr/share/elasticsearch/plugins -d elasticsearch:7.6.2

docker run --name es03 -p 9202:9202 -p 9302:9302 -e ES_JAVA_OPTS="-Xms128m -Xmx128m" -v /var/local/myapp/elasticsearch/cluster/node_03/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /var/local/myapp/elasticsearch/cluster/node_03/data:/usr/share/elasticsearch/data -v /var/local/myapp/elasticsearch/cluster/node_03/plugins:/usr/share/elasticsearch/plugins -d elasticsearch:7.6.2


# 浏览器中查看结点启动情况，出现如下打印信息，表示集群启动成功
http://121.4.47.229:9200/_cat/nodes

121.4.47.229 74 95 5 1.24 1.36 0.94 dilm * node_01
121.4.47.229 62 95 5 1.24 1.36 0.94 dilm - node_03
121.4.47.229 54 95 5 1.24 1.36 0.94 dilm - node_02

# 启动kibana。因为是集群，可以任意连接一个端口
# 连接单个结点
docker run -it -d -e ELASTICSEARCH_HOSTS=http://121.4.47.229:9202 --name kk -p 5601:5601 kibana:7.6.2
```



### 遇到的问题

1. 容器启动报错：max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

   问题翻译过来就是：elasticsearch用户拥有的内存权限太小，至少需要262144；

   **解决：**

   在宿主机`/etc/sysctl.conf`文件最后添加一行：

   `vm.max_map_count=262144`

   添加后重新加载参数：

   `sysctl -p`

   **查看结果：**

   ```shell
   sysctl -a|grep vm.max_map_count
   
   # 结果
   vm.max_map_count = 262144
   ```

2. 容器启动时告警：WARNING: IPv4 forwarding is disabled. Networking will not work. 这将导致外网无法访问容器。

   **解决：**

   更改`/etc/sysctl.conf`中  net.ipv4.ip_forward=1

   更改后执行  systemctl restart network 即可





# ES其他

## Recovery

### 什么是recovery？

在elasticsearch中，recovery指的是一个索引的分片分配到另外一个节点的过程，一般在快照恢复、索引复制分片的变更、节点故障或重启时发生，由于master节点保存整个集群相关的状态信息，因此可以判断哪些分片需要再分配及分配到哪个节点，例如：

- 如果某个主分片在，而复制分片所在的节点挂掉了，那么master需要另行选择一个可用节点，将这个主分片的复制分片分配到可用节点上，然后进行主从分片的数据复制。
  如果某个主分片所在的节点挂掉了，复制分片还在，那么master会主导将复制分片升级为主分片，然后再做主从分片数据复制。
- 如果某个分片的主副分片都挂掉了，则暂时无法恢复，而是要等持有相关数据的节点重新加入集群后，master才能主持数据恢复相关操作。

但是，recovery过程要消耗额外的资源，CPU、内存、节点间的网络带宽等。可能导致集群的服务性能下降，甚至部分功能暂时无法使用，所以，有必要了解在recovery的过程和其相关的配置，来减少不必要的消耗和问题。



### 减少集群full restart造成的数据来回拷贝

有时候，可能会遇到es集群整体重启的情况，比如硬件升级、不可抗力的意外等，那么再次重启集群会带来一个问题：某些节点优先起来，并优先选举出了主节点，有了主节点，该主节点会立刻主持recovery的过程。但此时，这个集群数据还不完整（还有其他的节点没有起来），例如A节点的主分片对应的复制分片所在的B节点还没起来，但主节点会将A节点的几个没有复制分片的主分片重新拷贝到可用的C节点上。而当B节点成功起来了，自检时发现在自己节点存储的A节点主分片对应的复制分片已经在C节点上出现了，就会直接删除自己节点中“失效”的数据（A节点的那几个复制分片），这种情况很可能频繁出现在有多个节点的集群中。而当整个集群恢复后，其各个节点的数据分布，显然是不均衡的（先启动的节点把数据恢复了，后起来的节点内删除了无效的数据），这时，master就会触发Rebalance的过程，将数据在各个节点之间挪动，这个过程又消耗了大量的网络流量。所以，我们需要合理的设置recovery相关参数来优化recovery过程。

- 在集群启动过程中，一旦有了多少个节点成功启动，就执行recovery过程，这个命令将master节点（有master资格的节点）和data节点都算在内。

```
gateway.expected_nodes: 3
```

- 有几个master节点启动成功，就执行recovery的过程。

```
gateway.expected_master_nodes: 3
```

- 有几个data节点启动成功，就执行recovery的过程。

```
gateway.expected_data_nodes: 3
```

当集群在期待的节点数条件满足之前，recovery过程会等待`gateway.recover_after_time`指定的时间，一旦等待超时，则会根据以下条件判断是否执行recovery的过程：

```
gateway.recover_after_nodes: 3    # 3个节点（master和data节点都算）启动成功
gateway.recover_after_master_nodes: 3  # 3个有master资格的节点启动成功
gateway.recover_after_data_nodes: 3   # 3个有data资格的节点启动成功
```

上面三个配置满足一个就会执行recovery的过程。
如果有以下配置的集群：

```
gateway.expected_data_nodes: 10
gateway.recover_after_time: 5m
gateway.recover_after_data_nodes: 8
```

此时的集群在5分钟内，有10个data节点都加入集群，或者5分钟后有8个以上的data节点加入集群，都会启动recovery的过程。



### 减少主副本之间的数据复制

如果不是full restart，而是重启单个节点，也会造成不同节点之间来复制，为了避免这个问题，可以在重启之前，关闭集群的`shard allocation`。

```
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.enable":"none"
  }
}
```

当节点重启后，再重新打开：

```
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.enable":"all"
  }
}
```

这样，节点重启后，尽可能的从本节点直接恢复数据。但是在es1.6版本之前，既使做了以上措施，仍然会出现大量主副分片之间的数据拷贝，从面上看，这点让人很不理解，主副分片数据是完全一致的，在节点重启后，直接从本节点的副本重恢复数据就好了呀，为什么还要再从主分片再复制一遍呢？原因是在于recovery是简单的对比主副分片的segment file（分段文件）来判断哪些数据一致是可以本地恢复，哪些不一致的需要重新拷贝的。而不同节点的segment file是完全独立运行的，这可能导致主副本merge的深度不完全一致，从而造成即使文档集完全一样，而产生的segment file却不完全一样。
为了解决这个问题，在es1.6版本之后，加入了synced flush（同步刷新）新特性，对于5分钟没有更新过的shard，会自动synced flush一下，其实就是为对应的shard加入一个synced flush id，这样在节点重启后，先对比主副shard的synced flush id，就可以知道两个shard是否完全相同，避免了不必要的segment file拷贝。
需要注意的是synced flush只对冷索引有效，对于热索引（5分钟内有更新的索引）无效，如果重启的节点包含有热索引，那还是免不了大量的拷贝。如果要重启一个包含大量热索引的节点，可以按照以下步骤执行重启过程，可以让recovery过程瞬间完成：

- 暂停数据写入
- 关闭集群的shard allocation
- 手动执行 `POST /_flush/synced`
- 重启节点
- 重新开启集群的shard allocation
- 等待recovery完成，当集群的health status是green后
- 重新开启数据写入



### 特大热索引为何恢复慢

对于冷索引，由于数据不再更新（对于elasticsearch来说，5分钟，很久了），利用synced flush可以快速的从本地恢复数据，而对于热索引，特别是shard很大的热索引，除了synced flush派不上用场，从而需要大量跨节点拷贝segment file以外，translog recovery可能是导致慢的更重要的原因。
我们来研究下这个translog recovery是什么鬼！
当节点重启后，从主分片恢复数据到复制分片需要经历3个阶段：

- 第一阶段，对于主分片上的segment file做一个快照，然后拷贝到复制分片所在的节点，在数据拷贝期间，不会阻塞索引请求，新增的索引操作会记录到translog中（理解为于临时文件）。
- 第二阶段，对于translog做一个快照，此快照包含第一阶段新增的索引请求，然后重放快照里的索引操作，这个阶段仍然不会阻塞索引请求，新增索引操作记录到translog中。
- 第三阶段，为了能达到主副分片完全同步，阻塞新索引请求，然后重放上一阶段新增的translog操作。

由此可见，在recovery过程完成之前，translog是不能被清除掉的。如果shard比较大，第一阶段会耗时很长，会导致此阶段产生的translog很大，重放translog要比简单的文件拷贝耗时更长，因此第二阶段的translog耗时也显著的增加了。等到了第三阶段，需要重放的translog可能会比第二阶段更多。要命的是，第三阶段是会阻塞新索引（写入）请求的，在对写入实时性要求很高的场合，这就会导致性能下降，非常影响用户体验。因此，要加快特大热索引恢复速度，最好是参照上一节中的方式：

- 暂停数据写入。
- 手动synced flush。
- 等待数据恢复完成后。
- 重新恢复数据写入。

这样就会把数据延迟影响降到最低。



## 打分机制

**确定文档和查询有多么相关的过程被称为打分（scoring）**。



### 文档打分机制：TF-IDF

`Lucene`和`es`的打分机制是一个公式。将查询作为输入，使用不同的手段来确定每一篇文档的得分，将每一个因素最后通过公式综合起来，返回该文档的最终得分。这个综合考量的过程，就是我们希望相关的文档被优先返回的考量过程。在`Lucene`和`es`中这种相关性称为得分。
在开始计算得分之前，`es`使用了被搜索词条的频率和它有多常见来影响得分，从两个方面理解：

- 一个词条在某篇文档中出现的次数越多，该文档就越相关。
- 一个词条如果在不同的文档中出现的次数越多，它就越不相关！

我们称之为`TF-IDF`，`TF`是词频（term frequency），而`IDF`是逆文档频率（inverse document frequency）。



#### 词频：TF

考虑一篇文档得分的首要方式，是查看一个词条在文档中出现的次数，比如某篇文章围绕`es`的打分展开的，那么文章中肯定会多次出现相关字眼，当查询时，我们认为该篇文档更符合，所以，这篇文档的得分会更高。
闲的蛋疼的可以`Ctrl + f`搜一下相关的关键词（es，得分、打分）之类的试试。



#### 逆文档频率：IDF

相对于词频，逆文档频率稍显复杂，如果一个词条在索引中的不同文档中出现的次数越多，那么它就越不重要。
来个例子，示例[地址](http://www.kekenet.com/read/201904/583147.shtml)：

```
The rules-which require employees to work from 9 am to 9 pm
In the weeks that followed the creation of 996.ICU in March
The 996.ICU page was soon blocked on multiple platforms including the messaging tool WeChat and the UC Browser.
```

假如`es`索引中，有上述3篇文档：

- 词条`ICU`的文档频率是`2`，因为它出现在2篇文档中，文档的逆源自得分乘以`1/DF`，`DF`是该词条的文档频率，这就意味着，由于`ICU`词条拥有更高的文档频率，所以，它的权重会降低。
- 词条`the`的文档频率是`3`，它在3篇文档中都出现了，注意：**尽管`the`在后两篇文档出都出现两次，但是它的词频是还是`3`，因为，逆文档词频只检查词条是否出现在某篇文档中，而不检查它在这篇文档中出现了多少次，那是词频该干的事儿**。

逆文档词频是一个重要的因素，用来平衡词条的词频。比如我们搜索`the 996.ICU`。单词`the`几乎出现在所有的文档中（中文中比如`的`），如果这个鬼东西要不被均衡一下，那么`the`的频率将完全淹没`996.ICU`。所以，逆文档词频就有效的均衡了`the`这个常见词的相关性影响。以达到实际的相关性得分将会对查询的词条有一个更准确地描述。
当词频和逆文档词频计算完成。就可以使用`TF-IDF`公式来计算文档的得分了。



#### Lucene评分公式

之前的讨论`Lucene`默认评分公式被称为`TF-IDF`，一个基于词频和逆文档词频的公式。`Lucene`实用评分公式如下：

[![img](https://img2018.cnblogs.com/blog/1168165/201904/1168165-20190417002013739-30143345.png)](https://img2018.cnblogs.com/blog/1168165/201904/1168165-20190417002013739-30143345.png)

你以为我会着重介绍这个该死的公式？！
我只能说，词条的词频越高，得分越高；相似地，索引中词条越罕见，逆文档频率越高，其中再加商调和因子和查询标准化，调和因子考虑了搜索过多少文档以及发现了多少词条；查询标准化，是试图让不同的查询结果具有可比性，这显然.....很困难。
我们称这种默认的打分方法是`TF-IDF`和向量空间模型（vector space model）的结合。



### 其他的打分机制

除了`TF-IDF`结合向量空间模型的实用评分模式，是`es`和`Lucene`最为主流的评分机制，但这并不是唯一的，除了`TF-IDF`这种实用模型之外，其他的模型包括：

- Okapi BM25。
- 随机性分歧（Divergence from randomness），即DFR相似度。
- LM Dirichlet相似度。
- LM Jelinek Mercer相似度。

这里简要的介绍`BM25`几种主要设置，即`k1`、`b`和`discount_overlaps`：

- k1和b是数值的设置，用于调整得分是如何计算的。
- k1控制对于得分而言词频（TF）的重要性。
- b是介于`0 ~ 1`之间的数值，它控制了文档篇幅对于得分的影响程度。
- 默认情况下，`k1`设置为`1.2`，而`b`则被设置为`0.75`
- `discount_overlaps`的设置用于告诉`es`，在某个字段中，多少个分词出现在同一位置，是否应该影响长度的标准化，默认值是`true`。



#### 配置BM25打分模型

##### 简要配置BM25

`BM25`是一种基于概率的打分框架，配置示例如下：

```json
PUT w2
{
  "mappings": {
    "doc": {
      "properties": {
        "title": {
          "type": "text",
          "similarity": "BM25"
        }
      }
    }
  }
}
```



##### settings配置BM25

```json
PUT w3
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer":"ik_smart"
      }
    },
    "similarity": {
      "my_custom_similarity": {
        "type": "BM25",
        "k1": 1.2,
        "b": 0.75,
        "discount_overlaps": false
      }
    }
  },
  "mappings": {
    "doc": {
      "properties": {
        "title": {
          "type": "text",
          "similarity":"my_custom_similarity"
        }
      }
    }
  }
}
```



##### 配置全局打分模型

如果我们要使用某种特定的打分模型，并且希望应用到全局，那么就在`elasticsearch.yml`配置文件中加入：

```shell
index.similarity.default.type: BM25
```



### boosting

`boosting`是一个用来修改文档相关性的程序。`boosting`有两种类型：

- 索引的时候，比如我们在定义mappings的时候。
- 查询一篇文档的时候。

以上两种方式都可以提升一个篇文档的得分。需要注意的是：**在索引期间修改的文档boosting是存储在索引中的，要想修改boosting必须重新索引该篇文档**。



#### 索引期间的boosting

```json
PUT w4
{
  "mappings": {
    "doc": {
      "properties": {
        "name": {
          "boost": 2.0,
          "type": "text"
        },
        "age": {
          "type": "long"
        }
      }
    }
  }
}
```

在创建索引时制定了boost，可以为后续所新增的文档都加上boost。但不推荐这样做。

原因之一是因为一旦映射建立完成，那么所有`name`字段都会自动拥有一个`boost`值。要想修改这个值，那就必须重新索引文档。另一个原因是，`boost`值是以降低精度的数值存储在`Lucene`内部的索引结构中。只有一个字节用于存储浮点型数值（存不下就损失精度了），所以，计算文档的最终得分时可能会损失精度。

最后，`boost`是应用与词条的。因此，再被`boost`的字段中如果匹配上了多个词条，就意味着计算多次的`boost`，这将会进一步增加字段的权重，可能会影响最终的文档得分。



#### 查询期间的boosting

在`es`中，几乎所有的查询类型都支持`boost`，正如你想象的那些`match、multi_match`等等。

```json
GET w5/doc/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "title":{
              "query": "elasticserach rocks",
              "boost": 2.5
            }
          }
        },
        {
          "match": {
            "content": "elasticserach rocks"
          }
        }
      ]
    }
  }
}
// 就对于最终得分而言，加了boost的title查询更有影响力。也只有在bool查询中，boost更有意义。

GET w5/doc/_search
{
  "query": {
    "multi_match": {
      "query": "elasticserach rocks",
      "fields": ["title", "content"],
      "boost": 2.5
    }
  }
}
// boost也可以用于multi_match查询。

GET w5/doc/_search
{
  "query": {
    "multi_match": {
      "query": "elasticserach rocks",
      "fields": ["title^3", "content"]
    }
  }
}
// 我们还可以使用特殊的语法，只为特定的字段指定一个boost。通过在字段名称后添加一个^符号和boost的值。告诉es只需对那个字段进行boost。
```

需要注意的是：

​		在使用`boost`的时候，无论是字段或者词条，都是按照相对值来`boost`的，而不是乘以乘数。如果对于所有的待搜索词条`boost`了同样的值，那么就好像没有`boost`一样（废话，就像大家都同时长高一米似的）！因为Lucene会标准化`boost`的值。如果`boost`一个字段`4`倍，不是意味着该字段的得分就是乘以`4`的结果。所以，如果你的得分不是按照严格的乘法结果，也不要担心。



#### explain 查看评分计算

通过指定`explain=true`来查看评分的详细计算过程。

```json
// 指定size=1，方便分析结果
GET s1/_search
{
  "query": {
    "match": {
      "title": {
        "query": "工",
        "boost": 2
      }
    }
  },
  "explain": true,
  "size": 1
}

// 打印结果
{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.4676589,
    "hits" : [
      {
        "_shard" : "[s1][0]",
        "_node" : "3-PXa9L3QbO6CJ6zKLbrXg",
        "_index" : "s1",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.4676589, // 评分是被 boost 2 的结果，修改 boost 这里也会发生变化
        "_source" : {
          "title" : "打工仔",
          "sex" : 1
        },
        "_explanation" : {
          "value" : 0.4676589,
          "description" : "weight(title:工 in 0) [PerFieldSimilarity], result of:",
          "details" : [
            {
              "value" : 0.4676589,
              "description" : "score(freq=1.0), computed as boost * idf * tf from:",
              "details" : [
                {
                  "value" : 4.4,
                  "description" : "boost",
                  "details" : [ ]
                },
                {
                  "value" : 0.18232156,
                  "description" : "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
                  "details" : [
                    {
                      "value" : 2,
                      "description" : "n, number of documents containing term",
                      "details" : [ ]
                    },
                    {
                      "value" : 2,
                      "description" : "N, total number of documents with field",
                      "details" : [ ]
                    }
                  ]
                },
                {
                  "value" : 0.58295965,
                  "description" : "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                  "details" : [
                    {
                      "value" : 1.0,
                      "description" : "freq, occurrences of term within document",
                      "details" : [ ]
                    },
                    {
                      "value" : 1.2,
                      "description" : "k1, term saturation parameter",
                      "details" : [ ]
                    },
                    {
                      "value" : 0.75,
                      "description" : "b, length normalization parameter",
                      "details" : [ ]
                    },
                    {
                      "value" : 3.0,
                      "description" : "dl, length of field",
                      "details" : [ ]
                    },
                    {
                      "value" : 6.5,
                      "description" : "avgdl, average length of field",
                      "details" : [ ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    ]
  }
}

```

**过程分析：**

从上面的`_explanation`中可以看到计算过程分为三步：

- 计算TF。

  ```json
  "value" : 0.58295965,
  "description" : "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
  ```

- 计算IDF。

  ```json
  "value" : 0.18232156,
  "description" : "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
  ```

- 根据boost计算最终得分。

  ```json
  "value" : 0.4676589,
  "description" : "score(freq=1.0), computed as boost * idf * tf from:",
  ```



需要注意的是，`explain`的特性会给`es`带来额外的性能开销。所以，除了在调试时可以使用，生产环境下，应避免使用`explain`。





## 路由机制

ES中的路由（routing）机制决定一个document存储到索引的哪个shard上面去，即文档到shard的路由。计算公式为：

```shell
shard_num = hash(_routing) % num_primary_shards
```

其中`_routing`是路由字段的值，默认使用文档的ID字段：`_id`。如果我们想自己控制数据的路由规则的话，那可以修改这个默认值。修改的方式非常简单，只需要在插入数据的时候指定路由的key即可。虽然使用简单，但有许多的细节需要注意。

**不指定路由：**

```json
PUT route_demo // 创建有两个主分片的索引 route_demo
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 0
  }
}

POST route_demo/_create/a?refresh  // 新增id为a的文档。refresh的作用是立刻刷新shard中的文档，方便后面查看
{
  "data": "A"
}

GET _cat/shards/route_demo?v  // 可以看到文档被保存到其中一个分片中
--------------------------------
index      shard prirep state   docs store ip           node
route_demo 1     p      STARTED    0  230b 121.4.47.229 node_03
route_demo 0     p      STARTED    1 4.9kb 121.4.47.229 node_02

POST route_demo/_create/b?refresh  // 再添加一条
{
  "data": "B"
}

GET _cat/shards/route_demo?v  // 因为没有指定路由，所以根据_id值分配到了另一个
-------------------------------
index      shard prirep state   docs store ip           node
route_demo 1     p      STARTED    1 4.9kb 121.4.47.229 node_03
route_demo 0     p      STARTED    1 4.9kb 121.4.47.229 node_02
```



**指定路由：**

```json
POST route_demo/_create/c?routing=key1&refresh  // 自定义routing的值为key1
{
  "data": "c"
}

GET _cat/shards/route_demo?v  // 可见，路由key1将数据保存到了shard 0 上
---------------------------------------
index      shard prirep state   docs  store ip           node
route_demo 1     p      STARTED    1 10.7kb 121.4.47.229 node_03
route_demo 0     p      STARTED    2  8.9kb 121.4.47.229 node_02

GET route_demo/_search  // 部分查询数据
----------------------------------------
      {
        "_index" : "route_demo",
        "_type" : "_doc",
        "_id" : "c",
        "_score" : 1.0,
        "_routing" : "key1",  // 指定路由时，返回结果就会有这样的字段
        "_source" : {
          "data" : "c"
        }
      }

// -------再次插入id是a的文档，本次指定路由--------
PUT route_demo/_doc/a?routing=key1&refresh
{
  "data": "A rewrite with routing"
}

// -------返回值-----
{
  "_index" : "route_demo",
  "_type" : "_doc",
  "_id" : "a",
  "_version" : 4,
  "result" : "updated",  // 可以看到，这里是updated，不是created
  "forced_refresh" : true,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 4,
  "_primary_term" : 1
}

GET _cat/shards/route_demo?v  // 带路由的文档a，仍然保存在 shard 0 上。这里可以解释上面为什么是updated，因为shard 0上已经有同一个id了
---------------------------------
index      shard prirep state   docs store ip           node
route_demo 1     p      STARTED    1   6kb 121.4.47.229 node_03
route_demo 0     p      STARTED    2 8.2kb 121.4.47.229 node_02

// -------再次插入id是b的文档，本次指定路由--------
PUT route_demo/_doc/b?routing=key1&refresh
{
  "data": "B rewrite with routing"
}

// -------返回值--------
{
  "_index" : "route_demo",
  "_type" : "_doc",
  "_id" : "b",
  "_version" : 1,
  "result" : "created",  // 这里是created
  "forced_refresh" : true,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 5,
  "_primary_term" : 1
}

GET _cat/shards/route_demo?v  // 带路由的文档b，仍然保存在 shard 0 上。此时shard 1 上也保存着一个id是b的文档
------------------------------
index      shard prirep state   docs store ip           node
route_demo 1     p      STARTED    1   6kb 121.4.47.229 node_03
route_demo 0     p      STARTED    3 7.9kb 121.4.47.229 node_02

GET route_demo/_search
-----------部分结果-----------
      {
        "_index" : "route_demo",
        "_type" : "_doc",
        "_id" : "b",
        "_score" : 1.0,
        "_routing" : "key1",
        "_source" : {
          "data" : "B rewrite with routing"
        }
      },
      {
        "_index" : "route_demo",
        "_type" : "_doc",
        "_id" : "b",
        "_score" : 1.0,
        "_source" : {
          "data" : "B"
        }
      }
```

**结论：**

自定义routing后会导致的一个问题：**doc_id不再全局唯一**。

**分析：**

ES shard的实质是Lucene的索引，所以其实每个shard都是一个功能完善的倒排索引。ES能保证doc_id全局唯一是采用doc_id作为了路由，所以同样的doc_id肯定会路由到同一个shard上面，如果出现doc_id重复，就会update或者抛异常，从而保证了集群内doc_id唯一标识一个doc。但如果我们换用其它值做routing，那这个就保证不了了，如果用户还需要doc_id的全局唯一性，那只能自己保证了。

因此，因为doc_id不唯一，即便我们指明doc_id查询文档，在指明和不指明路由的情况下，查询结果极可能不一样。

所以，**如果自定义了routing字段的话，一般doc的增删改查接口都要加上routing参数以保证一致性。**

为此，ES在mapping中提供了一个选项，可以强制检查doc的增删改查接口是否加了routing参数，如果没有加，就会报错。设置方式如下：

```json
PUT <索引名>/
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 0
  },
  "mappings": {
    "_routing": {
      "required": true        // 设置为true，则强制检查；false则不检查，默认为false
    }
  }
}
```



**自定义路由的作用：**

很多时候自定义路由是为了减少查询时扫描shard的个数，从而提高查询效率。默认查询接口会搜索所有的shard，但也可以指定routing字段，这样就只会查询routing计算出来的shard，提高查询速度。使用方式也非常简单，只需在查询语句上面指定routing即可，允许指定多个：

```json
GET route_test/_search?routing=key1,key2 
{
  "query": {
    "match": {
      "data": "b"
    }
  }
}
```

另外，指定routing还有个弊端就是容易造成负载不均衡。所以ES提供了一种机制可以将数据路由到一组shard上面，而不是某一个。只需在创建索引时（也只能在创建时）设置`index.routing_partition_size`，默认值是1，即只路由到1个shard，可以将其设置为大于1且小于索引shard总数的某个值，就可以路由到一组shard了。值越大，数据越均匀。当然，从设置就能看出来，这个设置是针对单个索引的，可以加入到动态模板中，以对多个索引生效。指定后，shard的计算方式变为：

```shell
shard_num = (hash(_routing) + hash(_id) % routing_partition_size) % num_primary_shards
```

对于同一个routing值，`hash(_routing)`的结果固定的，`hash(_id) % routing_partition_size`的结果有 *routing_partition_size* 个可能的值，两个组合在一起，对于同一个routing值的不同doc，也就能计算出 *routing_partition_size* 可能的shard num了，即一个shard集合。但要注意这样做以后有两个限制：

1. 索引的mapping中不能再定义join关系的字段，原因是join强制要求关联的doc必须路由到同一个shard，如果采用shard集合，这个是保证不了的。
2. 索引mapping中`_routing`的`required`必须设置为true。





## 别名机制

索引别名就像一个快捷方式或软连接，可以指向一个或多个索引，也可以给任何一个需要索引名的API来使用。别名 带给我们极大的灵活性，我们可以使用索引别名实现以下功能：

- 可以帮助运维实现零停机情况下重建索引
- 可以过滤一些索引的数据
- 可以指向多个索引（只能查，不能修改新增等操作）



**创建别名：**

```json
put s10 // 创建索引

POST s10/_alias/a_s10  // 为单个索引创建别名

POST /_aliases  // 批量管理别名
{
  "actions": [
    {
      "remove": {
        "index": "s10",
        "alias": "a_s10"
      }
    },
    {
      "add": {
        "index": "s10",
        "alias": "new_alias_s10"
      }
    }
  ]
}

POST /_aliases  // 多个索引公用一个别名
{
  "actions": [
    {
      "add": {
        "indices": ["s11", "s12"],
        "alias": "coommon_alias"
      }
    }
  ]
}
```



**使用别名**

别名可以完全取代索引名，来完成增删改查的操作。但更主要的作用是同一多个索引，对外提供一致的别名接口。

- **指向单索引**

  当别名只指向单个索引时，别名可以完全取代索引名，来完成增删改查的操作。

  ```json
  POST s10/_create/1  // 通过索引名创建文档
  {
    "data": "test1111"
  }
  
  POST new_alias_s10/_create/2  // 通过别名创建文档
  {
    "data": "test222222"
  }
  
  
  GET new_alias_s10/_search  // 通过别名查询
  ---------------------------
  "hits" : [
        {
          "_index" : "s10",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 1.0,
          "_source" : {
            "data" : "test1111"
          }
        },
        {
          "_index" : "s10",
          "_type" : "_doc",
          "_id" : "2",
          "_score" : 1.0,
          "_source" : {
            "data" : "test222222"
          }
        }
      ]
  ```

  

- **Filtered alias**

  带有过滤器的别名提供了一种创建同一索引的不同“视图”的简便方法。 可以使用Query DSL定义过滤器，并使用此别名将其应用于所有“搜索”，“计数”，“按查询删除”和“更多此类操作”。

  要创建过滤后的别名，首先我们需要确保映射中已存在这些字段：

  ```json
  PUT /test1
  {
    "mappings": {
      "properties": {
        "user" : {
          "type": "keyword"
        }
      }
    }
  }
  ```

  现在我们可以利用filter来创建一个alias，是基于user字段

  ```json
  POST /_aliases  // 创建带过滤器的别名
  {
    "actions" : [
      {
        "add" : {
          "index" : "test1",
          "alias" : "alias2",
          "filter" : { "term" : { "user" : "xiaozhang" } }
        }
      }
    ]
  }
  
  POST alias1/_bulk  // 通过别名批量插入数据
  {"create": {"_id": 1}}
  {"user": "xiaozhang"}
  {"create": {"_id": 2}}
  {"user": "xiaoli"}
  
  GET test1/_search  // 通过索引名查询，有没有别名都一样
  -------------------
  "hits" : [
        {
          "_index" : "test1",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 1.0,
          "_source" : {
            "user" : "xiaozhang"
          }
        },
        {
          "_index" : "test1",
          "_type" : "_doc",
          "_id" : "2",
          "_score" : 1.0,
          "_source" : {
            "user" : "xiaoli"
          }
        }
      ]
  
  GET alias1/_search  // 通过别名查询，别名中的过滤器会自动对查询结果过滤
  ----------------------
      "hits" : [
        {
          "_index" : "test1",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 1.0,
          "_source" : {
            "user" : "xiaozhang"
          }
        }
      ]
  ```

  

- **Write index**

  当别名指向多个索引时，默认情况下只允许通过别名进行查询操作，如果想要修改数据，可以将别名指向的索引关联为write索引。 指定后，针对指向多个索引的别名的所有索引和更新请求将尝试解析为write索引的一个索引。 每个别名只能将一个索引分配为一次write索引。 如果未指定write索引且别名引用了多个索引，则不允许写入。

  可以使用别名API和索引创建API将与别名关联的索引指定为write索引。

  ```
      POST /_aliases
      {
          "actions" : [
              {
                  "add" : {
                       "index" : "test",
                       "alias" : "alias1",
                       "is_write_index" : true
                  }
              },
              {
                  "add" : {
                       "index" : "test2",
                       "alias" : "alias1"
                  }
              }
          ]
      }
  ```

  在这里，我们定义了alias1同时指向test及test2两个索引。其中test中，注明了is_write_index，那么，如下的操作：

  ```
      PUT /alias1/_doc/1
      {
          "foo": "bar"
      }
  ```

  相当于如下的操作：

  ```
  PUT /test/_doc/1
  ```

  也就是写入到test索引中，而不会写入到test2中。

  要交换哪个索引是别名的写入索引，可以利用别名API进行原子交换。 交换不依赖于操作的顺序。

  ```
      POST /_aliases
      {
          "actions" : [
              {
                  "add" : {
                       "index" : "test",
                       "alias" : "alias1",
                       "is_write_index" : false
                  }
              }, {
                  "add" : {
                       "index" : "test2",
                       "alias" : "alias1",
                       "is_write_index" : true
                  }
              }
          ]
      }
  ```



## 模板机制

### 索引模板

Index Templates 帮助我们设定Mappings和Settings，并按照一定规则，自动匹配到新创建的索引之上。

- 模版仅在一个索引被新创建时，才会产生作用。修改模板对已经创建的索引不产生影响；
- 可以同时设定多个模板，这些模板会被"merge"到一起
- 创建模板时，可以指定`order`的值，来控制"merge"的过程

**示例：**

```json
POST _template/base  // 创建一个任何索引都能匹配的模板
{
  "index_patterns": ["*"],
  "order": 0,
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  }
}

POST _template/test_base  // 创建一个索引名以 test_ 开头的模板
{
  "index_patterns": ["test_*"],
  "order": 1,
  "mappings": {
    "properties": {
      "test_no": {
        "type": "long"
      },
      "test_group": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      }
    }
  }
}

PUT base_demo  // 创建索引

GET base_demo
------------------------
{
  "base_demo" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "creation_date" : "1636898679902",
        "number_of_shards" : "2",   // 从分片可以看出，当前索引使用了 base 模板
        "number_of_replicas" : "1",
        "uuid" : "mra9I7dhTkWC_kfHcMikcQ",
        "version" : {
          "created" : "7060299"
        },
        "provided_name" : "base_demo"
      }
    }
  }
}


PUT test_base_demo  // 创建test_*索引

GET test_base_demo
-----------------------
{
  "test_base_demo" : {
    "aliases" : { },
    "mappings" : {  // 从mapping可看出，使用了 test_base 模板
      "properties" : {
        "test_group" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword"
            }
          }
        },
        "test_no" : {
          "type" : "long"
        }
      }
    },
    "settings" : {
      "index" : {
        "creation_date" : "1636898690691",
        "number_of_shards" : "2",  // 从分片可看出，还同时使用了 base 模板，这就是 merge 模板。如果test_base中定义了相同的配置，那么就会根据 order 来选择，值大的优先。
        "number_of_replicas" : "1",
        "uuid" : "kCTDXkfSRVuOQv88b1mczQ",
        "version" : {
          "created" : "7060299"
        },
        "provided_name" : "test_base_demo"
      }
    }
  }
}
```



### 映射模板

在第一章节中，已经知道了动态映射，即在创建文档时，文档中包含了创建索引时没有创建映射的字段时，es采取哪一种处理方式。当设置 `dynamic=true`时，es会自动更新索引的mapping，但此时更新mapping的依据是系统默认的一些映射规则。那如果这种情况下，我们想自定义一个映射规则，来处理新出现的字段的mapping，那么 映射模板 就派上用场了。

映射模板 也称为 动态模板，有以下几个规则：

1. Dynamic Template 时定义在某个索引的mapping中的；
2. 模板是需要自定义一个名称；
3. 匹配规则是一个数组；
4. 为匹配到的字段设置mapping



#### 根据字段类型mapping

根据字段类型匹配通过 match_mapping_type 属性来控制，当添加文档的时候，根据ES的JsonParser解析出来字段的类型来匹配 match_mapping_type 指定的类型，如果匹配就会使用对应的mapping。

```json
{
  "mappings": {
    "dynamic_templates": [
      {
        "dt_name_one": {
          "match_mapping_type": "long",
          "mapping": {
            "type": "integer"
          }
        }
      },
      {
        "dt_name_two": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text",
            "fields": {
              "raw": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    ]
  }
}
```



#### 根据字段名称mapping

根据字段名称映射使用的是 match、unmatch、match_pattern 属性来控制。

```json
{
  "mappings": {
    "dynamic_templates": [
      {
        "longs_as_strings": {
          "match_mapping_type": "string",
          "match": "long_*",
          "unmatch": "*_text",
          "mapping": {
            "type": "long",
            "enable": false
          }
        }
      },
      {
        "longs_as_strings": {
          "match_pattern": "regex",
          "match": "^profit_\\d+$",
          "mapping": {
            "type": "long",
            "index": false,
            "norms": false,
            "doc_values": false
          }
        }
      }
    ]
  }
}
```



#### 根据字段路径mapping

按路径匹配使用的是 path_match、path_unmatch 属性来指定。

```json
{
  "mappings": {
    "dynamic_templates": [
      {
        "dt_path_name": {
          "path_unmatch": "user.*",
          "path_match": "*.conceal",
          "mapping": {
            "type": "text",
            "enable": false
          }
        }
      }
    ]
  }
}
```





# Python 操作ES

## 安装API

```python
pip3 install elasticsearch
```



## 基础操作

### 创建连接

```python
# 创建 es 连接客户端
# 单结点
es = Elasticsearch(hosts=["121.4.47.229:9200"], 
                   http_auth=("elastic", "Zj1340026934") # 认证信息
                  )

# 动态连接
es = Elasticsearch(
    ['esnode1:port', 'esnode2:port'],
    # 在做任何操作之前，先进行嗅探
    sniff_on_start=True,
    # 节点没有响应时，进行刷新，重新连接
    sniff_on_connection_fail=True,
    # 每 60 秒刷新一次
    sniffer_timeout=60
)

# 对不同的节点，赋予不同的参数
es = Elasticsearch([
    {'host': 'localhost'},
    {'host': 'othernode', 'port': 443, 'url_prefix': 'es', 'use_ssl': True},
])

# SSL开启时创建连接
es = Elasticsearch(
    ['localhost:443', 'other_host:443'],
    ＃打开SSL 
    use_ssl=True,
    ＃确保我们验证了SSL证书（默认关闭）
    verify_certs=True,
    ＃提供CA证书的路径
    ca_certs='/path/to/CA_certs',
    ＃PEM格式的SSL客户端证书
    client_cert='/path/to/clientcert.pem',
    ＃PEM格式的SSL客户端密钥
    client_key='/path/to/clientkey.pem'
)
```



### 文档操作

```python
# ---------创建文档-----------
	# index创建
	result_1 = es.index(index="py_demo1", id="2", document={"name": "李寻欢", "age": 26})
  
  # op_type: index or create. 显示指定为创建类型时，如果文档已存在将报错
 	result_1 = es.index(index="py_demo1", id="5", op_type="create", document={"name": "博强", "age": 18})
  
  # create方法创建，其内部调用的就是index，因此也不能重复创建文档
	result_1 = es.create(index="py_demo1", id="4", document={"name": "阿强", "age": 18})
  

# ---------查询文档-----------
	# 查询指定ID的文档
  result_1 = es.get(index="py_demo1", id="1")
  
  # 条件查询。同原生的DSL查询，参数直接从 query 后面开始写，不需要再写 query 这一层
  result_1 = es.search(index="py_demo1", query={"match": {"name": "强"}})
  result_1 = es.search(index="py_demo1", query={"bool": {"must": [{"match_phrase": {"name": "阿强"}},]}})

  # 过滤字典。只返回我们需要的字段信息，通过 filter_path 字段实现。通常 _source 中的字段才是我们需要的
	result_1 = es.search(index="py_demo1", query={"range": {"age": {"gt": 18}}}, filter_path="hits.hits._source")
	----
  {'hits': {'hits': [{'_source': {'name': '李寻欢', 'age': 26}}]}}
  
  # 返回指定字段。分别由三个字段可以控制。_source、_source_includes、_source_excludes
  result_1 = es.search(index="py_demo1", query={"match": {"name": "李寻欢"}}, filter_path="hits.hits._source",
                     _source_includes=["name"])
  ----
  {'hits': {'hits': [{'_source': {'name': '李寻欢'}}]}}

	# 分页、排序等都有与原生对应的入参

# ----------删除文档----------
	# 根据id删除
	result_1 = es.delete(index="py_demo1", id="1")
  
  # 根据查询结果删除文档
  result_1 = es.delete_by_query(index="py_demo1", body={"query": {"ids": {"values": ["2", "3"]}}})


# ----------更新文档----------
   # 删除原数据后，重新创建。同原生的 PUT
   result_1 = es.index(index="py_demo1", id="2", body={"name": "小强", "age": 20})  
  
   # 真正的修改数据，同原生的 POST
   result_1 = es.update(index="py_demo1", id="2", body={"doc": {"name": "张小强"}})
  

# ----------批量操作----------
  # 批量创建
  body = [
    {"create": {"_id": 8}},
    {"name": "西门吹雪", "age": 22},
    {"update": {"_id": 5}},
    {"doc": {"name": "伯强"}}
	]
	result_1 = es.bulk(index="py_demo1", body=body)  # 使用方法同原生批量操作
  
  # python提供的更优批量导入方案 helpers 模块
  actions = [
    {
        "_index": "py_demo1",
        "_op_type": "create",
        "_id": "9",
        "_source": {
            "name": "花满楼",
            "age": 20
        }
    },
    {
        "_index": "py_demo1",
        "_op_type": "create",
        "_id": "10",
        "_source": {
            "name": "陆小凤",
            "age": 22
        }
    },
    {
        "_index": "py_demo1",
        "_op_type": "update",
        "_id": "5",
        "_source": {
            "doc": {           # 更新文档时，要在修改数据前包一层 "doc"，和原生保持一致
                "name": "江流儿",
                "age": 14
            }
        }
    },
    {
        "_index": "py_demo1",
        "_op_type": "delete",
        "_id": "4"
    }
]

s = helpers.bulk(es, actions=actions)

print(s)  # 返回值 (成功条数, 错误items) 或 (成功条数, 失败条数)
(4, [])
```



### 索引操作

```python
# -----------创建索引-----------
	# 创建索引
	response = es.indices.create(index="py_demo2")
  
  # 创建索引及映射、分片设置
  response = es.indices.create(index="py_demo3",
                             mappings={"properties": {"name": {"type": "text"}, "age": {"type": "short"}}},
                             settings={"number_of_shards": 1, "number_of_replicas": 2})
  
# -----------查询索引------------
	# 查询索引
  es.indices.get(index="py_demo3")
  
  # 分别查询索引相关信息
  es.indices.get_mapping(index="py_demo3")
  es.indices.get_alias(index="py_demo3")
  es.indices.get_settings(index="py_demo3")
  
# -----------修改索引-----------
  es.indices.put_alias(index="py_demo3", name="py3")
  
# -----------删除索引-----------
	es.indices.delete(index="py_demo3")
  
# -----------检查索引是否存在----------
	es.indices.exists(index="py_demo1")
```



### 其他信息

```python
# 服务器是否启动
es.ping()

# 服务器信息
es.info()

# 插件信息
es.cat.plugins()

# 索引信息
es.cat.indices()

# 健康状态
es.cat.health()

# 查看文档总数. format 可以修改返回数据的格式
es.cat.count(format='json')

# 查看结点信息
es.cat.master()
es.cat.nodes()

# 集群相关
es.cluster.health()
es.cluster.state()
es.cluster.stats()
```



## 项目实战

项目实战代码：https://github.com/zhangjian-ai/chatroom/tree/master/backend/apps/es

这里贴出mysql同步es的脚本：

```python
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.helpers.errors import BulkIndexError

from db import DBPool


def news_to_es():
    pool = DBPool(
        host="121.4.47.229",
        port=3300,
        user="root",
        password="zm_123456",
        db="chatroom",
        mincached=10
    )
    es = Elasticsearch(hosts=["121.4.47.229:9200"], http_auth=("elastic", "Zj1340026934"))

    # 判断es索引是否存在，不存在就创建
    if not es.indices.exists(index="cars_news"):
        es.indices.create(index="cars_news",
                          mappings={
                              "properties": {
                                  "title": {
                                      "type": "text",
                                      "analyzer": "ik_max_word",
                                      "search_analyzer": "ik_max_word",
                                      "fields": {
                                          "suggest": {
                                              "type": "completion",
                                              "analyzer": "ik_max_word",
                                              "search_analyzer": "ik_max_word"
                                          }
                                      }
                                  },
                                  "summary": {
                                      "type": "text",
                                  },
                                  "detail_url": {
                                      "type": "text"
                                  },
                                  "img_url": {
                                      "type": "text"
                                  },
                                  "tag": {
                                      "type": "keyword"
                                  }
                              }
                          },
                          settings={
                              "max_result_window": 99999999
                          })

    # 查询临时表，如果有数据就开始同步
    res = pool.query_one(sql="select count(*) count from chatroom.news_temp;")
    if res.get("count"):
        offset = 0
        num = 20

        # 按照每一百条一次来同步
        print("开始同步")
        while offset < res.get("count"):
            sets = pool.query_many(
                sql=f"select id, title, summary, detail_url, img_url, tag from chatroom.news_temp limit {offset}, {num};")

            # 创建actions迭代器
            actions = (
                {
                    "_index": "cars_news",
                    "_op_type": "create",
                    "_id": item.get("id"),
                    "_source": {
                        "title": item.get("title"),
                        "summary": item.get("summary"),
                        "detail_url": item.get("detail_url"),
                        "img_url": item.get("img_url"),
                        "tag": item.get("tag")
                    }
                }
                for item in sets
            )
            try:
                helpers.bulk(es, actions=actions)
            except BulkIndexError:
                pass

            # 增加偏移量
            offset += len(sets)

            print(f"同步进度：{offset} 条！")

        # 删除已同步数据
        pool.execute_one(sql="truncate chatroom.news_temp;")

        print("同步完成")
    else:
        print("暂无同步数据")


if __name__ == '__main__':
    news_to_es()

```



 



