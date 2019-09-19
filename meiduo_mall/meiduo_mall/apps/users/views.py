from django.shortcuts import render,redirect
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from carts.utils import merge_cart_cookie_to_redis
from users.models import User
import re
import json
from django.conf import settings
# Create your views here.
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as TJW

class IndexView(View):
    #两种方式在index页面展示欢迎你：username
    def get(self,request):
        user=request.user
        return render(request, 'index.html', {"user":user})

        # return render(request,"index.html",)

class UserRegisterView(View):
    """
        用户注册
    """

    def get(self, request):
        """
            获取注册页面
        :param request:
        :return:
        """
        return render(request, 'register.html')

    def post(self, request):
        # 1、获取前端传递的表单数据
        data = request.POST
        username = data.get('user_name')
        pwd1 = data.get('pwd')
        pwd2 = data.get('cpwd')
        mobile = data.get('phone')
        image_code = data.get('pic_code')
        sms_code = data.get('msg_code')
        allow = data.get('allow')
        # 2、验证表单数据
        # 验证表单数据否存在
        if username is None or pwd1 is None or pwd2 is  None or mobile is None or image_code is None or sms_code is None or allow  is None:
            return render(request, 'register.html', {'error_allow': 'true'})
        # 验证用户名长度
        if len(username) < 5 or len(username) > 20:
            return HttpResponse('长度不符合要求',status=400)
        if re.match(r"1[3-9]\d{9}",username):
            if username!=mobile:
                return render(request, "register.html")
        # 验证用户名是否存在
        try:
            user = User.objects.get(username=username)
        except:
            user=None
        if user:
            return  HttpResponse('用户存在',status=400)
        # 验证两次密码是否一致
        if pwd1 != pwd2:
            return HttpResponse('密码不一致', status=400)
        # 验证手机号格式
        if not re.match(r'1[3-9]\d{9}',mobile):
            return HttpResponse('手机格式不正确', status=400)
        # 手机号长度
        if len(mobile) != 11:
            return HttpResponse('手机格式不正确', status=400)
        # 验证短信验证码长度
        if len(sms_code) != 6:
            return HttpResponse('短信验证码不正确', status=400)
        #判断验证码是否一致
        client=get_redis_connection("verify_code")
        real_sms_code=client.get("sms_code_%s"%mobile)
        if real_sms_code is None:
            return HttpResponse("短信验证码已失效")
        if sms_code != real_sms_code.decode():
            return HttpResponse("短信验证码错误")
        # 3、保存数据到数据库中
        # User.objects.create(username=username,mobile=mobile,password=pwd1)
        user=User.objects.create_user(username=username,mobile=mobile,password=pwd1)

        login(request,user)

        # 4、注册成功后，引导用户跳转首页

        return redirect("/index/")

# 登录
class LoginView(View):
    def get(self,request):
        return render(request, "login.html")

    def post(self,request):
        data=request.POST
        username=data.get("username")
        password=data.get("pwd")
        remembered=data.get("rememberd")
        # next=data.get("next")
        # if next is None:
        next="/index/"
        # if username is None or password is None:
        #     return render(request,"login.html")
        # try:
        #     user=User.objects.get(username=username)
        # except:
        #     return render(request,"login.html")
        # if not user.check_password(password):
        #     return render(request,"login.html")

        user=authenticate(request,username=username,password=password)  #django认证系统提供的用户校验方法，校验成功，返回用户对象，校验失败，返回none
        if user is None:
            return render(request, "login.html")

        #状态保持
        login(request,user)

        # 判断用户是否选择记住登录
        if remembered == 'on':
            request.session.set_expiry(60 * 60 * 24 * 7)
            response = redirect(next)
            response.set_cookie('username', username, 60 * 60 * 24 * 7)
        else:
            request.session.set_expiry(60 * 60 * 2)
            response = redirect(next)
            response.set_cookie('username',username, 60 * 60 * 2)
        #合并购物车
        response = merge_cart_cookie_to_redis(request,user,response)
        # 4、跳转到首页
        return response


class LogoutView(View):
    def get(self,request):
        logout(request)
        response=redirect("/login/")
        response.delete_cookie("username")
        return response


@method_decorator(login_required,name="dispatch")
#login_required本身只能装饰方法，配合method_decorator类装饰器一块进行使用
class UserInfoView(View):
    "用户中心"
    def get(self, request):
        return render(request, 'user_center_info.html')


@method_decorator(login_required,name="dispatch")
class UserEmailView(View):
    def put(self,request):
        """邮箱更新"""
        #1.获取json数据
        data=request.body.decode()
        #将接送转化为字典
        data_dict=json.loads(data)
        to_email=data_dict["email"]
        #3.验证邮箱的有效性，往用户输入的邮箱中发送邮件
        #标题   邮件信息内容  用户看到发件人信息 收件人的邮箱  html_message
        user=request.user
        tjw=TJW(settings.SECRET_KEY,300)
        token=tjw.dumps({"username":user.username,"email":to_email}).decode()
        verify_url=settings.EMAIL_VERIFY_URL+"?token=%s"%token
        subject="美多商场邮箱验证"
        html_message="<p>尊敬的用户你好</p>"\
                     "<p>感谢你使用美多商场</p>"\
                     "<p>你的邮箱为:%s，请点击连接激活你的邮箱</p>"\
                     "<p><a href='%s'>%s<a></p>"%(to_email,verify_url,verify_url)
        send_mail(subject, '', settings.EMAIL_FROM, ['sunningyanaaa@163.com'], html_message=html_message)

        #邮箱更新
        user=request.user
        if not user.is_authenticated:
            return JsonResponse({"code":4101})
        user.email=to_email
        user.save()
        return JsonResponse({"code":0})

@method_decorator(login_required, name='dispatch')
class UserEmailVerifyView(View):
    def get(self, request):
        """
            验证跳转到美多的邮箱验证验证连接
        :param request:
        :return:
        """
        # 1、获取token数据
        token = request.GET.get('token')
        if token is None:
            return HttpResponse("缺少token值", status=400)
        # 2、解密token
        tjs = TJW(settings.SECRET_KEY, 300)
        try:
            data = tjs.loads(token)
        except:
            return HttpResponse("无效token值", status=400)
        # 3、提取username和email
        username = data.get('username')
        email = data.get('email')
        if username is None or email is None:
            return HttpResponse("token值失效", status=400)
        # 4、验证username和email的数据机用户是否正确
        try:
            user = User.objects.get(username=username, email=email)
        except:
            return HttpResponse("错误的数据", status=400)
        # 5、更细邮箱状态
        user.email_active = True
        user.save()
        # 6、返回结果
        return render(request, 'user_center_info.html')


# 修改密码
#修改密码前需要校验原始密码是否正确，以校验修改密码的用户身份信息
# 如果密码正确，再将新的密码赋值给用户
class ChangePasswordView(View):
    def get(self,request):
        "展示修改密码界面"
        return render(request,"user_center_pass.html")

    def post(self,request):
        #实现修改密码逻辑
        old_password=request.POST.get("old_pwd")
        new_password1=request.POST.get("new_pwd")
        new_password2=request.POST.get("new_cpwd")

        #校验参数
        if not all([old_password,new_password1,new_password2]):
            return render(request,"user_center_pass.html")
        if not request.user.check_password(old_password):
            return render(request,"user_center_pass.html",{"errors_pwd":"原始密码错误"})
        if new_password1!=new_password2:
            return render(request,"user_center_pass.html",{"errors_pwd":"两次密码不一致"})

        try:
            request.user.set_password(new_password1)
            request.user.save()
        except:
            return render(request,"user_center_pass.html",{"errors":"修改密码错误"})

        #清理状态保持
        logout(request)
        response=redirect("/login/")
        response.delete_cookie("username")
        # 响应密码结果重定向到登录页面
        return response



class FindPwdView(View):
    def get(self,request):
        return render(request,"find_password.html")


# class ChangePwdView(View):
#     def post(self,request,user_id):
#         data=request.body.decode()
#         data_dict=json.loads(data)
#         password=data_dict.get("password")
#         password2=data_dict.get("password2")
#         access_token=data_dict.get("access_token")
#         #1.非空
#         if not all([access_token,password,password2]):
#             return HttpResponse("填写数据不完整")
#         if password!=password2:
#             return HttpResponse("两个密码不一致")
#
#         user_dict = meiduo_signature.loads(access_token, 300)
#         if user_dict is None:
#             return JsonResponse({},status=400)
#         if int(user_id)!=user_dict["user_id"]:
#             return JsonResponse({},status=400)
#
#         try:
#             user=User.objects.get(id=user_id)
#         except:
#             return JsonResponse({},status=400)
#         user.set_password(password)
#         user.save()
#         return JsonResponse({})