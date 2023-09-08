from app.settings import *

DEBUG = False

# TODO: 修改数据库连接的密码和 IP 地址
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "thss",
        "USER": "root",
        "PASSWORD": "huangshuwei",
        "HOST": "db",
        "PORT": "3306",
    }
}
