# recommend

## 环境

* NodeJS
* Python
* Git
* Spark
* VSCode

## 步骤

### 安装VSCode

### 安装Git，从Github上拉去代码

### 安装NodeJS
1、下载地址 <https://nodejs.org/en/> 并安装好
2、定位到 www目录
3、执行 npm i
4、运行 npm run dev



### 安装Spark
参照 。。。


1. Hadoop出现错误：WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable，解决方案
1、下载地址 <https://www.python.org/>
2、定位到Server Calc目录
3、执行 pip install -r requirements.txt 安装项目依赖
4、执行python server.py 启动站点
5、前端发起ajax请求请求数据





https://www.cnblogs.com/likui360/p/6558749.html

2. spark 安装
https://blog.csdn.net/ouyangyanlan/article/details/52355350

3. spark 执行顺序
https://blog.csdn.net/gou290966707/article/details/76546450

4. 一个电影系统



## 新的阿里云上面安装 

### 安装 Git

yum install -y git

生成SSH key并加到github上

`ssh-keygen -t RSA -c 'xxxx'`

复制仓库
`git@github.com:shijinghua2/recommend.git`

### 安装 python3

参考 https://www.cnblogs.com/ltz150/p/7228464.htmlmake

yum -y install zlib*

### 安装scala
参考 https://blog.csdn.net/bahaidong/article/details/44220633
下载地址使用 https://blog.csdn.net/bahaidong/article/details/

### 安装Spark
安装：https://blog.csdn.net/coffeeandice/article/details/78879151

### 安装Hadoop
安装：https://blog.csdn.net/coffeeandice/article/details/78879151
问题：https://blog.csdn.net/u013725455/article/details/70147331

### 安装sqlite3
https://blog.csdn.net/superbfly/article/details/35779697 方法2

### 安装redis
https://blog.csdn.net/ul646691993/article/details/52736279

要开的端口
* spark
    4040
    8080
* hadoop
    8088
    8042
* pycharm
    5432
* redis
    6379


## 可以改进的地方

注册用户
用户行为，评分 动态增加计算银子

## 操作


为什么有了Spark还要再用一个数据库，因为数据库对于结构化的数据很友好，存取筛选起来比较清晰，而Spark主要用于计算，本实例中，Spark用于计算推荐给用户的书籍及预测用户评分


进行计算的时候可以访问 http://47.106.32.55:4040 实时查看任务状态


## 启动服务端

使用SSH工具连接上阿里云主机，执行

```bash
cd /root/git/recommend/Server/Calc
spark-submit server.py
```


### 登录

输入UID进行登录，登录信息保存在 sqlite 里面，前端使用localStorage进行存储

登陆的UID从有评分的用户里面取，比如 233737

### 评分最高

取的是当前数据库里平均评分最高的图书

### 热门图书

取的是豆瓣的热门图书

### 猜你喜欢

未登录时，不显示此模块，按照推荐算法得出的对应于每个用户的最佳图书

缓存，Spark本身会有缓存，另外再用Redis做了一层缓存，加快存取速度