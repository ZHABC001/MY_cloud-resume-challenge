# Cloud Resume Challenge - 技术学习笔记

> 个人学习记录 - ZHANG BEICHUAN
> 项目: AWS 上构建简历网站
> 用途: 自学复习 + 面试准备

\---

## 目录

* [第 1 章 Web 基础三件套](#第-1-章-web-基础三件套)

  * [1.1 HTML 基础](#11-html-基础)
  * [1.2 CSS 简介](#12-css-简介)
  * [1.3 JavaScript 简介](#13-javascript-简介)
* [第 2 章 HTTP 协议](#第-2-章-http-协议)

  * [2.1 HTTP 是什么](#21-http-是什么)
  * [2.2 Headers（头部）](#22-headers头部)
  * [2.3 Body（正文）](#23-body正文)
  * [2.4 状态码](#24-状态码)
  * [2.5 CORS（跨域资源共享）](#25-cors跨域资源共享)
* [第 3 章 JSON 数据格式](#第-3-章-json-数据格式)

  * [3.1 JSON 是什么](#31-json-是什么)
  * [3.2 JSON 语法](#32-json-语法)
  * [3.3 JSON vs Python dict](#33-json-vs-python-dict)
* [第 4 章 Python / Lambda 语法](#第-4-章-python--lambda-语法)

  * [4.1 Lambda 函数结构](#41-lambda-函数结构)
  * [4.2 try / except 错误处理](#42-try--except-错误处理)
  * [4.3 boto3 使用](#43-boto3-使用)
* [第 5 章 Git 基础](#第-5-章-git-基础)
* [第 6 章 AWS 服务和创建逻辑](#第-6-章-aws-服务和创建逻辑)

  * [6.1 整体架构](#61-整体架构)
  * [6.2 S3（对象存储）](#62-s3对象存储)
  * [6.3 CloudFront（CDN）](#63-cloudfrontcdn)
  * [6.4 ACM（SSL 证书）](#64-acmssl-证书)
  * [6.5 DynamoDB（NoSQL 数据库）](#65-dynamodbnosql-数据库)
  * [6.6 Lambda（Serverless 函数）](#66-lambdaserverless-函数)
  * [6.7 IAM（权限管理）](#67-iam权限管理)
  * [6.8 API Gateway](#68-api-gateway)
* [第 7 章 服务依赖关系](#第-7-章-服务依赖关系)
* [第 8 章 关键面试要点](#第-8-章-关键面试要点)

\---

# 第 1 章 Web 基础三件套

## 1.1 HTML 基础

### HTML 是什么

```
HTML = HyperText Markup Language（超文本标记语言）
日语: ハイパーテキスト・マークアップ言語

不是编程语言，是"标记语言"
作用: 用"标签"告诉浏览器"这块内容是什么"
```

### 三件套分工

```
HTML  →  内容 + 结构  （骨架）
CSS   →  外观 + 样式  （皮肤）
JS    →  交互 + 行为  （动作）
```

### 标签基本结构

```html
<标签名>内容</标签名>
   ↑     ↑      ↑
开始标签  内容  结束标签

例:
<h1>这是标题</h1>
<p>这是段落</p>
```

### 关键规则

```
✅ 必须成对出现:    <p>...</p>
✅ 结束标签前面有斜杠: </p>
❌ 漏写会崩:       <p>...    （错）
```

### 自闭合标签（不需要结束）

```html
<img src="photo.jpg">    图片
<br>                     换行
<hr>                     水平分割线
```

### 嵌套规则

```html
✅ 后开的先关:
<外><内>...</内></外>

❌ 顺序错了:
<外><内>...</外></内>
```

### 常用标签速查

|标签|作用|例子|
|-|-|-|
|`<h1>` \~ `<h6>`|标题（数字越大越小）|`<h1>姓名</h1>`|
|`<p>`|段落（最常用）|`<p>这是一段文字</p>`|
|`<a>`|链接|`<a href="url">显示文字</a>`|
|`<img>`|图片|`<img src="path" alt="说明">`|
|`<strong>`|强调（加粗）|`<strong>重要</strong>`|
|`<ul>` `<ol>` `<li>`|列表|`<ul><li>项</li></ul>`|
|`<div>`|块级容器|`<div>...</div>`|
|`<span>`|行内容器|`<span>...</span>`|
|`<section>`|区块分组|`<section id="...">...</section>`|
|`<br>`|换行|`第一行<br>第二行`|

### 属性（Attribute）

```html
<a href="url" target="\_blank">链接</a>
   ↑    ↑     ↑      ↑
  标签  属性  属性值  另一个属性

常用属性:
href      链接地址        <a href="...">
src       图片/资源路径   <img src="...">
alt       图片说明       <img alt="...">
class     CSS 样式标识   <p class="lead">
id        唯一标识       <section id="education">
target    链接打开方式   target="\_blank"  → 新标签页
```

### 整体结构

```html
<!DOCTYPE html>            ← 声明 HTML5
<html lang="ja">           ← 文档语言
<head>                     ← 头部（用户看不到）
    <meta charset="utf-8">      字符编码
    <title>页面标题</title>      浏览器标签页标题
    <link rel="stylesheet" href="style.css">  引入 CSS
</head>
<body>                     ← 身体（用户看到的内容）
    <h1>页面标题</h1>
    <p>页面内容</p>
</body>
</html>
```

```
关键:
<head>  里的内容用户看不到（设置）
<body>  里的内容用户能看到（实际页面）
```

\---

## 1.2 CSS 简介

```
CSS = Cascading Style Sheets（层叠样式表）
日语: カスケーディングスタイルシート
作用: 控制网页外观（颜色、字体、布局、间距）
```

本项目使用 **Bootstrap 框架的工具类**，常见 class：

|Class|作用|
|-|-|
|`mb-0` \~ `mb-5`|下边距（margin-bottom）从无到大|
|`mt-4`|上边距|
|`text-primary`|主色（蓝）|
|`text-warning`|警告色（黄）|
|`d-flex`|启用 Flexbox 布局|
|`flex-column`|竖排|
|`flex-md-row`|中等屏幕以上变横排|
|`justify-content-between`|两端对齐|

\---

## 1.3 JavaScript 简介

```
JavaScript = 网页的"动作"
日语: ジャバスクリプト
英语: JavaScript

作用: 让网页有交互、调用 API、动态更新内容
本项目用途: 调用 API Gateway 获取访客数，显示在网页上
```

最简代码：

```javascript
fetch('https://api.example.com/counter')
    .then(response => response.json())
    .then(data => {
        document.getElementById('counter').innerText = data.count;
    });
```

\---

# 第 2 章 HTTP 协议

## 2.1 HTTP 是什么

```
HTTP = HyperText Transfer Protocol（超文本传输协议）
日语: ハイパーテキスト転送プロトコル

作用: 浏览器和服务器对话的"通用语言"

通信流程:
1. 浏览器发送 Request（请求）
2. 服务器返回 Response（响应）
3. 一来一回 = 一次 HTTP 通信
```

### 类比：寄信

```
一封信由两部分组成:

┌─────────────────────────┐
│ 信封信息 (Headers)       │  ← 关于这封信的信息
│ - 寄件人/收件人          │
│ - 邮编/邮票              │
│ - 类型: 书籍/食品...     │
├─────────────────────────┤
│                         │
│ 信件内容 (Body)          │  ← 实际要传达的内容
│                         │
│ "你好啊!最近怎么样?..."   │
│                         │
└─────────────────────────┘

Headers = 元信息（关于信本身）
Body    = 实际内容（你真正要传的东西）
```

\---

## 2.2 Headers（头部）

```
Headers = 键值对列表

格式:
   名字: 值
   ↓     ↓
 Header  内容

例:
Content-Type: application/json
Content-Length: 42
```

### 常见请求 Headers（浏览器→服务器）

|Header|含义|
|-|-|
|`User-Agent`|我是什么浏览器|
|`Accept`|我希望收到什么类型|
|`Accept-Language`|我希望什么语言|
|`Cookie`|我的登录状态|
|`Authorization`|我的认证 token|
|`Origin`|我的来源域名|

### 常见响应 Headers（服务器→浏览器）

|Header|含义|
|-|-|
|`Content-Type`|我返回的是什么类型|
|`Content-Length`|数据长度|
|`Set-Cookie`|让浏览器存的 cookie|
|`Cache-Control`|缓存策略|
|`Access-Control-Allow-Origin`|CORS 允许的来源 ⭐|

### Content-Type 常见值

```
text/html         → HTML 网页
application/json  → JSON 数据
image/png         → PNG 图片
image/jpeg        → JPG 图片
application/pdf   → PDF 文件
text/plain        → 纯文本
```

\---

## 2.3 Body（正文）

```
Body = 实际内容（数据本身）

可以是任何格式:
- HTML 网页代码
- JSON 数据
- 图片二进制数据
- 视频/PDF/任何文件
- 也可以是空（GET 请求通常没 Body）

服务器靠 Content-Type Header 告诉浏览器 Body 是什么格式
```

### 完整 HTTP 通信例子

#### 浏览器发送的请求

```
GET /counter HTTP/1.1                    ← 请求行
Host: xxx.execute-api.amazonaws.com      ← Header 开始
User-Agent: Mozilla/5.0
Accept: application/json
Origin: https://zhabc001.me
                                          ← 空行（标记 Body 开始）
                                          ← Body（GET 通常没 Body）
```

#### 服务器返回的响应

```
HTTP/1.1 200 OK                          ← 状态行
Content-Type: application/json            ← Header 开始
Access-Control-Allow-Origin: \*
Content-Length: 13
                                          ← 空行
{"count": 1}                              ← Body
```

\---

## 2.4 状态码

|范围|含义|
|-|-|
|2xx|成功|
|3xx|重定向|
|4xx|客户端错误|
|5xx|服务器错误|

### 常见状态码

|状态码|含义|你可能遇到的场景|
|-|-|-|
|`200 OK`|成功|正常访问|
|`301 Moved Permanently`|永久重定向|HTTP→HTTPS|
|`302 Found`|临时重定向|暂时跳转|
|`400 Bad Request`|请求格式错|API 参数错|
|`401 Unauthorized`|没登录|需要认证|
|`403 Forbidden`|没权限|S3 权限不对、CloudFront 配置问题|
|`404 Not Found`|资源不存在|URL 写错、文件没上传|
|`500 Internal Server Error`|服务器代码出 bug|Lambda 代码错误|
|`502 Bad Gateway`|网关错误|CloudFront 部署中|
|`503 Service Unavailable`|服务不可用|服务过载|

\---

## 2.5 CORS（跨域资源共享）

```
CORS = Cross-Origin Resource Sharing
日语: クロスオリジンリソース共有

为什么需要:
- 你的简历在 https://zhabc001.me
- API 在 https://xxx.execute-api.amazonaws.com
- 不同域名 → 浏览器的"同源策略"默认禁止 JS 跨域调用
- 解决: 服务器明确表示"我允许"

CORS 三剑客 Header:

Access-Control-Allow-Origin: \*
   "允许任何域名调用我"
   生产环境应该改成具体域名

Access-Control-Allow-Methods: GET, POST, OPTIONS
   "允许这些 HTTP 方法"
   OPTIONS = 浏览器预检请求（必须有）

Access-Control-Allow-Headers: Content-Type
   "允许客户端发送这些 Header"
```

### CORS 错误典型表现

```
Access to fetch at 'https://...' from origin 'https://...' 
has been blocked by CORS policy

原因排查:
1. Header 名字拼错（注意大小写）
2. 没有 OPTIONS 方法（预检失败）
3. API Gateway 自己的 CORS 配置覆盖了 Lambda 的
```

\---

# 第 3 章 JSON 数据格式

## 3.1 JSON 是什么

```
JSON = JavaScript Object Notation
读音: 杰森（不是字母拼读）
日语: ジェイソン
英语: JSON

本质: 一种数据交换格式
作用: 让不同系统/语言能传递数据

类比:
   你的 Lambda（Python）  →  JSON  →  浏览器（JavaScript）
                       ↑
              不同语言的"通用语"
```

\---

## 3.2 JSON 语法

### 语法只有 3 件事

#### 1\. 键值对

```json
{
    "name": "Zhang"
}
```

```
规则:
   "键": 值
    ↑     ↑
  字符串  任意类型
   双引号

✅ 键必须双引号:  "name"
❌ 不能单引号:   'name'
❌ 不能不加引号: name
```

#### 2\. 6 种值类型

```json
{
    "字符串": "Hello",          双引号包起来
    "数字": 42,                  直接写数字
    "布尔值": true,              true 或 false
    "空值": null,                null
    "数组": \[1, 2, 3],          用 \[]
    "对象": {"key": "value"}    用 {}
}
```

#### 3\. 嵌套（套娃）

```json
{
    "name": "Zhang",
    "age": 27,
    "skills": \["AWS", "Python", "日本語"],
    "address": {
        "country": "Japan",
        "city": "Chiba"
    }
}
```

**就这些**！整个 JSON 语法已经讲完。

\---

## 3.3 JSON vs Python dict

⚠️ 它们**长得很像**，但是**不一样的东西**！

```
Python dict:                JSON:
{                           {
    'key': 'value'              "key": "value"
    ↑                           ↑
   单引号也行                   必须双引号
}                           }
```

### 区别

```
JSON:
   是一种"格式" (Format)
   是一段"字符串" (String)
   '{"name": "Zhang"}'  ← 整体是个字符串
   ↑                ↑
  开始引号        结束引号

Python dict:
   是 Python 里的"数据结构"
   {"name": "Zhang"}  ← 没引号包起来
```

### 转换函数

```python
import json

# Python dict → JSON 字符串
my\_dict = {'count': 1}
my\_json = json.dumps(my\_dict)
print(my\_json)  # 输出: '{"count": 1}'   ← 字符串

# JSON 字符串 → Python dict
my\_str = '{"count": 1}'
my\_dict = json.loads(my\_str)
print(my\_dict)  # 输出: {'count': 1}    ← dict
```

```
记忆口诀:
json.dumps()  →  d-ump-s = "倒出来" = dict 倒成字符串
json.loads()  →  l-oad-s = "装进来" = 字符串装成 dict
```

\---

# 第 4 章 Python / Lambda 语法

## 4.1 Lambda 函数结构

### Lambda = 普通 Python + 一个特殊入口函数

```python
def lambda\_handler(event, context):
    # 你的代码
    return {...}
```

**就这么一个特殊点**，其他都是普通 Python。

### 拆解 `def lambda\_handler(event, context):`

```python
def lambda\_handler(event, context):
   ↑      ↑              ↑       ↑
   定义   函数名        参数 1  参数 2
```

```
def = define（定义）
   "我要定义一个函数"

lambda\_handler = 函数名（AWS 默认要求）
   可以改名字，但要在 Lambda 配置改 "Handler" 设置

event = AWS 传给你的"事件信息"
context = AWS 传给你的"运行环境信息"
   AWS 自动传给你，你不用主动传
```

### event 长什么样

API Gateway 触发时：

```python
event = {
    'httpMethod': 'GET',
    'path': '/',
    'headers': {...},
    'queryStringParameters': {...},
    'body': '...'
}
```

⚠️ 简单 Lambda（如访客计数器）不需要看 event。

### context 长什么样

```python
context.function\_name      # 'cloud-resume-counter'
context.aws\_request\_id     # 唯一请求 ID
context.get\_remaining\_time\_in\_millis()  # 剩余执行时间
```

⚠️ 简单 Lambda 也不用 context。

### Lambda 必须返回的格式

```python
return {
    'statusCode': 200,        # HTTP 状态码（必填）
    'headers': {...},         # HTTP 响应头
    'body': '字符串'           # HTTP 响应体（必须是字符串！）
}
```

⚠️ **常见错误**：

```python
# 错误 1: 直接返回 dict
return {'count': 1}
   → API Gateway 报错: 期望 statusCode

# 错误 2: body 是 dict
return {
    'statusCode': 200,
    'body': {'count': 1}   ← dict！
}
   → API Gateway 报错: body 必须是字符串

# 正确:
return {
    'statusCode': 200,
    'body': json.dumps({'count': 1})  ← 字符串
}
```

### 最简 Hello World Lambda

```python
def lambda\_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"message": "Hello World"}'
    }
```

\---

## 4.2 try / except 错误处理

```python
try:
    # 尝试做可能出错的事
    risky\_operation()
except SomeError:
    # 出错了，备用方案
    handle\_error()
```

```
try   = "我试试看做这件事"
except = "万一出错了，备用方案"

不用 try/except:
   出错 → 程序崩溃 → Lambda 返回 502

用 try/except:
   出错 → 走 except → 返回友好错误消息 → 程序继续
```

### 多层 except（捕获不同错误）

```python
try:
    table.update\_item(...)
except ClientError as e:
    # 处理 AWS 服务错误
    print(f"AWS error: {e}")
    return {'statusCode': 500, ...}
except Exception as e:
    # 处理其他所有错误（兜底）
    print(f"Unexpected error: {e}")
    return {'statusCode': 500, ...}
```

```
ClientError: AWS SDK 抛出的错误（表不存在、权限不足等）
Exception:   兜底，捕获所有未预料的错误

为什么要分两层:
✅ ClientError 能精确知道是 AWS 的问题，日志有用
✅ Exception 兜底，防止 Lambda 崩溃
```

\---

## 4.3 boto3 使用

```
boto3 = AWS 官方 Python SDK
作用: 让 Python 代码能调用 AWS 服务（DynamoDB、S3 等）
特点: Lambda 运行环境自带，不用单独安装
```

### resource vs client

```python
# 高级 API: resource（推荐新手）
dynamodb = boto3.resource('dynamodb', region\_name='ap-northeast-1')
table = dynamodb.Table('my-table')
table.update\_item(Key={...}, UpdateExpression=...)

# 底层 API: client
dynamodb = boto3.client('dynamodb', region\_name='ap-northeast-1')
dynamodb.update\_item(TableName='my-table', Key={...})
```

```
resource (推荐):
✅ 面向对象，更直观
✅ Key 直接用字典
✅ 适合简单操作

client:
✅ 功能完整
⚠️ 需要手动指定数据类型
⚠️ 略微复杂
```

### 关键性能优化：客户端初始化位置

```python
# ✅ 推荐：写在函数外（全局）
dynamodb = boto3.resource('dynamodb', region\_name='ap-northeast-1')
table = dynamodb.Table('cloud-resume-counter')

def lambda\_handler(event, context):
    table.update\_item(...)  ← 直接用全局变量

# ❌ 不推荐：写在函数里（每次调用都初始化）
def lambda\_handler(event, context):
    dynamodb = boto3.resource(...)
    table = dynamodb.Table(...)
    table.update\_item(...)
```

### 为什么写函数外更快

```
Lambda 执行模型:

第 1 次调用（冷启动 Cold Start）:
   - 启动新容器
   - 加载 Python 运行时
   - 执行 import + 函数外初始化代码 ⭐
   - 调用 lambda\_handler()
   总耗时: 500-2000ms

容器保留在内存里 ↓

第 2 次调用（暖启动 Warm Start）:
   - 复用现有容器
   - 函数外代码不再执行 ⭐
   - 直接调用 lambda\_handler()
   总耗时: 50-200ms
```

```
boto3.resource() 是重操作（建立 HTTPS 连接、加载证书）
- 写函数外: 暖启动 50ms
- 写函数里: 暖启动 300ms（多 250ms）
```

### DynamoDB 原子计数器（重要概念）

```python
table.update\_item(
    Key={'id': 'visitor\_count'},
    UpdateExpression='ADD #count :inc',
    ExpressionAttributeNames={'#count': 'count'},
    ExpressionAttributeValues={':inc': 1},
    ReturnValues='UPDATED\_NEW'
)
```

#### 参数详解

```python
Key={'id': 'visitor\_count'}
```

指定操作哪条记录（对应表的分区键）。

```python
UpdateExpression='ADD #count :inc'
```

意思: 给 count 字段加 :inc 这个值。

#### 占位符的原因

```python
ExpressionAttributeNames={'#count': 'count'}
ExpressionAttributeValues={':inc': 1}
```

```
占位符规则:
#count → 字段名占位（井号开头）
:inc   → 值占位（冒号开头）

为什么用占位符:
1. count 是 DynamoDB 保留字，直接写会报错
2. 防 SQL 注入（虽然 NoSQL 不太适用，但是好习惯）
3. 代码更清晰
```

#### 完整翻译

```python
'ADD #count :inc'
   ↓ 占位符替换
'ADD count 1'
   ↓ 含义
"给 count 字段 + 1"
```

#### 为什么是"原子"操作

```
非原子写法（错误）:
1. 读取: count = 5
2. 计算: new\_count = 5 + 1 = 6
3. 写入: count = 6

并发问题:
   用户 A 读到 count=5
   用户 B 读到 count=5
   用户 A 写入 count=6
   用户 B 写入 count=6  ← 应该是 7！
   
   结果: 丢失一次访问

原子写法（正确）:
   table.update\_item(UpdateExpression='ADD #count :inc')
   ↓
   DynamoDB 内部保证: 读+加+写 是不可分割的操作
   多并发请求自动排队 → 数据正确
```

### ReturnValues 参数

```python
ReturnValues='UPDATED\_NEW'

可选值:
   NONE          → 不返回任何东西（默认）
   UPDATED\_NEW   → 返回更新后的新值 ⭐ 我们用这个
   ALL\_NEW       → 返回整条记录的新值
   UPDATED\_OLD   → 返回更新前的旧值
   ALL\_OLD       → 返回整条记录的旧值
```

### Decimal 转换问题

```python
new\_count = int(response\['Attributes']\['count'])
```

```
DynamoDB 数字类型 → Python 里是 Decimal（高精度十进制）
JSON 不支持 Decimal → 序列化时会报错
所以要先转成 int

# 错误:
new\_count = response\['Attributes']\['count']  # 是 Decimal('1')
return json.dumps({'count': new\_count})       # TypeError!

# 正确:
new\_count = int(response\['Attributes']\['count'])  # 是 int(1)
return json.dumps({'count': new\_count})           # OK
```

\---

# 第 5 章 Git 基础

## 核心概念

```
Repository（仓库）= 项目的代码仓库
   - Local: 本地一份
   - Remote: GitHub 远程一份

Commit（提交）= 保存一次代码变更的快照

Push（推送）= 把本地 commit 上传到 GitHub

Pull（拉取）= 把 GitHub 的更新下载到本地

Branch（分支）= 用于并行开发，main 是主分支
```

## 基本工作流

```bash
# 改了代码后
git status                    # 查看哪些文件改了
git add .                     # 暂存所有改动
git commit -m "描述"           # 提交
git push origin main          # 推送到 GitHub
```

## Conventional Commits（约定式提交）

```
feat: 新功能（feature）
fix: 修复 bug
docs: 文档变更
style: 样式变更
refactor: 重构
test: 测试相关
chore: 杂项

例:
git commit -m "feat: 添加访客计数器"
git commit -m "fix: CORS 配置错误"
git commit -m "docs: 更新 README"
```

## SSH 密钥（免密 push）

```bash
# 生成密钥
ssh-keygen -t ed25519 -C "your\_email@example.com"

# 一路回车（不用密码）

# 查看公钥（要复制到 GitHub）
cat \~/.ssh/id\_ed25519.pub

# 测试连接
ssh -T git@github.com
```

\---

# 第 6 章 AWS 服务和创建逻辑

## 6.1 整体架构

```
本项目使用的 AWS 服务架构：

\[访客浏览器]
     ↓
\[Route 53 / Namecheap DNS]      ← 域名解析
     ↓
\[CloudFront]                     ← CDN + HTTPS + 缓存
     ↓
\[S3 静态文件]                    ← HTML/CSS/JS

JS 在浏览器里调用 ↓

\[API Gateway]                    ← HTTP API 入口
     ↓
\[Lambda]                         ← 业务逻辑
     ↓
\[DynamoDB]                       ← 访客数据存储

辅助服务:
\[ACM]      → 提供 SSL 证书给 CloudFront
\[IAM]      → 管理 Lambda 访问 DynamoDB 的权限
\[CloudWatch] → 监控 Lambda 日志和指标
```

\---

## 6.2 S3（对象存储）

### S3 是什么

```
S3 = Simple Storage Service
日语: シンプル・ストレージ・サービス
英语: Simple Storage Service

本质: AWS 的"网盘"，但比网盘强大
作用: 存储任何文件（HTML/图片/视频...）

本项目用途:
1. 存储简历 HTML/CSS/JS 文件
2. 静态网站托管（让 S3 直接对外提供 web 访问）
```

### 关键概念

```
桶 (Bucket): 存文件的容器，名字必须全球唯一
对象 (Object): 桶里的文件
键 (Key): 对象的路径名（如 "css/styles.css"）
```

### 创建逻辑

```
1. 选区域（必须 ap-northeast-1 东京）
2. 创建桶
   - 桶名规则: 小写字母/数字/连字符/点
   - 不能有大写、下划线、空格、中文
3. 关闭"阻止公共访问"（静态网站需要公开）
4. 上传文件
5. 启用静态网站托管
6. 配置桶策略（允许公开读取）
```

### 桶策略示例

```json
{
    "Version": "2012-10-17",
    "Statement": \[
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "\*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::桶名/\*"
        }
    ]
}
```

### S3 两种 endpoint 区别

```
S3 网站终端节点（Website Endpoint）:
   xxx.s3-website-region.amazonaws.com
   - HTTP only
   - 不能用 OAC
   - 适合临时测试

S3 REST API 终端节点:
   xxx.s3.region.amazonaws.com
   - HTTPS 支持
   - 可以用 OAC（最安全）
   - CloudFront 的源站推荐使用
```

\---

## 6.3 CloudFront（CDN）

### CloudFront 是什么

```
CloudFront = AWS 的 CDN（Content Delivery Network）
日语: コンテンツ配信ネットワーク
英语: Content Delivery Network

简单理解:
   S3 = 仓库（东京一个地方）
   CloudFront = 全球便利店网络（400+ 边缘节点）

效果:
   日本访问 → 东京边缘节点（10ms）
   美国访问 → 美国边缘节点（10ms）
   不需要绕回东京
```

### 为什么 SRE 都用 CloudFront

```
1. HTTPS 自动支持        ← 安全
2. 全球加速              ← 体验
3. DDoS 防护（基础版）   ← 安全
4. 缓存减少 S3 请求      ← 成本
5. 可集成 AWS WAF        ← 进一步安全
```

### 架构变化

```
没有 CloudFront:
\[用户] → http://xxx.s3-website-... → \[S3] (东京)

有 CloudFront:
\[用户] → https://xxxxx.cloudfront.net → \[CloudFront 边缘节点]
                                          ↓
                                     \[S3] (东京)
```

### 关键概念：OAC（Origin Access Control）

```
OAC = Origin Access Control（源访问控制）
日语: オリジンアクセスコントロール

作用: S3 桶关闭公开访问，只允许 CloudFront 来取数据

安全升级:
- 防止有人绕过 CloudFront 直接访问 S3
- 防止 S3 URL 被发现后被刷请求
- 是 SRE 的标准做法

OAI vs OAC:
OAI = Origin Access Identity（旧版）
OAC = Origin Access Control（新版，推荐）
```

### 创建逻辑

```
1. 选源（S3 REST API endpoint，不是 -website 那个）
2. 启用 OAC（自动更新 S3 桶策略）
3. 配置缓存行为
   - Viewer Protocol Policy: Redirect HTTP to HTTPS
   - Allowed HTTP Methods: GET, HEAD
   - Cache Policy: CachingOptimized
4. 价格类（北美+欧洲+亚洲）
5. 备用域名 + SSL 证书（如有自定义域名）
6. Default Root Object（重要！）
   - 填: index.html 或你的 HTML 文件名
   - 否则访问根 URL 会 403
7. WAF（免费方案包含，可启用）
8. 创建并等待部署（5-15 分钟）
```

### 价格类对比

|价格类|覆盖区域|价格|
|-|-|-|
|仅北美和欧洲|北美 + 欧洲|最便宜|
|北美+欧洲+亚洲等|+ 日本 + 东南亚|中等 ⭐|
|所有边缘节点|全世界|最贵|

```
对你的选择:
访问者主要在日本 → 必须包括亚洲
推荐: "北美、欧洲、亚洲、中东和非洲"
```

\---

## 6.4 ACM（SSL 证书）

### ACM 是什么

```
ACM = AWS Certificate Manager
日语: AWS Certificate Manager
作用: 申请和管理 SSL/TLS 证书

效果: HTTP → HTTPS（地址栏显示锁图标 🔒）
```

### 关键限制 ⭐

```
CloudFront 用的 ACM 证书必须在 us-east-1（北弗吉尼亚）创建！

原因: CloudFront 是全球服务，证书集中在弗吉尼亚
如果在 ap-northeast-1 创建 → CloudFront 找不到

这是新手最常踩的坑之一（也是面试题）
```

### 创建逻辑

```
1. 切换区域到 us-east-1
2. ACM → 请求证书 → 公有证书
3. 域名:
   - 主域名: zhabc001.me
   - 添加: www.zhabc001.me
4. 验证方法: DNS 验证（推荐）
5. ACM 给你 CNAME 验证记录
6. 在 DNS 商（Namecheap/Route 53）添加 CNAME
7. 等 5-30 分钟，状态变成"已颁发"
```

### DNS 验证 vs 邮件验证

```
DNS 验证（推荐）:
✅ 自动续期
✅ 长期有效
⚠️ 需要 DNS 配置权限

邮件验证:
✅ 简单
❌ 没有 admin@yourdomain.com 邮箱
❌ 不支持自动续期
```

\---

## 6.5 DynamoDB（NoSQL 数据库）

### DynamoDB 是什么

```
DynamoDB = AWS 的全托管 NoSQL 数据库
日语: フルマネージド NoSQL データベース
英语: Fully Managed NoSQL Database

特点:
✅ 无需管理服务器
✅ 自动扩展
✅ 毫秒级延迟
✅ 永久免费 25GB 存储

本项目用途: 存储访客计数（一条记录）
```

### 关键概念

```
表 (Table): 数据集合
项目 (Item): 表里的一条记录（类似 SQL 的 row）
属性 (Attribute): 项目里的字段（类似 SQL 的 column）

分区键 (Partition Key): 主键，每条记录必须有
排序键 (Sort Key): 可选，配合分区键组成复合主键
```

### 数据示例

```
表名: cloud-resume-counter
分区键: id (字符串)

记录:
   id="visitor\_count", count=42
```

### 创建逻辑

```
1. DynamoDB 控制台 → 创建表
2. 表名: cloud-resume-counter
3. 分区键: id（字符串类型）
4. 排序键: 不填
5. 表设置: 默认（按需付费）
6. 添加初始数据:
   id: visitor\_count
   count: 0（数字类型）
```

### NoSQL vs SQL

```
SQL（关系数据库）:
✅ 复杂查询（JOIN、子查询）
✅ 强一致性
⚠️ 需要先定义 schema
⚠️ 扩展困难

NoSQL（DynamoDB）:
✅ 灵活 schema
✅ 自动扩展
✅ 高性能（毫秒延迟）
⚠️ 不支持 JOIN
⚠️ 不擅长复杂查询
```

### 容量模式

```
按需付费 (On-demand) ⭐ 推荐:
- 用多少付多少
- 流量低 = 几乎免费
- 适合不可预测的流量

预置容量 (Provisioned):
- 提前买容量
- 适合稳定的高流量
- 不用也要付钱
```

\---

## 6.6 Lambda（Serverless 函数）

### Lambda 是什么

```
Lambda = AWS 的 Serverless 计算服务
日语: サーバーレス計算サービス
英语: Serverless Compute

特点:
✅ 不需要管理服务器
✅ 按调用次数付费
✅ 自动扩展
✅ 永久免费 100 万请求/月

本项目用途: 访客计数器后端逻辑（Python）
```

### Lambda 触发方式

```
触发器（Trigger）:
- API Gateway → HTTP 请求
- S3 → 文件上传
- DynamoDB Streams → 数据变化
- CloudWatch Events → 定时任务
- SNS / SQS → 消息队列

本项目: API Gateway 触发
```

### 创建逻辑

```
1. 创建 IAM 角色（Lambda 访问 DynamoDB 权限）
2. Lambda 控制台 → 创建函数
3. 函数名: cloud-resume-counter
4. 运行时: Python 3.12
5. 选择执行角色: 上面创建的角色
6. 写代码（处理函数）
7. Deploy（部署）
8. 配置触发器（API Gateway）
```

### 关键性能概念

```
冷启动 (Cold Start):
   - 第一次调用或长时间没调用
   - 启动新容器
   - 耗时: 500-2000ms
   - 优化: 函数外初始化客户端

暖启动 (Warm Start):
   - 容器已在内存
   - 直接执行
   - 耗时: 50-200ms

并发 (Concurrency):
   - Lambda 自动扩展
   - 多个请求同时来 = 多个容器同时跑
```

### 内存配置

```
内存范围: 128 MB - 10240 MB
默认: 128 MB

注意:
- 内存增加 → CPU 也按比例增加
- 计费按 GB-秒
- 简单函数 128 MB 够用
- 复杂处理可适当增加
```

\---

## 6.7 IAM（权限管理）

### IAM 是什么

```
IAM = Identity and Access Management
日语: アイデンティティとアクセス管理
英语: Identity and Access Management

作用: 管理"谁"能访问"什么"

核心概念:
- User: 真实的人/账号
- Role: 给 AWS 服务用的角色
- Policy: 权限策略（JSON 文档）
- Group: 用户组
```

### 为什么需要 IAM

```
默认情况下:
   Lambda 没有任何权限
   不能读 DynamoDB
   不能写 CloudWatch Logs

解决:
   给 Lambda 一个"角色"
   角色绑定相应的"策略"
   Lambda 用这个角色访问其他服务
```

### 本项目的 IAM 设计

```
IAM 角色: lambda-resume-counter-role

绑定策略:
1. AWSLambdaBasicExecutionRole
   - 写 CloudWatch Logs 权限

2. AmazonDynamoDBFullAccess
   - 读写 DynamoDB 权限
   ⚠️ 应急版用 FullAccess
   ⚠️ 生产环境应该用最小权限自定义策略
```

### 最小权限原则（Principle of Least Privilege）

```
SRE 视角的最佳实践:
❌ AmazonDynamoDBFullAccess（权限过大）
✅ 只允许操作特定表的特定操作

最小权限策略示例:
{
    "Version": "2012-10-17",
    "Statement": \[
        {
            "Effect": "Allow",
            "Action": \[
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:ap-northeast-1:\*:table/cloud-resume-counter"
        }
    ]
}
```

### 创建逻辑

```
1. IAM 控制台 → 角色 → 创建角色
2. 信任实体: AWS 服务
3. 使用案例: Lambda
4. 添加权限策略
5. 角色名 + 描述
6. 创建
```

\---

## 6.8 API Gateway

### API Gateway 是什么

```
API Gateway = AWS 的 API 管理服务
日语: API ゲートウェイ
英语: API Gateway

作用: 把 Lambda（或其他后端）暴露成 HTTP API
让浏览器/客户端可以通过 URL 调用
```

### 两种 API 类型

```
REST API:
- 功能完整
- 复杂配置
- 价格略贵
- 100 万请求 = $3.50

HTTP API ⭐ 推荐:
- 功能简化
- 配置简单
- 价格更便宜
- 100 万请求 = $1.00
- 大部分场景够用
```

### 创建逻辑

```
1. API Gateway 控制台 → 创建 API
2. 选 HTTP API
3. 添加集成: Lambda → 选你的 Lambda 函数
4. 配置路由（如 GET /counter）
5. 配置 CORS（关键！）
6. 部署
7. 拿到 API URL
```

### CORS 配置

```
两个地方都要配 CORS:
1. Lambda 返回的 headers（你写的代码）
2. API Gateway 的 CORS 配置

API Gateway CORS 设置:
- Access-Control-Allow-Origin: \*
- Access-Control-Allow-Methods: GET, OPTIONS
- Access-Control-Allow-Headers: Content-Type
```

\---

# 第 7 章 服务依赖关系

## 完整请求流程

```
访客打开 https://zhabc001.me 简历:

\[1] 浏览器
    ↓ DNS 查询
\[2] Namecheap DNS（zhabc001.me CNAME → CloudFront）
    ↓
\[3] CloudFront 边缘节点
    ↓ 检查缓存（命中则直接返回，跳到 \[6]）
    ↓ 未命中 → 用 OAC 签名访问源
\[4] S3（resume.zhangbeichuan）
    ↓ 返回 HTML/CSS/JS
\[5] CloudFront 缓存并返回
    ↓
\[6] 浏览器渲染网页

JS 执行 fetch('https://xxx.execute-api.amazonaws.com/counter'):

\[7] API Gateway
    ↓ 路由到 Lambda
\[8] Lambda（Python 函数）
    ↓ 用 IAM 角色 + boto3
\[9] DynamoDB
    ↓ ADD #count :inc 原子更新
\[10] 返回新 count
\[11] Lambda 返回 JSON 响应（含 CORS）
\[12] API Gateway 返回给浏览器
\[13] JS 把 count 显示到网页
```

\---

## 创建顺序

```
按依赖关系，正确的创建顺序：

阶段 A: 静态网站（前端）
1. S3 桶
2. 上传 HTML/CSS/JS
3. 启用静态网站托管

阶段 B: HTTPS + CDN
4. （在 us-east-1）申请 ACM 证书
5. 验证 DNS（在 Namecheap 加 CNAME）
6. 等证书颁发
7. 创建 CloudFront 分发
8. 关联 ACM 证书 + 自定义域名
9. 配置 OAC（自动更新 S3 桶策略）
10. 在 Namecheap 加 CNAME 指向 CloudFront

阶段 C: 后端
11. 创建 DynamoDB 表 + 初始数据
12. 创建 IAM 角色
13. 创建 Lambda 函数 + 写代码
14. 测试 Lambda

阶段 D: 前后端打通
15. 创建 API Gateway HTTP API
16. 关联 Lambda
17. 配置 CORS
18. 在 HTML 里加 JS 调用 API
19. 测试整个流程
```

\---

## 服务关系图

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Namecheap DNS                                  │
│  zhabc001.me ────CNAME───→ CloudFront            │
│                                                 │
└─────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────┐
│  CloudFront Distribution                        │
│  - SSL: ACM 证书（us-east-1）                    │
│  - Origin: S3 (REST API endpoint)              │
│  - OAC: 限制只允许 CloudFront 访问 S3            │
│  - Cache: CachingOptimized                     │
└─────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────┐
│  S3 Bucket: resume.zhangbeichuan                │
│  - 桶策略: 只允许 CloudFront                     │
│  - 文件: HTML/CSS/JS                            │
└─────────────────────────────────────────────────┘

JS 在浏览器里调用 ↓

┌─────────────────────────────────────────────────┐
│  API Gateway (HTTP API)                         │
│  - GET /counter                                 │
│  - CORS 配置                                    │
│  - 触发 Lambda                                  │
└─────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────┐
│  Lambda Function                                │
│  - Python 3.12 代码                             │
│  - 执行角色: IAM Role                           │
│    └── AWSLambdaBasicExecutionRole              │
│    └── AmazonDynamoDBFullAccess                 │
│  - boto3 客户端（函数外初始化）                  │
└─────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────┐
│  DynamoDB Table: cloud-resume-counter           │
│  - Partition key: id (string)                   │
│  - Item: {id: "visitor\_count", count: N}       │
│  - 按需计费（流量低 = 免费）                     │
└─────────────────────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────┐
│  CloudWatch Logs                                │
│  - Lambda 自动写入日志                          │
│  - 可设置保留期（推荐 7 天）                     │
└─────────────────────────────────────────────────┘
```

\---

## 区域选择总结

|服务|区域|原因|
|-|-|-|
|S3|ap-northeast-1（东京）|接近用户|
|DynamoDB|ap-northeast-1|和 Lambda 同区域|
|Lambda|ap-northeast-1|和 DynamoDB 同区域|
|API Gateway|ap-northeast-1|和 Lambda 同区域|
|**ACM 证书**|**us-east-1（弗吉尼亚）**|**CloudFront 全球服务的限制** ⭐|
|CloudFront|全球|不分区域|
|IAM|全球|不分区域|

\---

# 第 8 章 关键面试要点

## 8.1 架构设计相关

```
Q: なぜ S3 を選んだのですか？(为什么选 S3)
A: 静的なコンテンツの配信に最適化されており、
   サーバー管理が不要、自動でスケールし、
   従量課金で低コストだからです。

Q: なぜ CloudFront を使うのですか？(为什么用 CloudFront)
A: 主に 4 つの理由:
   1. HTTPS 対応（無料の SSL 証明書）
   2. グローバル CDN による低レイテンシ
   3. 基本的な DDoS 防護
   4. キャッシュによる S3 リクエスト数とコスト削減

Q: OAC を設定したのはなぜですか？(为什么设置 OAC)
A: S3 を public にすると、誰でも直接 S3 を叩けて
   CloudFront をバイパスできてしまいます。
   OAC を使うと、S3 はプライベートのまま、
   CloudFront のみがアクセスできる状態になり、
   セキュリティと統一エンドポイントを実現できます。
```

## 8.2 Lambda 性能相关

```
Q: なぜ boto3 クライアントを関数の外で初期化しているのですか？
A: Lambda は実行コンテキストを再利用します。
   関数外の初期化はコールドスタート時のみ実行され、
   ウォームスタート時はスキップされるため、
   レスポンス時間を 5-10 倍速くできます。

Q: コールドスタート対策は？
A: 主な対策:
   1. クライアントの関数外初期化
   2. 軽量なランタイム（Python 3.12）
   3. 必要に応じて Provisioned Concurrency
   4. 依存ライブラリの最小化
```

## 8.3 DynamoDB 相关

```
Q: なぜ ADD operation を使ったのですか？
A: ADD は atomic counter として動作します。
   read → modify → write の 3 段階だと、
   並行アクセス時に race condition が発生し、
   カウントが正確に増えない可能性があります。
   ADD を使えば、DynamoDB が内部で原子的に処理するので、
   並行性の問題を回避できます。

Q: なぜ DynamoDB を選んだのですか？(为什么选 DynamoDB)
A: 主な理由:
   1. Lambda との親和性が高い
   2. サーバーレスで管理不要
   3. 25 GB ストレージが永続無料
   4. 訪問者カウンターのようなシンプルなキーバリューアクセスには最適
   
   RDS（MySQL/PostgreSQL）も検討しましたが、
   このユースケースではオーバースペックです。
```

## 8.4 セキュリティ相关

```
Q: 最小権限の原則は守っていますか？
A: 現状は AmazonDynamoDBFullAccess を使っていますが、
   本番環境では特定のテーブルの特定操作のみを
   許可するカスタム IAM ポリシーに変更する予定です。
   これは"必要な権限のみを付与する"という
   セキュリティのベストプラクティスです。

Q: CORS の設定で気をつけたことは？
A: 開発時は Access-Control-Allow-Origin を '\*' にしましたが、
   本番では特定のドメイン（zhabc001.me）に絞ることで、
   不正なドメインからの API 呼び出しを防げます。
```

## 8.5 観測性（Observability）相关

```
Q: ログとモニタリングはどうしていますか？
A: CloudWatch Logs に Lambda の標準出力（print）が
   自動で送られます。今回はシンプルな print ですが、
   本番では logging モジュールで構造化ログを出力し、
   CloudWatch Logs Insights で分析できるようにします。
   また、CloudWatch Alarms で エラー率や Latency を
   監視する予定です。

Q: SRE の観点で何を意識しましたか？
A: 主に 4 つ:
   1. 可観測性: CloudWatch Logs/Metrics
   2. コスト最適化: Always Free Tier の活用、
      Price Class の調整
   3. セキュリティ: OAC、IAM、CORS
   4. ドキュメンテーション: README + DEVLOG で
      意思決定と学びを記録
```

## 8.6 コスト相关

```
Q: コスト最適化のために何をしましたか？
A: 複数の工夫をしています:
   1. AWS Always Free Tier を最大限活用
      - Lambda: 100 万リクエスト/月（永続無料）
      - DynamoDB: 25 GB ストレージ（永続無料）
      - CloudFront: 1 TB 流量/月（永続無料）
   2. CloudFront Price Class を絞る
      （北米+欧州+アジアのみ、不要な地域は除外）
   3. Budget Alert を $1 で設定
      （想定外のコスト増加を即検知）
   4. CloudWatch Logs Retention を 7 日に設定
      （ログの長期保存コストを抑制）
   
   結果、月額 0 円で運用できています。
```

\---

## 8.7 用日语自然介绍项目（1 分钟版）

```
このプロジェクトは Cloud Resume Challenge という、
AWS 上に履歴書サイトを構築する課題です。
SRE の観点から、可観測性とコスト最適化を意識した設計を心がけました。

フロントエンドは S3 で静的ホスティングし、
CloudFront で HTTPS 化と全世界配信を実現しています。
Origin Access Control（OAC）を使い、S3 は CloudFront 経由のみアクセス可能にしました。

バックエンドは Lambda + DynamoDB で訪問者カウンター機能を実装し、
DynamoDB の atomic counter で並行アクセスにも正確に動作します。

技術スタックは AWS、Python、JavaScript、HTML/CSS で、
全リソースに Standard Tag を付け、コスト追跡も可能にしています。
```

\---

# 附录: 重要术语对照表

|中文|日语|英语|
|-|-|-|
|云|クラウド|Cloud|
|静态网站|静的ウェブサイト|Static Website|
|内容分发网络|コンテンツ配信ネットワーク|CDN|
|边缘节点|エッジロケーション|Edge Location|
|跨域资源共享|クロスオリジンリソース共有|CORS|
|无服务器|サーバーレス|Serverless|
|函数计算|関数計算|Function as a Service|
|原子操作|アトミック操作|Atomic Operation|
|冷启动|コールドスタート|Cold Start|
|暖启动|ウォームスタート|Warm Start|
|并发|並行性|Concurrency|
|竞态条件|競合状態|Race Condition|
|可观测性|可観測性|Observability|
|最小权限原则|最小権限の原則|Principle of Least Privilege|
|基础设施即代码|Infrastructure as Code|IaC|
|持续集成/部署|CI/CD|Continuous Integration/Deployment|
|证书|証明書|Certificate|
|域名解析|ドメイン名解決|DNS Resolution|
|重定向|リダイレクト|Redirect|
|缓存|キャッシュ|Cache|
|状态码|ステータスコード|Status Code|
|请求|リクエスト|Request|
|响应|レスポンス|Response|
|头部|ヘッダー|Header|
|正文|ボディ|Body|
|路由|ルート|Route|
|触发器|トリガー|Trigger|

\---

**文档结束**

> 持续更新中。完成完整版后会补充 Terraform、CI/CD、监控等内容。

