from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.users.models import User

# Create your views here.

"""
判断用户名是否重复
    请求:  接收用户名
    业务逻辑: 
        根据用户名查询数据库  如果查询的数量为0, 说明该用户名没有注册
        如果查询的数量为1 , 说明该用户名已经注册
    响应      JSON文件
            {code:0, count:1/0, errmsg: ok}
    路由 GET  usernames/username/count
    步骤:
        1. 接收用户名
        2. 根据用户名查询数据库
        3. 返回响应
"""
class UsernameCountView(View):
    def get(self, request, username):
        # 接收username
        # 查询数据库
        count = User.objects.filter(username=username).count()
        # 返回响应
        return JsonResponse({
            'code': 0,
            'count': count,
            'errmsg': 'ok',
        })

"""
用户注册业务逻辑实现    
前端:     当用户输入 用户名, 密码, 确认密码, 手机号, 是否同意协议之后, 会点击注册按钮
        前端会发送Axios请求

后端:     请求:     接收请求(JSON), 获取数据
         业务逻辑:  验证数据, 数据入库
         响应:      JSON{'code':9, 'errmsg':'ok'
         
路由:    POST    register/

步骤:    1.接收请求(POST_JSON)
        2.获取数据
        3.验证数据
        4.数据入库
        5.返回响应
"""