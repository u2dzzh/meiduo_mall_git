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
