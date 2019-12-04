from django.contrib.auth.backends import ModelBackend
import re
from users.models import User

class UserUtils(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        #1.判断username是手机号还是用户名
        try:
            if re.match(r"1[3-9]\d{9}",username):
                #匹配到username接收到的是手机号数据
                user=User.objects.get(mobile=username)
            else:
                #匹配到的username是用户名数据
                user=User.objects.get(username=username)
        except:
            user=None
        #2.查询对象则校验密码是否正确
        if user is not None and user.check_password(password):
            return user