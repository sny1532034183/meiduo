from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login
from django.conf import settings
from QQLoginTool.QQtool import OAuthQQ

from carts.utils import merge_cart_cookie_to_redis
from oauth.models import OAuthQQUser
from django_redis import get_redis_connection
from users.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as TJW

class QQLoginView(View):
    def get(self,request):
        next=request.GET.get("next")
        if next is None:
            next="/index/"
        qq=OAuthQQ(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET,
                   redirect_uri=settings.QQ_REDIRECT_URI,state=next)
        login_url=qq.get_qq_url()
        print(login_url)
        return JsonResponse({"login_url":login_url})


class QQCallBackView(View):
    def get(self,request):
        # 1.获取code值和state
        code=request.GET.get("code")
        state=request.GET.get("state")
        print(code,state)
        state="/index/"
        if code is None or state is None:
            return JsonResponse({"error":"缺少参数"})

        #2.生成qq对象
        qq=OAuthQQ(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET,
                   redirect_uri=settings.QQ_REDIRECT_URI,state=state)
        try:
            # 3.调用方法获取access_token值
            access_token=qq.get_access_token(code)
            openid=qq.get_open_id(access_token)
        except:
            return JsonResponse({"error":"网络错误"})
        try:
            #判断qq有没有绑定美多账号
            qq_user=OAuthQQUser.objects.get(openid=openid)
        except:
            tjw = TJW(settings.SECRET_KEY, 300)
            openid = tjw.dumps({'openid': openid}).decode()
            return render(request, 'oauth_callback.html', {'token': openid})
        #绑定的用户
        login(request,qq_user.user)

        #将用户写入cookie方便在页面中展示
        response=redirect(state)
        response.set_cookie("username",qq_user.user.username,60 * 60 * 2)
        #合并购物车
        response = merge_cart_cookie_to_redis(request,qq_user.user,response)
        return response

    def post(self,request):
        """
        绑定qq用户
        :param request:
        :return:
        """
        # 1.数获取据
        data=request.POST
        mobile=data.get("mobile")
        password=data.get("pwd")
        sms_code=data.get("sms_code")
        openid=data.get("access_token")
        #2.验证数据
        client=get_redis_connection("verify_code")
        real_sms_code=client.get("sms_code_%s"%mobile)
        if real_sms_code is None:
            return render(request,"oauth_callback.html",{"error":"短信验证码已失效"})
        if sms_code.lower()!=real_sms_code.decode():
            return render(request,"oauth_callback.html",{"error":"验证码输入的不对"})
        try:
            user=User.objects.get(mobile=mobile)
            if not user.check_password(password):
                return render(request,"oauth_callback.html")
        except:
            #若当前手机未注册为美多用户，使用当前的手机号创建一个新的新用户
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)

        #将openid绑定在表中
        tjw=TJW(settings.SECRET_KEY,300)
        try:
            data=tjw.loads(openid)
        except:
            return render(request,"oauth_callback.html")
        openid=data.get("openid")
        OAuthQQUser.objects.create(openid=openid,user=user)

        login(request,user)
        response=redirect("/index/")
        response.set_cookie("username",user.username,60*60*2)
        #合并购物车
        response = merge_cart_cookie_to_redis(request,user, response)
        return response