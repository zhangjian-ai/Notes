# 实现原理

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

  - **动态映射**

    如果ES所有的mapping没有提前指定的话，当写入第一条数据的时候，就会自动创建索引，并且生成对应的映射。
     不同的数值类型有默认对应不同的es的数据结构，如下所示：

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

- 域Field：类似于关系型数据库中的字段。
- elasticsearch是面向restful的，下面是restful请求与elasticsearch操作的对应：

| 请求方法 | 对应操作 |        说明        |
| :------: | :------: | :----------------: |
|   GET    |   读取   |      获取数据      |
|   POST   |   新增   |      新增数据      |
|   PUT    |   修改   | 修改数据或增加数据 |
|  DELETE  |   删除   |      删除数据      |

- 索引用来存储数据，分片也是用来存储数据，它们是怎么对应的？一个索引存储在多个分片上，默认情况下，一个索引有五个主分片，五个副本分片。主分片的数量一旦定下来就不能再修改，但副本分片的数量还可以修改。



## 索引

Elasticsearch最关键的就是提供强大的索引能力了，其实InfoQ的这篇[时间序列数据库的秘密(2)——索引](http://www.infoq.com/cn/articles/database-timestamp-02?utm_source=infoq&utm_medium=related_content_link&utm_campaign=relatedContent_articles_clk)写的非常好，我这里也是围绕这篇结合自己的理解进一步梳理下，也希望可以帮助大家更好的理解这篇文章。

Elasticsearch索引的精髓：

> 一切设计都是为了提高搜索的性能

另一层意思：为了提高搜索的性能，难免会牺牲某些其他方面，比如插入/更新，否则其他数据库不用混了。前面看到往Elasticsearch里插入一条记录，其实就是直接PUT一个json的对象，这个对象有多个fields，比如上面例子中的*name, sex, age, about, interests*，那么在插入这些数据到Elasticsearch的同时，Elasticsearch还默默[1](http://blog.pengqiuyuan.com/ji-chu-jie-shao-ji-suo-yin-yuan-li-fen-xi/#fn:1)的为这些字段建立索引--倒排索引，因为Elasticsearch最核心功能是搜索。

InfoQ那篇文章里说Elasticsearch使用的倒排索引比关系型数据库的B-Tree索引快，为什么呢？



### 什么是B-Tree索引?

上大学读书时老师教过我们，二叉树查找效率是logN，同时插入新的节点不必移动全部节点，所以用树型结构存储索引，能同时兼顾插入和查询的性能。因此在这个基础上，再结合磁盘的读取特性(顺序读/随机读)，传统关系型数据库采用了B-Tree/B+Tree这样的数据结构：

<img src="./image-20211101155227593.png" alt="image-20211101155227593" style="zoom:67%;" />

为了提高查询的效率，减少磁盘寻道次数，将多个值作为一个数组通过连续区间存放，一次寻道读取多个数据，同时也降低树的高度。

### 什么是倒排索引?

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

这时候爱提问的小明又举手了:"那个FST是神马东东啊?"

一看就知道小明是一个上大学读书的时候跟我一样不认真听课的孩子，数据结构老师一定讲过什么是FST。但没办法，我也忘了，这里再补下课：

> FSTs are finite-state machines that **map** a **term (byte sequence)** to an arbitrary **output**.
>
> FST是将一个 词语（字节序列）映射到任意输出的有限状态机。

假设我们现在要将mop, moth, pop, star, stop and top(term index里的term前缀)映射到序号：0，1，2，3，4，5(term dictionary的block位置)。最简单的做法就是定义个Map<string, integer="">，大家找到自己的位置对应入座就好了，但从内存占用少的角度想想，有没有更优的办法呢？答案就是：**FST**([理论依据在此，但我相信99%的人不会认真看完的](http://www.cs.nyu.edu/~mohri/pub/fla.pdf))

<img src="./20211101160121.jpg" alt="Alt text" style="zoom:67%;" />

⭕️表示一种状态

-->表示状态的变化过程，上面的字母/数字表示状态变化和权重

将单词分成单个字母通过⭕️和-->表示出来，0权重不显示。如果⭕️后面出现分支，就标记权重，最后整条路径上的权重加起来就是这个单词对应的序号。

> FSTs are finite-state machines that map a term (**byte sequence**) to an arbitrary output.

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
   docker run --name elasticsearch -p 9200:9200 -p 9300:9300  -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms256m -Xmx256m" -v /var/local/myapp/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /var/local/myapp/elasticsearch/data:/usr/share/elasticsearch/data -v /var/local/myapp/elasticsearch/plugins:/usr/share/elasticsearch/plugins -d elasticsearch:7.6.2
   
   其中elasticsearch.yml是挂载的配置文件，data是挂载的数据，plugins是es的插件，如ik，而数据挂载需要权限，需要设置data文件的权限为可读可写,需要下边的指令。
   chmod -R 777 要修改的路径
   
   -e "discovery.type=single-node" 设置为单节点
   特别注意：
   -e ES_JAVA_OPTS="-Xms256m -Xmx256m" \ 测试环境下，设置ES的初始内存和最大内存，否则过大导致启动不了ES
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



## 高级CRUD

- **match匹配查询**

  > match：按条件匹配。match: { "age": 18 }
  >
  > match_all：全部匹配。match_all: {} ,全部匹配时，match_all 可省略不写
  >
  > 

  ```json
  # --------单值匹配--------
  GET users/_search
  {
    "query": {
      "match": {
        "message": "Singer"  # match中的匹配字段，匹配的值可以不完全匹配
      }
    }
  }
  
  # --------全部匹配，也就是查询ALL----------
  GET users/_search
  {
    "query": {
      "match_all": {}
    }
  }
  ```

- **bool查询**

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
  >   filter也常和range范围查询一起结合使用
  >
  >   range范围可供组合的选项：
  >
  >   - gt : 大于
  >
  >   - lt : 小于
  >
  >   - gte : 大于等于
  >
  >   - lte :小于等于

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

- **_source 文档字段过滤**

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

- **排序**

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

- **控制返回条数**

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

- **分页**

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

- **范围查询**

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

- **聚合函数**

  > *官方对聚合有四个关键字：`Metric(指标)、Bucket(桶)、Matrix(矩阵)、Pipeline(管道)`，在查询请求体中以aggregations语法来定义聚合分析，也可简写成aggs*
  >
  > ```text
  > Metric(指标)：指标分析类型，如计算最大值、最小值、平均值等（对桶内的文档进行聚合分析的操作）
  > Bucket(桶)：分桶类型，类似sql中的group by语法（满足特定条件的文档的集合）
  > Pipeline(管道)：管道分析类型，基于上一级的聚合分析结果进行再分析
  > Matrix(矩阵)：矩阵分析类型（聚合是一种面向数值型的聚合，用于计算一组文档字段中的统计信息）
  > ```

  - **指标（Mertric）聚合**

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

      

  - **分桶（Bucket）聚合**

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

      

  - **聚合嵌套：**适用于所有的聚合

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

    