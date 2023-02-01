
from django.urls import converters

class UsernameConverter:
    # 定义匹配用户名的正则表达式
    regex = '[a-z/0-9]{5,20}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)