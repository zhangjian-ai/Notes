# Nginx 简介

## Nginx 概述

Nginx ("engine x") 是一个高性能的 HTTP 和反向代理服务器,特点是占有内存少，并发能力强，事实上 nginx 的并发能力确实在同类型的网页服务器中表现较好。

## Nginx 作为 web 服务

Nginx 可以作为静态页面的 web 服务器，同时还支持 CGI 协议的动态语言，比如 perl、php等。但是不支持 java。Java程序只能通过与 tomcat 配合完成。Nginx 专为性能优化而开发，性能是其最重要的考量，实现上非常注重效率 ，能经受高负载的考验，有报告表明能支持高达 50,000 个并发连接数。

## 正向代理

Nginx不仅可以做反向代理，实现负载均衡。还能用作正向代理来进行上网等功能。如果把局域网外的 Internet 想象成一个巨大的资源库，则局域网中的客户端要访问 Internet，则需要通过代理服务器来访问，这种代理服务就称为正向代理。

## 反向代理

反向代理，其实客户端对代理是无感知的，因为客户端不需要任何配置就可以访问，我们只需要将请求发送到反向代理服务器，由反向代理服务器去选择目标服务器获取数据后，在返回给客户端，此时反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器地址，隐藏了真实服务器IP地址。

## 负载均衡

客户端发送多个请求到服务器，服务器处理请求，有一些可能要与数据库进行交互，服务器处理完毕后，再将结果返回给客户端。这种架构模式对于早期的系统相对单一，并发请求相对较少的情况下是比较适合的，成本也低。

但是随着信息数量的不断增长，访问量和数据量的飞速增长，以及系统业务的复杂度增加，这种架构会造成服务器相应客户端的请求日益缓慢，并发量特别大的时候，还容易造成服务器直接崩溃。

很明显这是由于服务器性能的瓶颈造成的问题，那么如何解决这种情况呢？

我们首先想到的可能是升级服务器的配置，比如提高 CPU 执行频率，加大内存等提高机器的物理性能来解决此问题，但是我们知道摩尔定律的日益失效，硬件的性能提升已经不能满足日益提升的需求了。最明显的一个例子，天猫双十一当天，某个热销商品的瞬时访问量是极其庞大的，那么类似上面的系统架构，将机器都增加到现有的顶级物理配置，都是不能够满足需求的。那么怎么办呢？上面的分析我们去掉了增加服务器物理配置来解决问题的办法，也就是说纵向解决问题的办法行不通了，那么横向增加服务器的数量呢？这时候集群的概念产生了，**单个服务器解决不了，就增加服务器的数量，然后将请求分发到各个服务器上，将原先请求集中到单个服务器上的情况改为将请求分发到多个服务器上，将请求负载分发到不同的服务器。**



## 动静分离

为了加快网站的解析速度，可把动态页面和静态页面由不同的服务器来解析，加快解析速度，降低原来单个服务器的压力。



## 环境搭建

> 基于Docker

```shell
# 先创建一个临时的nginx，将其配置文件等目录拷贝出来
mkdir -p /var/local/myapp/nginx/conf
mkdir -p /var/local/myapp/nginx/logs

docker run -d --name temp_nginx nginx
docker cp temp_nginx:/etc/nginx/nginx.conf /var/local/myapp/nginx/conf/nginx.conf
docker cp temp_nginx:/usr/share/nginx/html /var/local/myapp/nginx/
docker cp temp_nginx:/var/log/nginx /var/local/myapp/nginx/logs

# 删除临时容器
docker rm -f temp_nginx

# =========================================
# 启动容器，将刚才的目录挂载进去，后续修改了配置，重启容器即可
docker run -d -p 80:80 --restart=always --name=nginx -v /var/local/myapp/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /var/local/myapp/nginx/html:/usr/share/nginx/html -v /var/local/myapp/nginx/logs:/var/log/nginx nginx
```





# Nginx 配置文件

## 配置文件 结构

### 全局块

配置服务器整体运行的配置指令，比如 worker_processes 1。处理并发数的配置。worker_processes 值越大，可以支持的并发处理量也越多。

### events 块

影响 Nginx 服务器与用户的网络连接，比如 worker_connections 1024； 支持的最大连接数为 1024。

### http 块

代理、缓存和日志定义等绝大多数功能和第三方模块的配置。

http块还可以继续细分成如下两个块：

- **http 全局块：**http 全局块配置的指令包括文件引入、MIME-TYPE 定义、日志自定义、连接超时时间、单链接请求数上限等。
- **server块：**每个 http 块可以包括多个 server 块，而每个 server 块就相当于一个虚拟主机。而每个 server 块也分为全局 server 块，以及可以同时包含多个 location 块。
  - 全局 server 块：最常见的配置是本虚拟机主机的监听配置和本虚拟主机的名称或 IP 配置。
  - location 块：一个 server 块可以配置多个 location 块。这块的主要作用是基于 Nginx 服务器接收到的请求字符串（例如 server_name/uri-string），对虚拟主机名称（也可以是 IP 别名）之外的字符串（例如 前面的 /uri-string）进行匹配，对特定的请求进行处理。地址定向、数据缓存和应答控制等功能，还有许多第三方模块的配置也在这里进行。



**http块结构示例：**

```shell
http {                      # 这个是协议级别。从这里开始到server之前就是http全局块
　　include mime.types;
　　default_type application/octet-stream;
　　keepalive_timeout 65;
　　gzip on;
　　　　server {             # 这个是服务器级别。从这里开始到location之前就是server全局块
　　　　　　listen 80;
　　　　　　server_name localhost;
　　　　　　　　location / {  # 这个是请求级别
　　　　　　　　　　root html;
　　　　　　　　　　index index.html index.htm;
　　　　　　　　}
　　　　　　}
}
```



### location 块

> - location 是在 server 块中配置，根据不同的 URl使用不同的配置，来处理不同的请求。
>
> - location 是有顺序的，会被第一个匹配的location 处理。
>
> - 基本语法如下：
>
>   ```shell
>   # 匹配URL类型，有四种参数可选，当然也可以不带参数。
>   location [=|~|~*|^~] pattern{……}
>   
>   # 命名location，用@标识，类似于定于goto语句块。
>   location @name { … }
>   ```
>
> - location 前缀含义：
>
>   ```shell
>   =    表示精确匹配，优先级也是最高的 
>   ^~   表示url以某个常规字符串开头,理解为匹配url路径即可 
>   ~    表示区分大小写的正则匹配  
>   ~*   表示不区分大小写的正则匹配
>   !~   表示区分大小写不匹配的正则
>   !~*  表示不区分大小写不匹配的正则
>   /    通用匹配，任何请求都会匹配到
>   ```

#### 配置示例

1. `=` 精确匹配，一旦匹配成功，则不再查找其他匹配项。

   ```shell
   location = /abc/ {
     .....
    }
           
   # 只匹配http://abc.com/abc
   # http://abc.com/abc [匹配成功]
   # http://abc.com/abc/index [匹配失败]
   ```

2. `~`执行正则匹配，区分大小写

   ```shell
   location ~ /Abc/ {
     .....
   }
   # http://abc.com/Abc/ [匹配成功]
   # http://abc.com/abc/ [匹配失败]
   ```

3. `~*`执行正则匹配，不区分大小写

   ```shell
   location ~* /Abc/ {
     .....
   }
   # 则会忽略 uri 部分的大小写
   # http://abc.com/Abc/ [匹配成功]
   # http://abc.com/abc/ [匹配成功]
   ```

4. `^~`表示匹配普通字符串，类似 前缀匹配。一旦匹配成功，则不再查找其他匹配项。

   ```shell
   location ^~ /index/ {
     .....
   }
   # 以 /index/ 开头的请求，都会匹配上
   # http://abc.com/index/index.page  [匹配成功]
   # http://abc.com/error/error.page [匹配失败]
   ```

5. 不加任何规则时，默认是大小写敏感，前缀匹配

   ```shell
   location /index/ {
     ......
   }
   # http://abc.com/index  [匹配成功]
   # http://abc.com/index/index.page  [匹配成功]
   # http://abc.com/test/index  [匹配失败]
   # http://abc.com/Index  [匹配失败]
   # 匹配到所有uri
   ```

6. `@` Nginx 内部跳转

   ```shell
   location /index/ {
     error_page 404 @index_error;
   }
   location @index_error {
     .....
   }
   # 以 /index/ 开头的请求，如果链接的状态为 404。则会匹配到 @index_error 这条规则上。
   ```

7. `/` 表示全匹配，所有URI都将被匹配

   ```shell
   location / { ... }
   
   # http://abc.com/index  [匹配成功]
   # http://abc.com/test/index  [匹配成功]
   # http://abc.com/  [匹配成功]
   ```



#### 匹配优先级

`=` > `^~` > `~ | ~* | !~ | !~*` > 前缀匹配 > `/`

**说明：**

```shell
# 按优先级从上往下排
# ---------------
location = 			# 精准匹配，匹配优先级最高。一旦匹配成功，则不再查找其他匹配项。
location ^~ 		# 带参前缀匹配，一旦匹配成功，则不再查找其他匹配项。
location ~ 			# 正则匹配（区分大小写）
location ~* 		# 正则匹配（不区分大小写）
location /a 		# 普通前缀匹配，优先级低于带参数前缀匹配。
location / 			# 任何没有匹配成功的，都会匹配这里处理
```



**示例：**

```shell
location = /  {
#规则A
}

location = /login {
#规则B
}

location ^~ /static/ {
#规则C
}

location ~ \.(gif|jpg|png|js|css)$ {
#规则D
}

location ~* \.png$ {
#规则E
}

location !~ \.xhtml$ {
#规则F
}

location !~* \.xhtml$ {
#规则G
}

location /static/ {
#规则H
}

location / {
#规则I
}

# =======================================
# 访问 http://localhost/ 										匹配 规则A
# 访问 http://localhost/login								匹配 规则B
# 访问 http://localhost/register						匹配 规则I
# 访问 http://localhost/static/a.html				匹配 规则C 和 规则H，但带参前缀匹配优先级更高，最终走 规则C
# 访问 http://localhost/b.png								匹配 规则D 和 规则E，但 规则D优先级更高
# 访问 http://localhost/static/c.png				匹配 规则C 和 规则H，但带参前缀匹配优先级更高，最终走 规则C
# 访问 http://localhost/a.PNG								匹配 规则E
# 访问 http://localhost/a.xhtml							不会匹配 规则F 和 规则G，规则F，规则G属于排除法，符合规则就不匹配。
# 访问 http://localhost/a.XHTML							不会匹配 规则G
# 访问 http://localhost/qll/id/1111 				匹配 规则I
```



#### URI 结尾带不带 `/`

1. 如果 URI 结构是  https://domain.com/ 的形式，尾部有没有 / 都不会造成重定向。因为浏览器在发起请求的时候，默认加上了 / 。虽然很多浏览器在地址栏里也不会显示 / 。
2. 如果 URI 的结构是 https://domain.com/some-dir/ 。尾部如果缺少 / 将导致重定向。因为根据 **约定，URL 尾部的 / 表示目录，没有 / 表示文件**。所以访问 /some-dir/ 时，服务器会自动去该目录下找对应的默认文件。如果访问 /some-dir 的话，服务器会先去找 some-dir 文件，找不到的话会将 some-dir 当成目录，重定向到 /some-dir/ ，去该目录下找默认文件。



#### root 和 alias 指令区别

> - alias 是为 目录路径 定义一个别名；
> - root 是为 location 后面的 目录路径 指定 从根路径开始的 上层路径。

```shell
location /img {
    alias /var/www/image/;
}
# 若按照上述配置的话，则访问/img/目录下的文件时，ningx会自动去/var/www/image/目录找文件

location /img {
    root /var/www/image;
} 
# 若按照这种配置的话，则访问/img/目录下的文件时，nginx会去/var/www/image/img/目录下找文件。
```



#### if 判断指令

语法为if(condition){...}，对给定的条件condition进行判断。如果为真，大括号内的rewrite指令将被执行，if条件(conditon)可以是如下任何内容：

1. 当表达式只是一个变量时，如果值为空或任何以0开头的字符串都会当做false；
2. 直接比较变量和内容时，使用=或!=；
3. 正则匹配，匹配前缀和 location 的前缀使用方式相同。

> if指令相关的指令集系统变量：
>
> **指令：**
>
> ```shell
> -f和!-f用来判断是否存在文件
> -d和!-d用来判断是否存在目录
> -e和!-e用来判断是否存在文件或目录
> -x和!-x用来判断文件是否可执行
> ```
>
> **系统变量：**
>
> ```shell
> $args ： 这个变量等于请求行中的参数，同$query_string
> $content_length ： 请求头中的Content-length字段。
> $content_type ： 请求头中的Content-Type字段。
> $document_root ： 当前请求在root指令中指定的值。
> $host ： 请求主机头字段，否则为服务器名称。
> $http_user_agent ： 客户端agent信息
> $http_cookie ： 客户端cookie信息
> $limit_rate ： 这个变量可以限制连接速率。
> $request_method ： 客户端请求的动作，通常为GET或POST。
> $remote_addr ： 客户端的IP地址。
> $remote_port ： 客户端的端口。
> $remote_user ： 已经经过Auth Basic Module验证的用户名。
> $request_filename ： 当前请求的文件路径，由root或alias指令与URI请求生成。
> $scheme ： HTTP方法（如http，https）。
> $server_protocol ： 请求使用的协议，通常是HTTP/1.0或HTTP/1.1。
> $server_addr ： 服务器地址，在完成一次系统调用后可以确定这个值。
> $server_name ： 服务器名称。
> $server_port ： 请求到达服务器的端口号。
> $request_uri ： 包含请求参数的原始URI，不包含主机名，如：”/foo/bar.php?arg=baz”。
> $uri ： 不带请求参数的当前URI，$uri不包含主机名，如”/foo/bar.html”。
> $document_uri ： 与$uri相同。
> ```

```shell
if ($http_user_agent ~ MSIE) {
    rewrite ^(.*)$ /msie/$1 break;
} //如果UA包含"MSIE"，rewrite请求到/msid/目录下
 
if ($http_cookie ~* "id=([^;]+)(?:;|$)") {
    set $id $1;
 } //如果cookie匹配正则，设置变量$id等于正则引用部分
 
if ($request_method = POST) {
    return 405;
} //如果提交方法为POST，则返回状态405（Method not allowed）。return不能返回301,302
 
if ($slow) {
    limit_rate 10k;
} //限速，$slow可以通过 set 指令设置
 
if (!-f $request_filename){
    break;
    proxy_pass  http://127.0.0.1; 
} //如果请求的文件名不存在，则反向代理到localhost 。这里的break也是停止rewrite检查
 
if ($args ~ post=140){
    rewrite ^ http://example.com/ permanent;
} //如果query string中包含"post=140"，永久重定向到example.com
 
location ~* \.(gif|jpg|png|swf|flv)$ {
    valid_referers none blocked www.jefflei.com www.leizhenfang.com;
    if ($invalid_referer) {
        return 404;
    } //防盗链
}
```



#### rewrite 

rewrite功能就是，使用nginx提供的全局变量或自己设置的变量，结合正则表达式和标志位实现url重写以及重定向。rewrite只能放在server{},location{},if{}中，并且只能对域名后边的除去传递的参数外的字符串起作用，例如 http://seanlook.com/a/we/index.php?id=1&u=str 只对/a/we/index.php重写。语法`rewrite regex replacement [flag]`;

如果相对域名或参数字符串起作用，可以使用全局变量匹配，也可以使用proxy_pass反向代理。

表明看rewrite和location功能有点像，都能实现跳转，主要区别在于rewrite是在同一域名内更改获取资源的路径，而location是对一类路径做控制访问或反向代理，可以proxy_pass到其他机器。很多情况下rewrite也会写在location里，它们的执行顺序是：

```
1. 执行server块的rewrite指令
2. 执行location匹配
3. 执行选定的location中的rewrite指令
```

如果其中某步URI被重写，则重新循环执行1-3，直到找到真实存在的文件；循环超过10次，则返回500 Internal Server Error错误。



**示例一：**

> 对形如/images/ef/uh7b3/test.png的请求，重写到/data?file=test.png，于是匹配到location /data，先看/data/images/test.png文件存不存在，如果存在则正常响应，如果不存在则重写tryfiles到新的image404 location，直接返回404状态码。

```shell
http {
    # 定义image日志格式
    log_format imagelog '[$time_local] ' $image_file ' ' $image_type ' ' $body_bytes_sent ' ' $status;
    # 开启重写日志
    rewrite_log on;
 
    server {
        root /home/www;
 
        location / {
                # 重写规则信息
                error_log logs/rewrite.log notice; 
                # 注意这里要用‘’单引号引起来，避免{}
								# $3、$4 表示第三第四个正则编组匹配到的值
                rewrite '^/images/([a-z]{2})/([a-z0-9]{5})/(.*)\.(png|jpg|gif)$' /data?file=$3.$4;
                # 注意不能在上面这条规则后面加上“last”参数，否则下面的set指令不会执行
                set $image_file $3;
                set $image_type $4;
        }
 
        location /data {
                # 指定针对图片的日志格式，来分析图片类型和大小
                access_log logs/images.log mian;
                root /data/images;
                # 应用前面定义的变量。判断首先文件在不在，不在再判断目录在不在，如果还不在就跳转到最后一个url里
                try_files $image_file /image404.html;
        }
        location = /image404.html {
                # 图片不存在返回特定的信息
                return 404 "image not found\n";
        }
}
```



**示例二：**

> 对形如`/images/bla_500x400.jpg`的文件请求，重写到`/resizer/bla.jpg?width=500&height=400`地址，并会继续尝试匹配location。

```shell
# last的作用是终止在当前块中继续执行语句
rewrite '^/images/(.*)_(\d+)x(\d+).(png|jpg|gif)' /resizer/$1.$4?width=$2&height=$3 last;
```



#### try_files

Nginx的配置语法灵活，可控制度非常高。在0.7以后的版本中加入了一个try_files指令，配合location，可以部分替代原本常用的rewrite配置方式，提高解析效率。

**语法：**

```shell
# 方式一
try_files file ... uri; 

# 方式二
try_files file ... =code;
```

**语法解析：**

- 按指定的file顺序查找存在的文件，并使用第一个找到的文件进行请求处理；
- 查找路径是按照给定的root或alias为根路径来查找的；
- 如果给出的file都没有匹配到，则重新请求最后一个参数给定的uri，就是新的location匹配；
- 如果是格式2，如果最后一个参数是 = 404 ，若给出的file都没有匹配到，则最后返回404的响应码。



**示例一：**

```shell
location /images/ {
    root /opt/html/;
    try_files $uri $uri/ /images/default.gif; 
}

# 访问 http://127.0.0.1/images/test.gif
# $uri: /images/test.gif。查找顺序如下:
# 1. 查找 /opt/html/images/test.gif 是否存在，存在则直接返回，否则进入下一步；
# 2. 查找 /opt/html/images/test.gif/index.html 是否存在，不存在进入下一步；
# 3. 直接请求 127.0.0.1/images/default.gif。 这里 等同于重新给 $uri 赋值后直接请求资源。
```



**示例二：**

```shell
location / {
    try_files /system/maintenance.html
              $uri $uri/index.html $uri.html
              @mongrel;
}

location @mongrel { # 以上中若未找到给定顺序的文件，则将会交给location @mongrel处理
    proxy_pass http://mongrel;
}
```





#### 配置建议

实际使用中，通常建议至少有三个匹配规则定义，如下：

```shell
# 直接匹配网站根，通过域名访问网站首页比较频繁，使用这个会加速处理，比如说官网。
# 这里是直接转发给后端应用服务器了，也可以是一个静态首页
# 第一个必选规则
location = / {
    proxy_pass http://localhost:8080/index
}
# 第二个必选规则是处理静态文件请求，这是nginx作为http服务器的强项
# 有两种配置模式，前缀匹配或后缀匹配,任选其一或搭配使用
location ^~ /static/ {
    root /webroot/static/;
}
location ~* \.(gif|jpg|jpeg|png|css|js|ico)$ {
    root /webroot/res/;
}
# 第三个规则就是通用规则，用来转发动态请求到后端应用服务器
# 非静态文件请求就默认是动态请求，自己根据实际把握
# 毕竟目前的一些框架的流行，带.php,.jsp后缀的情况很少了
location / {
    proxy_pass http://localhost:8080/
}
```





## 配置文件 参数详解

```shell
######Nginx配置文件nginx.conf中文详解#####

#定义Nginx运行的用户和用户组
user www www;

#nginx进程数，建议设置为等于CPU总核心数。
worker_processes 8;
 
#全局错误日志定义类型，[ debug | info | notice | warn | error | crit ]
error_log /usr/local/nginx/logs/error.log info;

#进程pid文件
pid /usr/local/nginx/logs/nginx.pid;

#指定进程可以打开的最大描述符：数目
#工作模式与连接数上限
#这个指令是指当一个nginx进程打开的最多文件描述符数目，理论值应该是最多打开文件数（ulimit -n）与nginx进程数相除，但是nginx分配请求并不是那么均匀，所以最好与ulimit -n 的值保持一致。
#现在在linux 2.6内核下开启文件打开数为65535，worker_rlimit_nofile就相应应该填写65535。
#这是因为nginx调度时分配请求到进程并不是那么的均衡，所以假如填写10240，总并发量达到3-4万时就有进程可能超过10240了，这时会返回502错误。
worker_rlimit_nofile 65535;


events
{
    #参考事件模型，use [ kqueue | rtsig | epoll | /dev/poll | select | poll ];
    #epoll模型 是Linux 2.6以上版本内核中的高性能网络I/O模型，linux建议epoll，如果跑在FreeBSD上面，就用kqueue模型。
    #补充说明：
    #与apache相类，nginx针对不同的操作系统，有不同的事件模型
    #A）标准事件模型
    #Select、poll属于标准事件模型，如果当前系统不存在更有效的方法，nginx会选择select或poll
    #B）高效事件模型
    #Kqueue：使用于FreeBSD 4.1+, OpenBSD 2.9+, NetBSD 2.0 和 MacOS X.使用双处理器的MacOS X系统使用kqueue可能会造成内核崩溃。
    #Epoll：使用于Linux内核2.6版本及以后的系统。
    #/dev/poll：使用于Solaris 7 11/99+，HP/UX 11.22+ (eventport)，IRIX 6.5.15+ 和 Tru64 UNIX 5.1A+。
    # Eventport：使用于Solaris 10。 为了防止出现内核崩溃的问题， 有必要安装安全补丁。
    use epoll;

    #单个进程最大连接数（最大连接数=连接数*进程数）
    #根据硬件调整，和前面工作进程配合起来用，尽量大，但是别把cpu跑到100%就行。每个进程允许的最多连接数，理论上每台nginx服务器的最大连接数为 65535，通常建议配置为 1024。
    worker_connections 1024;

    #keepalive超时时间。
    keepalive_timeout 60;

    #客户端请求头部的缓冲区大小。这个可以根据你的系统分页大小来设置，一般一个请求头的大小不会超过1k，不过由于一般系统分页都要大于1k，所以这里设置为分页大小。
    #分页大小可以用shell命令 getconf PAGESIZE 取得。
    #[root@web001 ~]# getconf PAGESIZE
    #4096
    #
    #但也有client_header_buffer_size超过4k的情况，但是client_header_buffer_size该值必须设置为“系统分页大小”的整倍数。
    client_header_buffer_size 4k;

    #这个将为打开文件指定缓存，默认是没有启用的，max指定缓存数量，建议和打开文件数一致，inactive是指经过多长时间文件没被请求后删除缓存。
    open_file_cache max=65535 inactive=60s;

    #这个是指多长时间检查一次缓存的有效信息。
    #语法:open_file_cache_valid time 默认值:open_file_cache_valid 60 使用字段:http, server, location 这个指令指定了何时需要检查open_file_cache中缓存项目的有效信息.
    open_file_cache_valid 80s;

    #open_file_cache指令中的inactive参数时间内文件的最少使用次数，如果超过这个数字，文件描述符一直是在缓存中打开的，如上例，如果有一个文件在inactive时间内一次没被使用，它将被移除。
    #语法:open_file_cache_min_uses number 默认值:open_file_cache_min_uses 1 使用字段:http, server, location  这个指令指定了在open_file_cache指令无效的参数中一定的时间范围内可以使用的最小文件数,如果使用更大的值,文件描述符在cache中总是打开状态.
    open_file_cache_min_uses 1;
    
    #语法:open_file_cache_errors on | off 默认值:open_file_cache_errors off 使用字段:http, server, location 这个指令指定是否在搜索一个文件是记录cache错误.
    open_file_cache_errors on;
}
 
 
 
#设定http服务器，利用它的反向代理功能提供负载均衡支持
http
{
    #文件扩展名与文件类型映射表
    include mime.types;

    #默认文件类型
    default_type application/octet-stream;

    #默认编码
    #charset utf-8;

    #服务器名字的hash表大小
    #保存服务器名字的hash表是由指令server_names_hash_max_size 和server_names_hash_bucket_size所控制的。参数hash bucket size总是等于hash表的大小，并且是一路处理器缓存大小的倍数。在减少了在内存中的存取次数后，使在处理器中加速查找hash表键值成为可能。如果hash bucket size等于一路处理器缓存的大小，那么在查找键的时候，最坏的情况下在内存中查找的次数为2。第一次是确定存储单元的地址，第二次是在存储单元中查找键 值。因此，如果Nginx给出需要增大hash max size 或 hash bucket size的提示，那么首要的是增大前一个参数的大小.
    server_names_hash_bucket_size 128;

    #客户端请求头部的缓冲区大小。这个可以根据你的系统分页大小来设置，一般一个请求的头部大小不会超过1k，不过由于一般系统分页都要大于1k，所以这里设置为分页大小。分页大小可以用命令getconf PAGESIZE取得。
    client_header_buffer_size 32k;

    #客户请求头缓冲大小。nginx默认会用client_header_buffer_size这个buffer来读取header值，如果header过大，它会使用large_client_header_buffers来读取。
    large_client_header_buffers 4 64k;

    #设定通过nginx上传文件的大小
    client_max_body_size 8m;

    #开启高效文件传输模式，sendfile指令指定nginx是否调用sendfile函数来输出文件，对于普通应用设为 on，如果用来进行下载等应用磁盘IO重负载应用，可设置为off，以平衡磁盘与网络I/O处理速度，降低系统的负载。注意：如果图片显示不正常把这个改成off。
    #sendfile指令指定 nginx 是否调用sendfile 函数（zero copy 方式）来输出文件，对于普通应用，必须设为on。如果用来进行下载等应用磁盘IO重负载应用，可设置为off，以平衡磁盘与网络IO处理速度，降低系统uptime。
    sendfile on;

    #开启目录列表访问，合适下载服务器，默认关闭。
    autoindex on;

    #此选项允许或禁止使用socket的TCP_CORK的选项，此选项仅在使用sendfile的时候使用
    tcp_nopush on;
     
    tcp_nodelay on;

    #长连接超时时间，单位是秒
    keepalive_timeout 120;

    #FastCGI相关参数是为了改善网站的性能：减少资源占用，提高访问速度。下面参数看字面意思都能理解。
    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 64k;
    fastcgi_buffers 4 64k;
    fastcgi_busy_buffers_size 128k;
    fastcgi_temp_file_write_size 128k;

    #gzip模块设置
    gzip on; #开启gzip压缩输出
 		gzip_proxied any;
    gzip_min_length 1k;    #最小压缩文件大小
    gzip_buffers 16 8k;    #压缩缓冲区
    gzip_http_version 1.1;    #压缩版本（默认1.1，前端如果是squid2.5请使用1.0）
    gzip_comp_level 1;    #压缩等级
    gzip_types text/plain application/x-javascript text/css application/xml;    #压缩类型，默认就已经包含text/xml，所以下面就不用再写了，写上去也不会有问题，但是会有一个warn。
    gzip_vary on;

    #开启限制IP连接数的时候需要使用
    #limit_zone crawler $binary_remote_addr 10m;



    #负载均衡配置
    upstream jh.w3cschool.cn {
     
        #upstream的负载均衡，weight是权重，可以根据机器配置定义权重。weigth参数表示权值，权值越高被分配到的几率越大。
        server 192.168.80.121:80 weight=3;
        server 192.168.80.122:80 weight=2;
        server 192.168.80.123:80 weight=3;

        #nginx的upstream目前支持5种方式的分配
        #1、轮询（默认）
        #每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器down掉，能自动剔除。
        #2、weight
        #指定轮询几率，weight和访问比率成正比，用于后端服务器性能不均的情况。
        #例如：
        #upstream bakend {
        #    server 192.168.0.14 weight=10;
        #    server 192.168.0.15 weight=10;
        #}
        #3、ip_hash
        #每个请求按访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，可以解决session的问题。
        #例如：
        #upstream bakend {
        #    ip_hash;
        #    server 192.168.0.14:88;
        #    server 192.168.0.15:80;
        #}
        #4、fair（第三方）
        #按后端服务器的响应时间来分配请求，响应时间短的优先分配。
        #upstream backend {
        #    server server1;
        #    server server2;
        #    fair;
        #}
        #5、url_hash（第三方）
        #按访问url的hash结果来分配请求，使每个url定向到同一个后端服务器，后端服务器为缓存时比较有效。
        #例：在upstream中加入hash语句，server语句中不能写入weight等其他的参数，hash_method是使用的hash算法
        #upstream backend {
        #    server squid1:3128;
        #    server squid2:3128;
        #    hash $request_uri;
        #    hash_method crc32;
        #}

        #tips:
        #upstream bakend{#定义负载均衡设备的Ip及设备状态}{
        #    ip_hash;
        #    server 127.0.0.1:9090 down;
        #    server 127.0.0.1:8080 weight=2;
        #    server 127.0.0.1:6060;
        #    server 127.0.0.1:7070 backup;
        #}
        #在需要使用负载均衡的server中增加 proxy_pass http://bakend/;

        #每个设备的状态设置为:
        #1.down表示当前的server暂时不参与负载
        #2.weight为weight越大，负载的权重就越大。
        #3.max_fails：允许请求失败的次数默认为1.当超过最大次数时，返回proxy_next_upstream模块定义的错误
        #4.fail_timeout:max_fails次失败后，暂停的时间。
        #5.backup： 其它所有的非backup机器down或者忙的时候，请求backup机器。所以这台机器压力会最轻。

        #nginx支持同时设置多组的负载均衡，用来给不用的server来使用。
        #client_body_in_file_only设置为On 可以讲client post过来的数据记录到文件中用来做debug
        #client_body_temp_path设置记录文件的目录 可以设置最多3层目录
        #location对URL进行匹配.可以进行重定向或者进行新的代理 负载均衡
    }
     
     
     
    #虚拟主机的配置
    server
    {
        #监听端口
        listen 80;

        #域名可以有多个，用空格隔开
        server_name www.w3cschool.cn w3cschool.cn;
        index index.html index.htm index.php;
        root /data/www/w3cschool;

        #对******进行负载均衡
        location ~ .*.(php|php5)?$
        {
            fastcgi_pass 127.0.0.1:9000;
            fastcgi_index index.php;
            include fastcgi.conf;
        }
         
        #图片缓存时间设置
        location ~ .*.(gif|jpg|jpeg|png|bmp|swf)?$
        {
            expires 10d;
        }
         
        #JS和CSS缓存时间设置
        location ~ .*.(js|css)?$
        {
            expires 1h;
        }
         
        #日志格式设定
        #$remote_addr与$http_x_forwarded_for用以记录客户端的ip地址；
        #$remote_user：用来记录客户端用户名称；
        #$time_local： 用来记录访问时间与时区；
        #$request： 用来记录请求的url与http协议；
        #$status： 用来记录请求状态；成功是200，
        #$body_bytes_sent ：记录发送给客户端文件主体内容大小；
        #$http_referer：用来记录从那个页面链接访问过来的；
        #$http_user_agent：记录客户浏览器的相关信息；
        #通常web服务器放在反向代理的后面，这样就不能获取到客户的IP地址了，通过$remote_add拿到的IP地址是反向代理服务器的iP地址。反向代理服务器在转发请求的http头信息中，可以增加x_forwarded_for信息，用以记录原有客户端的IP地址和原来客户端的请求的服务器地址。
        log_format access '$remote_addr - $remote_user [$time_local] "$request" '
        '$status $body_bytes_sent "$http_referer" '
        '"$http_user_agent" $http_x_forwarded_for';
         
        #定义本虚拟主机的访问日志
        access_log  /usr/local/nginx/logs/host.access.log  main;
        access_log  /usr/local/nginx/logs/host.access.404.log  log404;
         
        #对 "/" 启用反向代理
        location / {
            proxy_pass http://127.0.0.1:88;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
             
            #后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            # nginx和uwsgi配合搭建服务器，前面不需要带http://
            # include 是指定解析文件地址，把浏览器请求解析给uwsgi
            # include /etc/nginx/uwsgi_params;
            # uwsgi_pass jh.w3cschool.cn;


            #以下是一些反向代理的配置，可选。
            proxy_set_header Host $host;

            #允许客户端请求的最大单文件字节数
            client_max_body_size 10m;

            #缓冲区代理缓冲用户端请求的最大字节数，
            #如果把它设置为比较大的数值，例如256k，那么，无论使用firefox还是IE浏览器，来提交任意小于256k的图片，都很正常。如果注释该指令，使用默认的client_body_buffer_size设置，也就是操作系统页面大小的两倍，8k或者16k，问题就出现了。
            #无论使用firefox4.0还是IE8.0，提交一个比较大，200k左右的图片，都返回500 Internal Server Error错误
            client_body_buffer_size 128k;

            #表示使nginx阻止HTTP应答代码为400或者更高的应答。
            proxy_intercept_errors on;

            #后端服务器连接的超时时间_发起握手等候响应超时时间
            #nginx跟后端服务器连接超时时间(代理连接超时)
            proxy_connect_timeout 90;

            #后端服务器数据回传时间(代理发送超时)
            #后端服务器数据回传时间_就是在规定时间之内后端服务器必须传完所有的数据
            proxy_send_timeout 90;

            #连接成功后，后端服务器响应时间(代理接收超时)
            #连接成功后_等候后端服务器响应时间_其实已经进入后端的排队之中等候处理（也可以说是后端服务器处理请求的时间）
            proxy_read_timeout 90;

            #设置代理服务器（nginx）保存用户头信息的缓冲区大小
            #设置从被代理服务器读取的第一部分应答的缓冲区大小，通常情况下这部分应答中包含一个小的应答头，默认情况下这个值的大小为指令proxy_buffers中指定的一个缓冲区的大小，不过可以将其设置为更小
            proxy_buffer_size 4k;

            #proxy_buffers缓冲区，网页平均在32k以下的设置
            #设置用于读取应答（来自被代理服务器）的缓冲区数目和大小，默认情况也为分页大小，根据操作系统的不同可能是4k或者8k
            proxy_buffers 4 32k;

            #高负荷下缓冲大小（proxy_buffers*2）
            proxy_busy_buffers_size 64k;

            #设置在写入proxy_temp_path时数据的大小，预防一个工作进程在传递文件时阻塞太长
            #设定缓存文件夹大小，大于这个值，将从upstream服务器传
            proxy_temp_file_write_size 64k;
        }
         
         
        #设定查看Nginx状态的地址
        location /NginxStatus {
            stub_status on;
            access_log on;
            auth_basic "NginxStatus";
            auth_basic_user_file confpasswd;
            #htpasswd文件的内容可以用apache提供的htpasswd工具来产生。
        }
         
        #本地动静分离反向代理配置
        #所有jsp的页面均交由tomcat或resin处理
        location ~ .(jsp|jspx|do)?$ {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://127.0.0.1:8080;
        }
         
        #所有静态文件由nginx直接读取不经过tomcat或resin
        location ~ .*.(htm|html|gif|jpg|jpeg|png|bmp|swf|ioc|rar|zip|txt|flv|mid|doc|ppt|
        pdf|xls|mp3|wma)$
        {
            expires 15d; 
        }
         
        location ~ .*.(js|css)?$
        {
            expires 1h;
        }
    }
}
```





# Nginx 反向代理

反向代理，其实客户端对代理是无感知的，因为客户端不需要任何配置就可以访问，我们只需要将请求发送到反向代理服务器，由反向代理服务器去选择目标服务器获取数据后，在返回给客户端，此时反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器地址，隐藏了真实服务器IP地址。



**示例：**

```shell
server {
	listen 80;
	server_name 127.0.0.1;
	location = / {  # 精确匹配
		proxy_pass http://121.4.47.229:9200;
		}

	location ^~ /_cat/   {  # 前缀匹配
		proxy_pass http://121.4.47.229:9200;
		}

	}
	
	# 反向代理中还有一些可选参数，详见 配置文件 参数详解
```



# Nginx 负载均衡

负载均衡配置搭建，需要在 http块 中 引入 uptream 块，在 upstream 中配置具体的负载机和均衡策略。

**配置示例：见 配置文件 参数详解**



# Nginx 动静分离

通过 location 路由，将动态请求和静态文件请求分开。

```shell
# 第二个必选规则是处理静态文件请求，这是nginx作为http服务器的强项
# 有两种配置模式，前缀匹配或后缀匹配,任选其一或搭配使用
location ^~ /static/ {
    root /webroot/static/;
}
location ~* \.(gif|jpg|jpeg|png|css|js|ico)$ {
    root /webroot/res/;
}
# 第三个规则就是通用规则，用来转发动态请求到后端应用服务器
# 非静态文件请求就默认是动态请求，自己根据实际把握
# 毕竟目前的一些框架的流行，带.php,.jsp后缀的情况很少了
location / {
    proxy_pass http://localhost:8080/
}
```



# Nginx 配置示例

## http

```shell
#注意，upstream 部分放置在 server 块之外,至少需要一个服务器ip。 
upstream  goskeleton_list {
    # 设置负载均衡模式为ip算法模式，这样不同的客户端每次请求都会与第一次建立对话的后端服务器进行交互
    # ip_hash 可以有效解决 session 共享问题
    ip_hash;
    server  127.0.0.1:20202  ;
    server  127.0.0.1:20203  ;
}
server{
    #监听端口
    listen 80  ; 
    #  站点域名，没有的话，写项目名称即可
    server_name     www.ginskeleton.com ;  
    root            /home/wwwroot/goproject2020/goskeleton/public;
    index           index.htm  index.html;   
    charset         utf-8 ;
    
    # 使用 nginx 直接接管静态资源目录
    # 由于 ginskeleton 把路由(public)地址绑定到了同名称的目录 public ，所以我们就用 nginx 接管这个资源路由
    location ~  /public/(.*)  {
        # 使用我们已经定义好的 root 目录，然后截取用户请求时，public 后面的所有地址，直接响应资源，不存在就返回404
        # 这里就是查找 /home/wwwroot/goproject2020/goskeleton/public/$1 是否存在，不存在则 返回404
        try_files  /$1   =404;  # $1 就是路径中编组匹配到的值
        
     }

    
     location ~ / {
         # 静态资源、目录交给ngixn本身处理，动态路由请求执行后续的代理代码
         try_files $uri $uri/  @goskeleton;
     }
    location   @goskeleton {

        #将客户端的ip和头域信息一并转发到后端服务器  
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # 转发Cookie，设置 SameSite
        proxy_cookie_path / "/; secure; HttpOnly; SameSite=strict";

        # 最后，执行代理访问真实服务器
        proxy_pass http://goskeleton_list;
    
    }
     # 以下是静态资源缓存配置
     location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
     {
         expires      30d;
     }

     location ~ .*\.(js|css)?$
     {
         expires      12h;
     }

     location ~ /\.
     {
         deny all;
     }
}
```



## websocket

```shell
upstream  ws_list {
    ip_hash;
    server  192.168.251.149:20175  ;
    #server  192.168.251.149:20176  ;
}

server {
    listen       20175;
    server_name  localhost;

    location / {
    		# websocket 主要增加下面这一部分
    		proxy_pass http://ws_list;
    		
        proxy_http_version 1.1;
        proxy_set_header Upgrade websocket;
        proxy_set_header Connection Upgrade;
        proxy_read_timeout 60s ;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;

        proxy_cookie_path / "/; secure; HttpOnly; SameSite=strict";
    }


     location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
     {
         expires      30d;
     }

     location ~ .*\.(js|css)?$
     {
         expires      12h;
     }

     location ~ /\.
     {
         deny all;
     }
}
```



## https

> 1. 基于 `http` 内容稍作修改即可。
> 2. 相关域名、云服务器都必须备案,否则无法通过域名访问，但是仍然可以通过 `http://云服务器ip` 访问,只不过通过ip访问会浏览器地址栏会提示不安全。

```shell
#注意，upstream 部分放置在 server 块之外,至少需要一个服务器ip。 
upstream  goskeleton_list {
    # 设置负载均衡模式为ip算法模式，这样不同的客户端每次请求都会与第一次建立对话的后端服务器进行交互
    ip_hash;
    server  127.0.0.1:20202  ;
    server  127.0.0.1:20203  ;
}
# 这里主要是将 http 访问重定向到 https，这样就能同时支持 http 和 https 访问
server {
    listen 80;
    server_name www.ginskeleton.com;
    rewrite ^(.*)$ https://$host$1  permanent;
}

server{
    #监听端口
    listen 443 ssl  ; 
    #  站点域名，没有的话，写项目名称即可
    server_name     www.ginskeleton.com ;  
    root            /home/wwwroot/goproject2020/goskeleton/public ;
    index           index.html  index.htm ;   
    charset         utf-8 ;

    # 配置 https 证书
    # ssl on;  #  注意，在很早的低版本nginx上，此项是允许打开的，但是在高于 1.1x.x 版本要求必须关闭.
    ssl_certificate      ginskeleton.crt;   # 实际配置建议指定证书的绝对路径
    ssl_certificate_key  ginskeleton.key;   # ginskeleton.crt 、ginskeleton.key 需要向云服务器厂商申请，后续有介绍
    ssl_session_timeout  5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 SSLv2 SSLv3;
    ssl_ciphers ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
    ssl_prefer_server_ciphers on;
    
    # 使用 nginx 直接接管静态资源目录
    # 由于 ginskeleton 把路由(public)地址绑定到了同名称的目录 public ，所以我们就用 nginx 接管这个资源路由
    location ~  /public/(.*)  {
        # 使用我们已经定义好的 root 目录，然后截取用户请求时，public 后面的所有地址，直接响应资源，不存在就返回404
        try_files  /$1   =404;
     }
     
     location ~ / {
         # 静态资源、目录交给ngixn本身处理，动态路由请求执行后续的代理代码
         try_files $uri $uri/  @goskeleton;
     }
    // 这里的 @goskeleton 和 try_files 语法块的名称必须一致 
    location   @goskeleton {

        #将客户端的ip和头域信息一并转发到后端服务器  
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # 转发Cookie，设置 SameSite
        proxy_cookie_path / "/; secure; HttpOnly; SameSite=strict";

        # 最后，执行代理访问真实服务器
        proxy_pass http://goskeleton_list   ;
    
    }
     # 以下是静态资源缓存配置
     location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
     {
         expires      30d;
     }

     location ~ .*\.(js|css)?$
     {
         expires      12h;
     }

     location ~ /\.
     {
         deny all;
     }
}
```

**关于 `https` 的简要介绍:**

> 1. 首先能保证数据在传输过程中的安全性.
> 2. 证书需要向第三方代理机构申请（华为云、阿里云、腾讯云等）, 个人证书一般都会有免费一年的体验期.
> 3. 证书申请时需要提交您的相关域名, 颁发机构会把您的域名信息和证书绑定, 最终配置在nginx, 当使用浏览器访问时, 浏览器地址栏会变成绿色安全图标.
> 4. 本次使用的 `ssl` 证书是在腾讯云申请的1年免费期证书, 申请地址：`https://console.cloud.tencent.com/ssl` , 企业证书一年至少在 3000+ 元.
> 5. 项目前置 `nginx` 服务器配置 `ssl` 证书通过`https` 协议在网络中传输数据, 当加密数据到达 `nginx` 时,瞬间会被 `http_ssl_module` 模块解密为明文,因此代理的负载均衡服务器不需要配置 `ssl` 选项.





# Nginx 原理解析

## Nginx 是如何实现高并发的？

多进程+异步非阻塞(IO多路复用+epoll)和大量的底层代码优化。

如果一个server采用一个进程负责一个request的方式，那么进程数就是并发数。正常情况下，会有很多进程一直在等待中。

而nginx采用一个master进程，多个woker进程的模式。

- master进程主要负责收集、分发请求。每当一个请求过来时，master就拉起一个worker进程负责处理这个请求。
- 同时master进程也负责监控woker的状态，保证高可靠性。
- woker进程一般设置为跟cpu核心数一致。nginx的woker进程在同一时间可以处理的请求数只受内存限制，可以处理多个请求。

Nginx 的异步非阻塞工作方式把等待时间利用起来了。在需要等待的时候，这些进程就空闲出来待命了，因此表现为少数几个进程就解决了大量的并发问题。

每进来一个request，会有一个worker进程去处理。但不是全程的处理，处理到什么程度呢?处理到可能发生阻塞的地方，比如向上游(后端)服务器转发request，并等待请求返回。那么，这个处理的worker很聪明，他会在发送完请求后，注册一个事件：“如果upstream返回了，告诉我一声，我再接着干”。于是他就休息去了。此时，如果再有request 进来，他就可以很快再按这种方式处理。而一旦上游服务器返回了，就会触发这个事件，worker才会来接手，这个request才会接着往下走。



## 为什么 Nginx 不使用多线程?

Apache: 创建多个进程或线程，而每个进程或线程都会为其分配 cpu 和内存(线程要比进程小的多，所以worker支持比perfork高的并发)，并发过大会耗光服务器资源。

Nginx: 采用单线程异步非阻塞来处理请求(管理员可以配置Nginx主进程的工作进程的数量)(epoll)，不会为每个请求分配cpu和内存资源，节省了大量资源，同时也减少了大量的CPU的上下文切换。所以才使得Nginx支持更高的并发。



## Nginx常见的优化配置有哪些?

- 调整worker_processes

指Nginx要生成的worker数量，最佳实践是每个CPU运行1个工作进程。

系统中的CPU核心数: `grep processor /proc/cpuinfo | awk '{print $3}'`

- 优化worker_connections

Nginx Web服务器可以同时提供服务的客户端数。与worker_processes结合使用时，获得每秒可以服务的客户端数

客户端数/秒=工作进程*工作者连接数

***为了最大化Nginx的全部潜力，应将worker连接设置为核心一次可以运行的允许的进程数1024。***

- 启用Gzip压缩

压缩文件大小，减少了客户端http的传输带宽，因此提高了页面加载速度

建议的gzip配置示例如下:( 在http部分内)

``` shell
#gzip模块设置
    gzip on; #开启gzip压缩输出
 		gzip_proxied any;
    gzip_min_length 1k;    #最小压缩文件大小
    gzip_buffers 16 8k;    #压缩缓冲区
    gzip_http_version 1.1;    #压缩版本（默认1.1，前端如果是squid2.5请使用1.0）
    gzip_comp_level 1;    #压缩等级
    gzip_types text/plain application/x-javascript text/css application/xml;    #压缩类型，默认就已经包含text/xml，所以下面就不用再写了，写上去也不会有问题，但是会有一个warn。
    gzip_vary on;
```

- 为静态文件启用缓存

为静态文件启用缓存，以减少带宽并提高性能，可以添加下面的命令，限定计算机缓存网页的静态文件：

``` shell
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ { 
	expires 5d; 
} 
```

- Timeouts

keepalive连接减少了打开和关闭连接所需的CPU和网络开销。

- 禁用access_logs

访问日志记录，它记录每个nginx请求，因此消耗了大量CPU资源，从而降低了nginx性能。

``` shell
# 完全禁用访问日志记录
access_log off;

# 如果必须具有访问日志记录，则启用访问日志缓冲。flush 表示日志在缓冲区保存的最长时间
access_log ``/var/log/nginx/access``.log main buffer=32k flush=1m;
```



## 502报错可能原因有哪些?

- FastCGI进程是否已经启动

- FastCGI worker进程数是否不够

- FastCGI执行时间过长

- FastCGI Buffer不够

- nginx和apache一样，有前端缓冲限制，可以调整缓冲参数
  - fastcgi_buffer_size 32k; 
  - fastcgi_buffers 8 32k; 

- Proxy Buffer不够，如果你用了Proxying，调整
  - proxy_buffer_size 16k; 
  - proxy_buffers 4 16k; 

