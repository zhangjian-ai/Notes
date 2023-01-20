# Django





## ORM

### ORM

- ORM : 全称 object relational mapping，对象关系映射
- 功能 : 通过orm实现使用操作对象的方式来操作数据库中的数据
- 目的 : 就是为了能够让不懂SQL语句的人通过python面向对象的知识点也能够轻松自如的操作数据库，ORM其实就是将类对象的语法翻译成SQL语句的一个引擎



### ORM与数据库的映射关系

<table border=1>
<tr><td>ORM</td><td>DB</td></tr>
<tr><td>模型类</td><td>表</td></tr>
<tr><td>类属性</td><td>表字段</td></tr>
<tr><td>模型类实例</td><td>一行表数据</td></tr>
</table>


查询操作得到query对象，每一个对象对应一行表数据，通过反序列化即可获得表数据。



### 模型字段类型

在ORM中，类属性名直接对应表的字段，属性的值应该是一个指定字段类型的实例，用来表达我们对该字段的规定和约束。比如，字段的类型、是否为索引列、默认值、comment 信息 等。

- **AutoField**

  自增的整数类型，必填参数 primary_key=True，则成为数据库的主键。无该字段时，Django在创建表时会自动添加一个id属性，字段类型就是AutoField。 一个model不能有两个AutoField字段。

- **IntegerField**

  一个整数类型。数值的范围是 -2147483648 ~ 2147483647。 

- **CharField**

  字符类型，必须提供max_length参数。max_length表示字符的长度。 

- **DateField**

  日期类型，日期格式为YYYY-MM-DD，相当于Python中的datetime.date的实例。 

  > 参数：
  > auto_now：每次修改时修改为当前日期时间。
  > auto_now_add：新创建对象时自动添加当前日期时间。
  >
  > 注意：auto_now 和 auto_now_add 和 default 参数是互斥的，不能同时设置。

- **DatetimeField**

  日期时间类型，格式为YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]，相当于Python中的datetime.datetime的实例

  > 参数：同 DateField

- **DecimalField**

  浮点类型。

  > 参数：
  >
  > max_digits：总位数(不包括小数点和符号)
  >
  > decimal_places：小数位数

- **BooleanField**

  布尔类型。

- **TextField**

  文本类型，用于保存大文本的字段。

- **ForeignKey**

  外键类型。在子表中创建字段，指向主表。

  > 参数：
  >
  > to：要关联的主表。如果是自关联，则赋值该字段为 'self'
  >
  > on_delete/on_update：当主表中被关联数据被删除或更新时，子表该字段的处理方式
  >
  > ​		CASCADE：同步操作。即主表数据删除，子表关联的数据也同步删除；
  >
  > ​		PROTECT：阻止主表的删除操作，但是弹出ProtectedError异常；
  >
  > ​		SET_NULL：将外键字段设为null，只有当字段设置了null=True时，才可以使用该参数
  >
  > ​		SET_DEFAULT：将外键字段设为默认值，只有当字段设置了default参数时，才可以使用该参数
  >
  > ​		DO_NOTHING：什么都不做，子表保持现状
  >
  > ​		SET()：设置为一个传递给SET()的 值和一个回调函数 的返回值
  >
  > to_field：要关联的主表字段。该参数不填时，外键默认存储的是主表的主键；指定该参数时，要求主表的该字段 unique=True；
  >
  > related_name：关联别名。用于主表对象获取子表的对象，当子表中多个字段都为外键时，该字段必须指定；

- **FileField**

  文件类型。Django 默认情况是直接将文件保存到服务器本地，但这通常是不满足环境部署规范的，我们通常需要实现自己的文件存储类（继承 django.core.files.storage.Storage 类），将文件保存到专门的文件服务器中，而该字段也通常保存的是文件在文件服务器中的地址。

- **ImageField**

  图片类型。与FileField类型相似。



这里仅介绍常用的字段类型，更多字段可见官网：https://docs.djangoproject.com/en/1.11/ref/models/fields

在上面介绍字段类型时，也介绍了类型的部分参数，但都是该类型特有的，下面介绍一些通用的字段类型参数。

1. null

   是否允许字段为空，默认 False

2. blank

   是否允许字段不填，默认 False

   区别于 null，null纯粹是数据库范畴的，而 blank 是数据验证范畴的，如果一个字段的blank=True，表单的验证将允许该字段是空值。如果字段的blank=False，该字段就是必填的

3. default

   字段的默认值。可以是一个值或者可调用对象

4. primary_key

   设置字段为主键，默认 False，用来覆盖Django默认的主键字段

5. unique

   设置字段为唯一键，添加唯一约束，默认 False

6. choices

   类似枚举。其值应该是一个二元组组成的可迭代对象，用来给字段提供值的选项。例如：[(1, '高'), (2, '中'), (3, '低')]，数据表中，保存 1、2、3 就可以了，而我们通过序列化，可以返回具有明确语义的值（高、中、低）到查询结果中

7. db_index

   设置字段为索引，默认 false

8. verbose_name

   在admin管理后台，字段展示的值（列名）



### 模型Meta类

Meta类是模型类中类。可用于定义有关模型的各种内容，例如权限、数据库名称、单复数名称、抽象、排序等，是否在模型类中添加该类，是可选的。

这里介绍一些常用的Meta类属性配置：

更多属性：https://docs.djangoproject.com/en/3.0/ref/models/options/

1. abstract

   该选项用于定义模型是否抽象；它们与[抽象类](https://www.zhihu.com/search?q=抽象类&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2310626679})的工作方式相同。抽象类是不能被实例化，只能被扩展或继承的类。

   设置为抽象的模型只能被继承。如果是有多个具有共同字段的base模型，则可以使用此选项。

2. db_table

   此选项用于设置数据库内本模型对应的表的名称

3. ordering

   此选项用于指定查询结果的排序规则，其值应该是一个列表，列表的值为该表的字段名。

   例如：ordering = ["-dateTimeOfPosting"]

   在上面的示例中，检索到的对象将根据 dateTimeOfPosting 字段按降序排列。 （- 前缀用于定义降序。）

4. verbose_name

   此选项用于为模型定义一个类可读的单数名称，并将覆盖 Django 的默认命名约定。此名称也将反映在[管理面板 (admin) 中。

5. verbose_name_plural

   此选项用于为模型定义一个人类可读的复数名称，这将再次覆盖 Django 的默认命名约定。此名称也将反映在管理面板 (admin) 中。



### 创建表

1. 配置settings.py文件

   ```python
   # 添加默认数据库配置
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'orm01',
           'USER':'root',
           'PASSWORD':'zxy521',
           'HOST':'1,2,3,4',
           'PORT':3306,
       }
   }
   
   # 如果涉及到多个数据库，则还需要在当前配置数据库路由，以告诉Django在不同时候请求不同的数据库
   # 配置读写分离
   DATABASE_ROUTERS = ['meiduo_mall.utils.db_router.MasterSlaveDBRouter']
   
   # MasterSlaveDBRouter
   class MasterSlaveDBRouter(object):
       """数据库主从分离路由"""
   
       def db_for_read(self, model, **hints):
           """读数据库"""
           return "slave_01"
   
       def db_for_write(self, model, **hints):
           """写数据库"""
           return "default"
   
       def allow_relation(self, obj1, obj2, **hints):
           """是否运行关联操作"""
           return True
   ```

2. 在项目根目录的`__init__.py`文件中，配置mysql

   ```python
   import pymysql
   
   pymysql.install_as_MySQLdb()
   ```

3. 相关命令

   ```shell
   # 创建Django项目
   django-admin startproject  项目名称
   
   # 创建app
   python3 manage.py startapp 应用名称
   
   # 迁移数据库。迁移之前，需要现在数据创建好对应数据库
   python manage.py makemigrations  # 编译迁移文件
   python manage.py migrate  # 执行迁移
   ```

4. 编写模型类

   ```python
   class UserInfo(models.Model):
       id = models.AutoField(primary_key=True)
       name = models.CharField(max_length=10)
       bday = models.DateField()
       checked = models.BooleanField()
   
   # 编写好模型类，便可在命令行执行迁移操作，将我们的模型类，转换成数据库表
   ```

   

### 增加数据

操作表数据前提是，在models.py文件中创建了模型类，ORM的所有操作，都要基于模型类。

- 直接实例化模型类

  ```python
  # views.py
  from django.shortcuts import render,HttpResponse
  from   app01 import  models
  import datetime
  
  def home(request):
      now_date = datetime.datetime.now()
      # 实例化模型类型，实例化仅在视图层生效，此时并未将数据写入数据库
      new_sql = models.UserInfo(
          id =1,
          name='zbb',
          bday=now_date,
          checked=1,
      )
      # 实例对象调用 save 方法，将实例翻译成SQL语句，并在数据执行。此时才真正的将数据入库
      new_sql.save()
  
      return HttpResponse("执行sql操作完成!")
  ```

- 使用objects中的create方法

  创建模型时，都是需要继承 models.Model 基类，在基类中提供了 objects 对象，该对象中 封装了很多我们能直接使用的操作方法。

  ```python
  def home(request):
    # 通过模型类调用objects，在调用create方法，此时就不需要再手动调用 save 保存了
    ret = models.UserInfo.objects.create(
      # 这里 id 字段没有写也是可以的，因为 id 是AutoField类型，具有自增属性
      name='zxy',
      bday='2020-8-8',
      checked=0
    )
  
    return HttpResponse("执行sql操作完成!")
  ```

- 批量创建

  实例化多条表数据，一次性创建

  ```python
  obj_list = []
  for i in range(20):
      obj = models.UserInfo(
        name=f'zxy{i}',
        bday='2020-8-8',
        checked=0
      )
      obj_list.append(obj)
  
  # bulk_create 批量创建
  models.UserInfo.objects.bulk_create(obj_list) 
  ```

  

### 查询数据

查询操作是业务当中用得最多的，而 **filter** 是用得最多也推荐使用的查询方式。这里用到查询方法，也都是objects对象中封装好的。

> - 两个对象
>   1. Model 对象，表示一行表数据，也就是模型类的一个实例；
>   2. QuerySet 对象，由多个 Model 对象组成。QuerySet 对象可以继续调用所有查询方法
> - 两个方法，在具体示例中举例介绍，这里仅有一个概念即可
>   1. F方法：针对某一列的值进行操作，获得指定列的值，在更新时也可以用得到；
>   2. Q方法：针对复杂的查询场景。配合 &、|、~ 实现 与、或、非 的查询

1. all 查询

   all 查询数据表中的所有数据行，结果是一个 QuerySet 对象

   ```python
   # 查询所有数据
   qs = models.UserInfo.objects.all()
   ```

2. get 查询

   get 查询要求比较严格，查询结果必须有且只有一条数据，没有数据或者多条数据时，都会引发异常

   get 查询结果是一个 Model 对象

   ```python
   # 查询一条唯一数据
   q = models.UserInfo.objects.get(id=1)
   ```

3. exclude 查询

   排除查询，把满足条件的排除掉，获取不满足条件的数据

   ```python
   qs = models.UserInfo.exclude(name='zxy')
   ```

4. **filter 查询**

   filter 查询结果也是一个 QuerySet 对象，其中可以有0条或多条数据，不会引发异常。

   提示：QuerySet 对象是可以继续调用filter方法完成进一步筛选的。

   ```python
   # 单条件查询
   qs = models.UserInfo.filter(name='zxy')
   
   # and 查询
   qs = models.UserInfo.filter(name='zxy', checked=0)
   
   # or 查询，借助Q方法
   qs = models.UserInfo.filter(Q(name='zxy') | Q(checked=0))
   
   # not 查询，借助Q方法
   qs = models.UserInfo.filter(～ Q(name='zxy'))
   
   # 列与列之间的值做比较，借助F方法
   # 查询评论数大于价格的书籍信息
   ret = models.Book.objects.filter(comment__gt=F('good'))
   
   # 大于
   ret = models.Book.objects.filter(price__gt=35)
   
   # 大于等于
   ret = models.Book.objects.filter(price__gte=35)
   
   # 小于
   ret = models.Book.objects.filter(price__lt=35)
   
   # 小于等于
   ret = models.Book.objects.filter(price__lte=35)
   
   # 大于等于35,小于等于38
   ret = models.Book.objects.filter(price__range=[35,38])
   
   # 包含字符串
   ret = models.Book.objects.filter(title__contains='金瓶') 
   
   # 包含字符串，不区分大小写
   ret = models.Book.objects.filter(title__icontains="python")
   
   # 以什么开头，istartswith  不区分大小写；endswith/iendswith 以什么结尾
   ret = models.Book.objects.filter(title__startswith="py")
   
   # 日期类查询操作
   ret = models.Book.objects.filter(publish_date='2019-09-15')
   ret = models.Book.objects.filter(publish_date__year='2018') 
   ret = models.Book.objects.filter(publish_date__year__gt='2018')
   ret = models.Book.objects.filter(publish_date__year='2019',publish_date__month='8',publish_date__day='1')
   
   # 字段是否为空
   ret = models.Book.objects.filter(publish_date__isnull=True)
   ```

5. QuerySet 常用方法

   1. order_by 排序

      ```python
      # id相同的  价格降序（在字段前加 - 号）
      models.Book.objects.all().order_by('id','-price')
      
      # reverse 反转排序后的数据
      models.Book.objects.all().order_by('id','-price').reverse()
      ```

   2. values

      QuerySet 对象的行数据，都包含了行的所有字段，使用values则可仅获取需要的字段。

      ```python
      # values 返回的仍然是一个queryset对象
      ret = models.Book.objects.filter(id=9).values('title','price')
      
      # values 可以直接作用在objects对象上，此时返回所有行。下面两条等价
      ret = models.Book.objects.all().values()
      ret = models.Book.objects.values()
      
      # values_list 方法，与 values 方法相似。只是 values_list 返回的queryset内部是列表对象，values 返回的queryset对象内部是字典对象
      ret = models.Book.objects.all().values_list('title','price')
      ```

   3. count

      返回int型的数据条数

      ```python
      # 统计查询对象中一共有多少条数据
      models.Book.objects.all().count() 
      ```

   4. first/last

      返回Model对象

      ```python
      # 获取查询集中第一条或最后一条数据
      ret = models.Book.objects.all().first()
      ret = models.Book.objects.all().last()
      
      # QuerySet 对象也支持直接使用下表获取指定索引的Model对象
      ret = models.Book.objects.filter()[0]
      ```

   5. distinct

      去重，返回值仍是QuerySet对象

      ```python
      models.Book.objects.all().values('name').distinct()
      ```

   6. aggregate

      聚合查询，返回值是字典类型，使用聚合查询后，那么也就意味着本条查询结束

      ```python
      # 聚合查询要配合 Avg\Max\Min\Count 等方法一起使用
      ret =models.Book.objects.all().aggregate(a=Avg('price'),m=Max('price'))
      ```

   7. 分组查询

      annotate 方法，用于分组时聚合，返回值仍是 QuerySet 类型

      ```python
      # 用的book表的price字段进行分组
      ret = models.Book.objects.annotate(a=Avg('price'))
      
      # 用publish表的id进行分组，并计算分组的平均值
      ret = models.Book.objects.values('publish__id').annotate(a=Avg('price'))
      
      # 用的book表的price字段进行分组
      ret = models.Publish.objects.annotate(a=Avg('book__price')).values('a')
      ```

      

### 修改数据

1. 通过Model对象修改

   ```python
   # 跟创建数据一样Model对象的变更需要调用 save 方法
   ret = models.UserInfo.objects.filter(id=3)[0]  
   ret.name = '渣渣'
   ret.checked = 1
   ret.save()
   ```

2. 使用objects的update方法

   ```python
   # 修改后直接生效
   models.UserInfo.objects.filter(id=2).update(name='追梦NAN')
   
   # 涉及到运算的，使用F方法，批量操作
   models.Book.objects.all().update(price=F('price')+100)
   ```

   

### 删除数据

Model对象和QuerySet对象都可以调用delete方法执行删除操作

```python
# Model 对象，通常用来删除大条数据
ret = models.UserInfo.objects.filter(id=7)[0]
ret.delete()

# QuerySet 通常删除批量数据。删除所有价格为50的书籍信息
ret = models.Book.objects.filter(price=50)
ret.delete()
```



## ORM 多表





## 序列化

