# Memory Story Life

基于 Django 的个人博客系统，支持多用户博客站点、文章管理、评论互动。

## 技术栈

- Django 4.2 + MySQL + Redis
- Python 3.12

## 功能模块

- 用户注册/登录/退出
- 个人站点（每个用户拥有独立博客）
- 文章管理（发布、编辑、删除）
- 分类与标签
- 评论（支持嵌套回复）
- 点赞/点踩
- 个人资料修改（头像、用户名、密码）
- 后台管理面板（标签、分类、文章、评论 CRUD）

## 数据模型

| 模型 | 说明 |
|------|------|
| Person | 自定义用户（继承 AbstractUser），含头像、电话、关联博客 |
| Blog | 博客站点（标题、主题样式） |
| Articles | 文章（标题、内容、点赞/踩/评论计数） |
| Categories | 文章分类 |
| Tags | 文章标签（多对多） |
| Comments | 评论（支持自关联嵌套回复） |
| UpOrDowns | 点赞/点踩记录 |

## 环境要求

- Python 3.10+
- MySQL 8.0+
- Redis 6.0+

## 快速开始

```bash
# 1. 创建数据库
mysql -u root -p -e "CREATE DATABASE practise DEFAULT CHARACTER SET utf8mb4;"

# 2. 安装依赖
pip install django mysqlclient django-redis Pillow

# 3. 数据库迁移
python manage.py migrate

# 4. 创建管理员
python manage.py createsuperuser

# 5. 启动服务
python manage.py runserver
```

## 配置说明

数据库和 Redis 连接在 `practise/settings.py` 中配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'practise',
        'USER': 'root',
        'PASSWORD': '150030',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
    }
}
```

部署时请根据实际环境修改。

## 项目结构

```
practise/
├── app01/              # 主应用（用户、博客、文章、评论）
│   ├── models.py       # 数据模型
│   ├── views.py        # 视图逻辑
│   ├── urls.py         # 路由配置
│   ├── forms/          # 表单验证
│   └── migrations/     # 数据库迁移
├── app02/              # 辅助应用
├── practise/           # 项目配置
│   ├── settings.py
│   └── urls.py
├── templates/          # HTML 模板
├── static/             # 静态资源（CSS/JS/图片）
├── media/              # 用户上传文件
└── manage.py
```

## License

Private
