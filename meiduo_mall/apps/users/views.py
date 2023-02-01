import json
import re

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
         响应码  0 成功   400 失败
         
路由:    POST    register/

步骤:    1.接收请求(POST_JSON)
        2.获取数据
        3.验证数据
        4.数据入库
        5.返回响应
"""
class RegisterView(View):
    def post(self, request):
        # 1.接收请求(POST_JSON)
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # 2.获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        # 3.验证数据
        # 3.1 五个数据不为空
        # all([])里的元素, 如果有None或False, 就会返回False
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code':'400', 'errmsg':'参数不全'})
        # 3.2 用户名是否满足规则且不重复
        if not re.match('[a-zA-z0-9_-]{5,20}',username):
            return JsonResponse({'code':'400', 'errmsg':'用户名不满足规则'})
        count = User.objects.filter(username=username).count()
        if count != 0:
            return JsonResponse({'code':'400', 'errmsg':'用户名重复'})
        # 3.2 密码满足规则
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '密码格式有误!'})
        # 3.3 判断两次密码是否一致
        if password != password2:
            return JsonResponse({'code':400, 'errmsg':'密码与确认密码不一致'})
        # 3.4 判断手机号是否合法且不重复
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号码格式有误!'})
        count = User.objects.filter(phone_num=mobile).count()
        if count != 0:
            return JsonResponse({'code':400, 'errmsg': '手机号码重复'})
        # 3.5判断是否勾选用户协议
        if not allow:
            return JsonResponse({'code': 400, 'errmsg': '请勾选同意协议'})
        # 4.数据入库
        User.objects.create(
            username = username,
            password = password,
            phone_num = mobile,
        )
        # 5.返回响应
        return JsonResponse({'code':0, 'errmsg':'ok'})