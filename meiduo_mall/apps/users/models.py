from django.db import models

# Create your models here.

"""
设置用户, 需求是满足获得并保存用户名, 密码, 手机号 现有两种方案

1. 自己定义用户类, 获取信息, 并且将密码加密, 登录时有验证
class User(models.Model):
    user_name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11, unique=True)
    模拟密码加密 登录验证 ....
"""
# 2. django自带用户模型, 有密码加密和密码验证 继承重写
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    # 添加一个phone_num 字段
    phone_num = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name