import json

from django.shortcuts import render,redirect
from django.views import View
from django.conf import settings
from django.http import JsonResponse
# Create your views here.
from sinaoauth.OAuth import OAuthWeibo
from sinaoauth.models import OAuthSinaUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJS
from django.contrib.auth import login
from django_redis import get_redis_connection
from users.models import User

class WeiboAuthURLLView(View):
    """定义微博第三方登录的视图类"""
    def get(self, request):
        next = request.GET.get('state')
        if not next:
            next = "/index/"

        # 获取微博登录网页
        oauth = OAuthWeibo(client_id=settings.WEIBO_APP_ID,
                        client_secret=settings.WEIBO_APP_KEY,
                        redirect_uri=settings.WEIBO_REDIRECT_URI,
                        state=next)
        login_url = oauth.get_weibo_url()
        return JsonResponse({"login_url": login_url})



class WeiboCallbackView(View):
    """验证微博登录"""

    def get(self, request):

        # 1.获取code值
        code = request.GET.get("code")
        state=request.GET.get("state")


        # 2.检查参数
        if not code:
            return JsonResponse({'errors': '缺少code值'}, status=400)

        # 获取微博登录网页
        weiboauth = OAuthWeibo(client_id=settings.WEIBO_APP_ID,
                               client_secret=settings.WEIBO_APP_KEY,
                               redirect_uri=settings.WEIBO_REDIRECT_URI,
                               state=state)
        weibotoken = weiboauth.get_access_token(code=code)
        uid=weibotoken.get("uid")
        print(uid)

        # 5.判断是否绑定过美多账号
        try:
            weibo_user = OAuthSinaUser.objects.get(uid=uid)
        except:
            # 6.未绑定,进入绑定页面,完成绑定
            tjs = TJS(settings.SECRET_KEY, 300)
            uid=tjs.dumps({'uid': uid}).decode()

            return render(request, 'oauth_callback.html', {'token': uid})
        # 绑定的用户
        login(request, weibo_user.user)

        # 将用户写入cookie方便在页面中展示
        response = redirect("/index/")
        response.set_cookie("username", weibo_user.user.username)
        return response

    def post(self, request):
        # 1.数获取据
        data = request.POST
        mobile = data.get("mobile")
        password = data.get("pwd")
        sms_code = data.get("sms_code")
        uid= data.get("access_token")
        # 2.验证数据
        client = get_redis_connection("verify_code")
        real_sms_code = client.get("sms_code_%s" % mobile)
        if real_sms_code is None:
            return render(request, "oauth_callback.html", {"error": "短信验证码已失效"})
        if sms_code.lower() != real_sms_code.decode():
            return render(request, "oauth_callback.html", {"error": "验证码输入的不对"})
        try:
            user = User.objects.get(mobile=mobile)
            if not user.check_password(password):
                return render(request, "oauth_callback.html")
        except:
            # 若当前手机未注册为美多用户，使用当前的手机号创建一个新的新用户
            user = User.objects.create_user(username=mobile,mobile=mobile,password=password)

        # 将openid绑定在表中
        tjw = TJS(settings.SECRET_KEY, 300)
        try:
            data = tjw.loads(uid)
        except:
            return render(request, "oauth_callback.html")
        uid = data.get("uid")
        OAuthSinaUser.objects.create(uid=uid, user=user)

        login(request, user)
        response = redirect("/index/")
        response.set_cookie("username", user.username, 60 * 60)
        return response
