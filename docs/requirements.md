# 情侣私密博客 - 需求文档

> 一个只属于两个人的私密空间，集聊天、朋友圈、生活记录、共同计划于一体。

---

## [S1] 项目概述

### 1.1 项目名称
**我们的小窝**（OurNest）

### 1.2 目标用户
仅限两个人使用，完全私密，不对外开放。

### 1.3 核心价值
- 一个安全、私密的两人空间
- 可以随时聊天、分享生活点滴
- 记录每天的日常：吃了啥、干了啥
- 写悄悄话，制造小浪漫
- 一起规划未来：想去的地方、想看的剧
- 记录共同的回忆，支持图文帖子
- 简洁温馨的界面设计

---

## [S2] 参考项目

| 项目 | 技术栈 | 亮点功能 | 参考价值 |
|------|--------|---------|---------|
| [PoopHub (拉无忧)](https://github.com/Temp1258/PoopHub) | React Native + Node.js + SQLite | 50+ 表情推送、每日仪式、信箱、便利贴墙、纪念日管理 | 功能最全面的情侣 App，架构设计参考 |
| [nous-deux](https://github.com/martinbouvet2000-tech/nous-deux) | React + TypeScript + Supabase | 倒计时、心情追踪、感恩墙、回忆录、活动计划 | Web 端情侣 dashboard，UI 设计参考 |
| [timeless-love-anniversary-app](https://github.com/jmcmomic/timeless-love-anniversary-app) | React + Tailwind CSS | 照片画廊、时间线、背景音乐、惊喜元素 | 纪念日/时间线展示参考 |
| [Love-Connect](https://github.com/amarhumayunx/Love-Connect) | Flutter + Firebase | 约会计划、回忆分享、通知推送 | 移动端交互参考 |

---

## [S3] 功能需求

### 3.1 用户认证模块

**简单双人登录系统：**
- 两个固定账号（如：用户A / 用户B），各自设置密码
- 不需要注册流程，账号在部署时预设
- Django 内置认证系统 + 自定义 User 模型
- 登录后显示对方的昵称和头像
- 支持"记住我"功能（session 持久化）

### 3.2 实时聊天模块

**WebSocket 即时通讯：**
- 使用 Django Channels + WebSocket 实现实时消息
- 消息类型：
  - 纯文本消息
  - 图片消息（支持发送图片）
  - 表情消息（预设 emoji 快捷面板）
  - 系统消息（如"对方正在输入..."）
- 消息状态：已发送、已读
- 聊天记录持久化存储，支持历史消息加载
- 消息按日期分组显示
- 支持"对方正在输入"提示

### 3.3 朋友圈模块

**图文动态发布与互动：**
- **发布帖子：**
  - 支持文字 + 多张图片（最多 9 张）
  - 图片支持拖拽排序
  - 可选择心情标签（开心、难过、想念、感恩等）
  - 支持定位（可选）
- **浏览动态：**
  - 时间线瀑布流展示
  - 图片点击放大查看
  - 无限滚动加载
- **互动功能：**
  - 点赞（❤️）
  - 评论（支持图片评论）
  - 评论回复（一级回复）
- **管理功能：**
  - 编辑自己的帖子
  - 删除自己的帖子/评论
  - 按日期筛选

### 3.4 存储桶模块

**帖子与文件管理：**
- 独立的"存储桶"页面，以卡片/网格形式展示所有帖子
- 支持搜索（按文字内容搜索）
- 支持按心情标签筛选
- 支持按日期范围筛选
- 图片批量上传（支持拖拽）
- 图片存储优化（自动生成缩略图）
- 支持下载图片原图

### 3.5 个人中心

- 修改个人昵称、头像
- 查看自己的发布统计
- 修改密码

### 3.6 生活记录模块

**记录每天的日常：**

#### 3.6.1 今天吃了啥（美食日记）
- 记录每天吃了什么（早餐/午餐/晚餐/加餐）
- 支持拍照 + 文字描述
- 可选择餐厅/地点
- 按日历视图查看历史记录
- 两人各自的记录用不同颜色区分
- 支持给对方的美食点赞 ❤️

#### 3.6.2 今天干了啥（每日日记）
- 简短记录今天做了什么（类似朋友圈但更日常、更简短）
- 支持文字 + 图片
- 自动生成时间戳
- 按日期倒序浏览
- 可添加心情 emoji
- 支持按日期搜索回顾

#### 3.6.3 悄悄话
- 两人之间的私密留言空间
- 可以写想说但不好意思当面说的话
- 支持匿名发送（不显示是谁写的，但可以猜）
- 支持定时显示（写完设定对方什么时候能看到）
- 悄悄话墙：以卡片形式展示，带浪漫背景
- 支持文字 + 小图片

### 3.7 共同计划模块

**一起规划未来：**

#### 3.7.1 一起去的地方（旅行心愿单）
- 添加想去的地方（城市/景点/餐厅）
- 每个地点支持：名称、描述、图片、想去程度（⭐1-5）
- 标记"已去过"并上传打卡照片
- 地图视图展示所有想去的地方（可选，使用 Leaflet.js）
- 两人可以各自添加，互相看到
- 按想去程度排序

#### 3.7.2 想看的剧和电影（观影清单）
- 添加想看的电影/电视剧/综艺
- 每部支持：名称、类型、海报图片、简介、谁想看的
- 状态管理：想看 → 在看 → 看完
- 看完后可以打分（⭐1-5）+ 简短评价
- 支持按类型筛选（电影/电视剧/综艺/动漫）
- 支持按状态筛选
- 两人各自的标记用不同颜色区分

---

## [S4] 技术架构

### 4.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| 后端框架 | Django 5.x + Django REST Framework | Python 全栈框架，自带 ORM、Admin、认证 |
| 实时通信 | Django Channels + WebSocket | Django 官方 WebSocket 支持 |
| 数据库 | PostgreSQL | 生产环境推荐，支持 JSON 字段 |
| 本地开发 | SQLite | 开发阶段使用，零配置 |
| 前端 | Django Templates + HTMX + Alpine.js | 轻量级前端，无需构建工具 |
| CSS 框架 | Tailwind CSS (CDN) | 实用优先，快速开发 |
| 图片处理 | Pillow | Python 图片处理库，生成缩略图 |
| 文件存储 | 本地存储 / 可选 S3 | 开发用本地，生产可迁移到 S3 |
| WebSocket 层 | Redis (Channels layer) | Django Channels 的消息通道后端 |

### 4.2 为什么选择 Django Templates + HTMX 而不是前后端分离？

对于两个人使用的私密博客：
- **开发更快**：不需要单独的前端构建流程
- **部署更简单**：一个 Django 项目搞定一切
- **HTMX 让页面交互流畅**：无需完整页面刷新，局部更新即可
- **维护成本低**：一套代码，Python 全栈

### 4.3 项目结构

```
personal_blog/
├── manage.py
├── requirements.txt
├── config/                 # Django 项目配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py            # ASGI 配置（WebSocket 需要）
│   └── wsgi.py
├── apps/
│   ├── accounts/           # 用户认证
│   │   ├── models.py       # 自定义 User 模型
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   ├── chat/               # 实时聊天
│   │   ├── models.py       # Message 模型
│   │   ├── consumers.py    # WebSocket 消费者
│   │   ├── routing.py      # WebSocket 路由
│   │   ├── views.py
│   │   └── urls.py
│   ├── moments/            # 朋友圈
│   │   ├── models.py       # Post, Comment, Like 模型
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   ├── daily/              # 生活记录
│   │   ├── models.py       # FoodLog, DailyLog, Whisper 模型
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   ├── plans/              # 共同计划
│   │   ├── models.py       # Place, Movie 模型
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   └── storage/            # 存储桶
│       ├── models.py       # 继承 moments 的模型或独立
│       ├── views.py
│       └── urls.py
├── templates/              # Django 模板
│   ├── base.html
│   ├── accounts/
│   ├── chat/
│   ├── moments/
│   ├── daily/
│   ├── plans/
│   └── storage/
├── static/                 # 静态文件
│   ├── css/
│   ├── js/
│   └── images/
└── media/                  # 用户上传文件
    ├── avatars/
    ├── posts/
    ├── chat/
    ├── food/               # 美食照片
    ├── daily/              # 日记照片
    └── travel/             # 旅行/打卡照片
```

### 4.4 数据库设计

#### User（扩展 Django User）
```python
class User(AbstractUser):
    nickname = CharField(max_length=50)     # 昵称
    avatar = ImageField(upload_to='avatars/') # 头像
    bio = TextField(max_length=200, blank=True) # 个性签名
```

#### Message（聊天消息）
```python
class Message:
    sender = ForeignKey(User)
    content = TextField                      # 文本内容
    message_type = CharField                 # text/image/emoji/system
    image = ImageField(upload_to='chat/')    # 图片消息
    emoji = CharField                        # emoji 字符
    is_read = BooleanField(default=False)    # 已读状态
    created_at = DateTimeField(auto_now_add=True)
```

#### Post（朋友圈帖子）
```python
class Post:
    author = ForeignKey(User)
    content = TextField                      # 文字内容
    mood = CharField                         # 心情标签
    location = CharField(blank=True)         # 定位（可选）
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### PostImage（帖子图片）
```python
class PostImage:
    post = ForeignKey(Post, related_name='images')
    image = ImageField(upload_to='posts/')
    thumbnail = ImageField(upload_to='posts/thumbs/')
    order = IntegerField(default=0)          # 排序
```

#### Comment（评论）
```python
class Comment:
    post = ForeignKey(Post, related_name='comments')
    author = ForeignKey(User)
    content = TextField
    image = ImageField(upload_to='comments/', blank=True)
    parent = ForeignKey('self', null=True)   # 回复哪条评论
    created_at = DateTimeField(auto_now_add=True)
```

#### Like（点赞）
```python
class Like:
    post = ForeignKey(Post, related_name='likes')
    user = ForeignKey(User)
    created_at = DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['post', 'user']   # 一篇帖子只能赞一次
```

#### FoodLog（美食日记）
```python
class FoodLog:
    author = ForeignKey(User)
    meal_type = CharField                     # breakfast/lunch/dinner/snack
    title = CharField(max_length=100)         # 如"红烧肉"
    description = TextField(blank=True)       # 描述
    image = ImageField(upload_to='food/')     # 美食照片
    location = CharField(blank=True)          # 餐厅/地点
    date = DateField()                        # 日期
    created_at = DateTimeField(auto_now_add=True)
```

#### DailyLog（每日日记）
```python
class DailyLog:
    author = ForeignKey(User)
    content = TextField                       # 今天干了啥
    mood = CharField                          # 心情 emoji
    image = ImageField(upload_to='daily/', blank=True)
    date = DateField()                        # 日期
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

#### Whisper（悄悄话）
```python
class Whisper:
    author = ForeignKey(User)
    content = TextField                       # 悄悄话内容
    image = ImageField(upload_to='whispers/', blank=True)
    is_anonymous = BooleanField(default=False) # 匿名发送
    visible_at = DateTimeField(null=True)     # 定时显示（null=立即）
    is_read = BooleanField(default=False)     # 对方是否已读
    created_at = DateTimeField(auto_now_add=True)
```

#### Place（一起去的地方）
```python
class Place:
    added_by = ForeignKey(User)
    name = CharField(max_length=100)          # 地点名称
    description = TextField(blank=True)       # 描述
    image = ImageField(upload_to='travel/', blank=True)
    rating = IntegerField(default=3)          # 想去程度 1-5
    location = CharField(blank=True)          # 城市/区域
    is_visited = BooleanField(default=False)  # 是否去过
    visited_photo = ImageField(upload_to='travel/visited/', blank=True)
    visited_date = DateField(null=True)       # 打卡日期
    created_at = DateTimeField(auto_now_add=True)
```

#### Movie（想看的剧和电影）
```python
class Movie:
    added_by = ForeignKey(User)
    title = CharField(max_length=200)         # 片名
    movie_type = CharField                    # movie/tv/variety/anime
    poster = ImageField(upload_to='posters/', blank=True)
    description = TextField(blank=True)       # 简介
    status = CharField(default='want')        # want/watching/done
    rating = IntegerField(null=True)          # 看完后打分 1-5
    review = TextField(blank=True)            # 简短评价
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

---

## [S5] 页面设计

### 5.1 导航结构

```
顶部导航栏：
├── 🏠 首页（朋友圈时间线）
├── 💬 聊天
├── 🍽️ 生活记录（今天吃了啥 / 今天干了啥 / 悄悄话）
├── 🎯 共同计划（一起去的地方 / 想看的剧）
├── 📦 存储桶
└── 👤 个人中心
```

### 5.2 页面清单

| 页面 | 路由 | 功能 |
|------|------|------|
| 登录页 | `/login/` | 简洁登录表单 |
| 朋友圈首页 | `/` | 动态时间线 + 发帖入口 |
| 聊天页 | `/chat/` | 实时聊天界面 |
| 美食日记 | `/daily/food/` | 今天吃了啥，按日历/列表查看 |
| 每日日记 | `/daily/journal/` | 今天干了啥，时间线展示 |
| 悄悄话 | `/daily/whisper/` | 悄悄话墙 + 写悄悄话 |
| 旅行心愿单 | `/plans/places/` | 想去的地方列表 + 地图视图 |
| 观影清单 | `/plans/movies/` | 想看的剧和电影，按状态筛选 |
| 存储桶 | `/storage/` | 所有帖子网格/卡片视图 |
| 帖子详情 | `/post/<id>/` | 单篇帖子详情 + 评论 |
| 个人中心 | `/profile/` | 个人信息编辑 |
| 发帖页 | `/post/new/` | 发布新帖子 |

### 5.3 UI 风格

- **色调**：温暖柔和（粉色/米色/浅紫渐变）
- **字体**：圆润可爱的中文字体
- **图标**：Emoji 风格，活泼可爱
- **动画**：轻微的过渡动画，点赞心跳效果
- **响应式**：移动端优先，PC 端自适应

---

## [S6] 非功能需求

### 6.1 安全性
- HTTPS 强制（生产环境）
- CSRF 保护（Django 内置）
- XSS 防护（Django 模板自动转义）
- 登录失败限流（防暴力破解）
- 图片上传类型验证（仅允许 jpg/png/gif/webp）
- 图片大小限制（单张最大 10MB）

### 6.2 性能
- 图片自动生成缩略图（列表页使用缩略图）
- 聊天消息分页加载（每次加载 50 条）
- 朋友圈无限滚动（每次加载 20 条）
- 数据库查询优化（select_related / prefetch_related）

### 6.3 部署
- **推荐平台**：Railway / Render / Fly.io（对 Django + WebSocket 友好）
- **数据库**：平台内置 PostgreSQL 或 Supabase
- **Redis**：平台内置 Redis 或 Upstash
- **媒体文件**：S3 / Cloudflare R2 / 本地挂载卷
- **环境变量**：SECRET_KEY、DATABASE_URL、REDIS_URL 等通过环境变量配置

---

## [S7] 开发计划（建议分期）

### Phase 1 - 基础框架（MVP）
- [x] Django 项目初始化
- [ ] 用户认证（登录/登出）
- [ ] 基础页面布局和导航
- [ ] 朋友圈：发帖（纯文字）+ 时间线浏览
- [ ] 数据库模型设计

### Phase 2 - 图片支持
- [ ] 朋友圈：图片上传 + 多图展示
- [ ] 图片缩略图自动生成
- [ ] 存储桶页面：网格展示所有帖子
- [ ] 帖子详情页

### Phase 3 - 互动功能
- [ ] 点赞功能
- [ ] 评论功能
- [ ] 心情标签
- [ ] 搜索和筛选

### Phase 4 - 生活记录
- [ ] 今天吃了啥（美食日记，按日历查看）
- [ ] 今天干了啥（每日日记，时间线）
- [ ] 悄悄话（私密留言 + 定时显示）

### Phase 5 - 共同计划
- [ ] 一起去的地方（旅行心愿单 + 地图）
- [ ] 想看的剧和电影（观影清单 + 状态管理）

### Phase 6 - 实时聊天
- [ ] Django Channels 配置
- [ ] WebSocket 聊天消费者
- [ ] 聊天界面（消息气泡、时间分组）
- [ ] 图片消息
- [ ] "正在输入"提示
- [ ] 消息已读状态

### Phase 7 - 打磨与部署
- [ ] UI 细节优化和动画
- [ ] 个人中心完善
- [ ] 移动端适配优化
- [ ] 部署到生产环境
- [ ] 数据备份方案

---

## [S8] 开发环境

### 8.1 依赖

```
# requirements.txt
Django>=5.0
djangorestframework>=3.15
channels>=4.0
channels-redis>=4.2
Pillow>=10.0
django-htmx>=1.17
whitenoise>=6.5        # 静态文件服务
python-dotenv>=1.0     # 环境变量管理
```

### 8.2 本地启动

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py migrate

# 4. 创建超级用户（两个账号）
python manage.py createsuperuser

# 5. 启动开发服务器
python manage.py runserver

# 6. 启动 WebSocket（需要 Redis）
# 本地开发可以用 InMemoryChannelLayer（不需要 Redis）
```

---

## [S9] 待确认事项

> 以下是你可能需要补充或修改的内容，请根据实际情况调整：

1. **两个账号的昵称**：你们想叫什么？（如：宝宝/贝贝，或自定义）
2. **心情标签列表**：默认提供哪些心情选项？
3. **是否需要通知功能**：对方发消息/评论时是否需要浏览器通知？
4. **是否需要纪念日功能**：类似 PoopHub 的纪念日倒计时？
5. **是否需要数据导出**：支持导出所有帖子和聊天记录？
6. **配色偏好**：粉色系？紫色系？其他？
7. **部署平台偏好**：Railway / Render / Fly.io / 其他？

---

## [S10] 附录：功能对比表

| 功能 | PoopHub | nous-deux | 本项目 |
|------|---------|-----------|--------|
| 实时聊天 | ✅ | ❌ | ✅ |
| 朋友圈/动态 | ❌ | ❌ | ✅ |
| 图文帖子 | ❌ | ✅ | ✅ |
| 评论互动 | ❌ | ❌ | ✅ |
| 点赞 | ❌ | ❌ | ✅ |
| 文件存储桶 | ❌ | ❌ | ✅ |
| 今天吃了啥 | ❌ | ❌ | ✅ |
| 今天干了啥 | ❌ | ❌ | ✅ |
| 悄悄话 | ❌ | ❌ | ✅ |
| 旅行心愿单 | ✅ | ✅ | ✅ |
| 观影清单 | ❌ | ❌ | ✅ |
| 纪念日 | ✅ | ❌ | 待定 |
| 每日仪式 | ✅ | ✅ | 待定 |
| 情绪追踪 | ❌ | ✅ | 待定 |
| 移动端 App | ✅ (iOS) | ❌ | ❌ (Web) |
| 实时同步 | ✅ | ✅ | ✅ |
