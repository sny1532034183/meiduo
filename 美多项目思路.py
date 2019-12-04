# 一：立定
# 1.在码云上创建项目，并且克隆远程仓库到本地，步骤不细说
# 2.创建分支
# 3.在meiduo_mall下创建static用来存放前端资源
# 4.push到码云(git push origin dev:dev)
# 5.在马云上发起合并请求(pull requests)
# 6.安装静态文件服务器live-server,和python无关
# (1)安装node.js版本控制工具  curl -o- https://raw.githubusercontent.co ... v0.33.11/install.sh | bash
# (2)重新进入终端，下载最新的node.js    nvm install node
# (3)安装live-server  npm install -g live-server
# (4)使用live-server  在静态文件目录front_end_pc 下执行：live-server

# 7.创建虚拟环境，创建meiduo_mall项目
# (1)添加logs目录(记录日志)
# (2)同名meiduo_mall
# (2.1)在meiduo_mall下添加apps包(存放应用)
# (2.2)meiduo_mall下创建settings包(开发配置文件dev、生成配置文件prod)
# (2.3)在meiduo_mall下创建libs包(第三方包captcha图片验证码、yuntongxun)
# (2.4)在meiduo_mall下创建templates包(模板文件)
# (2.5)在meiduo_mall下创建utils包(工具包jinja2)


# 二.配置
# 1.在dev文件中添加使用配置文件的模块
# (1)import sys
# (2)sys.payh.insert(0,os.path.join(BASE_DIR,"apps"))
# (3)就可以直接在dev中的install_apps，直接使用app名字注册
# (4)在manage.py文件中修改配置文件的路径  os.environ.setdefault("DJANGO_SETTINGS_MODULE","meiduo_mall.settings.dev")
# 2.创建数据库及为数据库创建账号
# create database meiduo_mall charset=utf8;
# create user meiduo identified by "meiduo"   创建账号及密码
# grant all on  meiduo_mall.* to "meiduo"@"%"   授权meiduo_mall下数据库下的所有表的所有权限给用户meiduo再以任何ip访问数据库的时候
# flush privileges   刷新生效用户权限
# 3.在dev中配置数据库，在同名，项目的init文件中添加：
#     import pymysql
#     pymysql.install_as_MySQLdb()
# 4.安装redis并在dev中配置一个是默认的default，还有一个是session ，底下SESSION_CACHE_ALIAS="session"
# 5.在dev中配置本地化语言还有时间
# 6.在dev中配置日志
# 7.异常处理(修改django REST framework的默认异常处理方法(默认处理了序列化器抛出的异常)，补充
# 处理数据库异常和redis异常)
# (1)在dev中配置异常处理器，显示的给EXCEPTION_HANDLER设置你期望的值：
#    REST_FRAMEWORK={"EXCEPTION_HANDLER":"meiduo_mall.utils.exception_handle"}
# (2)在utils下创建exceptions.py
# (3)from rest_framework.views import exception_handler as drf_exception_handle
#    import logging
#    from django.db import DatabaseError
#    from redis.exceptions import RedisError
#    from rest_framework.response import Response
#    from rest_framework import status
#
   #获取在配置文件中定义的logger，用来记录日志
   # logger=logging.getLogger("django")
   # def exception_handle(exc,content):
   #     """
   #     :param exc: 异常
   #     :param content:  抛出异常的上下文
   #     :return: Response 响应对象
   #     """
   #     #调用drf框架原生的异常处理方法
   #     response=drf_exception_handle(exc,content)
   #     if response is None:
   #         view=content["view"]  #通过context["view"]获取当前的视图
   #         if isinstance(exc,DatabaseError) or isinstance(exc,RedisError):
   #             #数据库异常
   #              logger.error("[%s]%s"%(view,exc))
   #              response=Response({"message":"服务器内部出错"},status=status.HTTP_507_INSUFFICIENT_STORAGE)
   #         return response
# (4)添加配置文件
# REST_FRAMEWORK = {
#     # 异常处理
#     'EXCEPTION_HANDLER': 'meiduo_mall.utils.exceptions.exception_handler',
# }


# 三：登录注册模块
# 1.使用django认证系统中的用户模型类创建自定义的用户模型类
# 在apps下的users下的models
# from django.comtrib.auth.models import AbstraUser
# class User(AbstractUser):
#     """用户模型类"""
#     mobile=mobile.CharField(max_length=11,unique=True,verbose_name="手机号")
#     class Meta:
#         db_table="tb_users"
#         verbose_name="用户"
#         verbose_name_plural=verbose_name
#

# 2.在dev配置中指明自定义的用户模型类
# 3.进行数据库迁移(第一次数据库迁移必须在配置自定义用户模型类之后)
#   python manage.py makemigrations
#   python manage.py migrate

# 4.图片验证码
# (1)分析接口设计
# <1>接口的请求方式
# 接口的url路径定义
# 需要前端传递的数据及数据格式(如路径参数、查询字符串、请求体表单、json等)
# 返回给前端的数据及数据格式
# <2>用户注册中需要实现的接口
# 图片验证码
# 短信验证码
# 用户名判断是否存在
# 手机号判断是否存在
# 注册保存用户数据

# (2)在apps中创建新的应用verifications
# (3)在dev配置中注册应用
# (4)新建图片验证码类视图
#   <1>接收参数
#   <2>校验参数
#   <3>生成验证码图像
#   <4>保存真实值
#   <5>返回图片
# (5)在libs创建一个captcha包，里面创建第三方生成验证码captcha文件
# (6)添加redis保存验证码的配置饿
# (7)在verifications下创建constans存放常量
# (8)添加url然后在全局url中包含
#
#
# 5.本地域名映射
# (1)vim /etc/hosts
# (2)在文件中增加两条信息
#    <1>前端：127.0.0.1  www.meiduo.site
#    <2>后端:127.0.0.1   api.meiduo.site
# (3)在dev配置文件中ALLOWED_HOSTS添加可访问的地址ALLOWED_HOSTS=['api.meiduo.site', '127.0.0.1', 'localhost', 'www.meiduo.site']
# (4)在front_end_ps/js中新建host.js为前端保存后端域名，添加var host='http://api.meiduo.site:8000'
#
#
# 6.修改前端代码
# (1)在register.html导入host.js
# (2)修改js代码
#  <1>创建生成uuid函数
#  <2>创建获取图片验证码函数
#  <3>添加变量存储存储uuid
#  <4>为图片验证码的src绑定一个变量, 变量存储的是图片验证码的url(: src = "")
#  <5>js中添加存储图片验证码url的变量
#  <6>添加全局的host变量
#  <7>拼接图片验证码的url放入存储图片验证码的变量中
#  <8>在js中的vue.js页面加载完就执行的方法中调用获取图片验证码函数
#  <9>在html为图片添加点击事件, 调用获取图片验证码的函数( @ click = "")
#
#
# 7.短信验证后端逻辑
# (1)接口设计
# (2)在verifications新建短信验证码类视图，GET请求，继承GenericApiView
#   <1>校验参数(由序列化完成)
#   <2>生成短信验证码
#   <3>保存短信验证码，发送记录
#   <4>发送短信
#   <5>返回
# (3)添加序列化验证参数
#  <1>验证是否符合格式
#  <2>添加校验方法
#  <3>获取数据
#  <4>查询真实的图片验证码，查询失败抛出异常
#  <5>解码图片验证码，比较图片验证码，错误的话raise serializer.ValidationErroe("")
#  <6>判断手机号是否在60秒内(获取redis中的手机发送标志，如果有数据，说明已经发送过了，抛出异常)
#  <7>返回字典数据
# (4)生成短信验证码
# (5)保存短信验证码
# (6)保存短信验证码的发送记录
# (7)发送短信
#  <1>导入云通讯到libs下
#  <2>创建发送短信验证码的对象
#  <3>设置短信验证码的有效分钟数：expires=短信验证码有效时间
#  <4>传参(send_template_sms(手机号,[验证码，短信验证码，有效分钟数],模板id常量))
#  <5>为发送短信验证码捕获异常，写入日志，返回结果
# (8)添加路由
# (9)为保存短信验证码补充redis管道
#  redis_conn=get_redis_connectuion("verify_codes")
#  pl=redis_conn.pipeline()
#  pl.setex("sms_code%s"mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
#  pl.setex("senf_flag-%s"mobile,constants,SEND_SMS_CODE_INTERVAL,1)
# (10)序列化器中删除短信验证码(验证码输错或输对都删除，即查询出来就从redis中删除)
#  try:
#      redis_conn.delete("img_%s"%image_code_id)
#  except RedisError as e:
#      logger.error(e)
# (11)添加全前端代码
#
#
# 8.CORS解决跨域请求
# (1)安装扩展：pip install django-cors-headers
# (2)dev配置文件install_apps注册
# (3)dev中 在中间件中添加中间件配置，放在最上面:"corsheaders.middleware.CorsMiddleware"
# (4)dev中 添加白名单配置：
#    CORS_ORIGIN_WHITELISH=(
#        "127.0.0.1:8080"
#        "localhost:8080"
#        "www.meiduo.site:8080"
#        "api.meiduo.site:8000"
#    )
#    CORS_ALLOW_CREDENTIALS=True  #允许携带cookie
#
#
# 9.在meiduo仓库下meiduo_mall下创建celery包
# (1)创建main.py(celery的启动模块)和config.py
# (2)在celery包下为短信验证码sms_code创建包,在再包下创建task.py文件
# (3)安装celery扩展
# (4)在main.py下导入Celery并创建celery应用：app=Celery("meiduo")
# (5)在config.py文件中添加配置：
#   broker_url="redis://127.0.0.1/4"(沟通桥梁的信息，存储任务的队列)
#   result_backend="redis://127.0.0.1/15"(保存任务运行完成之后的返回结果信息，比如函数的返回值，任务id，状态等)
# (6)在main.py中导入celery配置：app.config_from_object("celery_tasks.config")
# (7)main下注册任务：app.autodiscover_tasks（["celery_tasks.sms_code"]）
# (8)把发送短信的代码写在sms_code下
#     @celery_app.task(name='send_sms_code')
#     def send_sms_code(mobile,sms_code):
#         ccp=CCP()
#         ccp.send_template_sms(mobile, [sms_code, '5'], 1)
# (9)把短信验证码工具包在copy一份放在celery_tasks下
# (10)修改原来发送短信验证码的代码，在verification下的views中，用到一些变量传参的方式
# (11)导入日志，添加django的日志配置文件logger=logging.getLogger("django")
# (12)在main.py文件中添加celery使用django配置的代码;
#   import os
#   if not os.getenv("DJANGO_SETTINGS_MODULE"):
#       os.environ["DJANGO_SETTINGS_MODULE"]="meiduo_mall.settings.dev"
# (13)sms_code下的tasks文件下使用装饰器发送验证码的方法：就是上面的(8)
#     导入app：from celery_tasks.main import celery_app
#     使用的应用于名.task(),其中装饰器的参数是为了指明任务的名字，在运行的时候可以知道调用了那个任务运行
#
# (14)在verification发送短信验证码的视图函数中调用发送短信验证码的方法并传参
#   <1>导包:from celery_tasks.sms_code.tasks import send_sms_code
#   <2>expires=constants.SMS_CODE_REDIS_EXPIRES//60
#   <3>send_sms_code.delay(mobile,sms_code,expires,contants.SMS_CODE_TEMP_ID)
#   <4>return Response({"message":"ok"})
#
# (15)启动celery(在异步所在目录下)：celery -A celery_tasks.main worker -I info
#    -A代表一个应用，后面跟的就是启动文件的路径
#    -I info 表示显示所有级别在info以上的worker日志信息
#
# --------------------------------------------------
#
# 10.判断账号
# (1)判断用户是否存在
#  <1>users下定义类视图
#  <2>获取指定用户名的数量
#  <3>返回数据
#  <4>前端实现
# (2)判断手机号是否存在
#  <1>user下定义类视图
#  <2>获取指定的手机号的数量
#  <3>返回数据
#  <4>前端实现


# 11.用户注册
# (1)在users应用下创建新的类视图(继承createAPIView)实现用户注册(参数:username、
#    password1、password2、sms_code、mobile、allow)
#     <1>类视图中使用序列化器类(createUserSerializer)
# (2)实现序列化器
#     <2>导入rest_framwork的serializer
#     <3>创建序列化器CreateUserSerilizer,继承serialize.ModelSerializer
#     <4>添加自定义字段(数据库模型类么有的字段)都设为校验时使用的字段(添加属性：write_only=True)
#     <5>声明序列化器类有哪些字段和映射那个模型类：
#     class Meta:
#         model = User
#         fields = (所有需要显示的字段名, 包括模型类里面的以及自定义的, 此时校验和返回都是这些字段)
#     <6>使用extra_kwargs对字段指明额外的需求
#     <7>对特定的字段进行校验(validate_字段名):包括mobile、allow
#     <8>对多个字段同时进行校验(validate):判断两次密码和短信验证码
#     <9>重写保存方法(create),增加密码加密功能
#         (1):移除数据库模型类不存在的属性(allow,sms_code,password2)
#         (2):调用父类的保存方法
#         (3):调用django的认证系统加密码，保存
#         (4):返回user
#
# (3)实现注册的前端js


# 12.使用JWT机制判断用户身份
# (1).安装扩展：pip install djangorestframework-jwt
# (2)在dev配置文件中得REST_FRAMWORK中添加认证的配置：
# 'DEFAULT_AUTHENTICATION_CLASSES': (
#     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#     'rest_framework.authentication.SessionAuthentication',
#     'rest_framework.authentication.BasicAuthentication',
# )
# (3)在dev配置文件中添加JWT的配置token的有效期
#     JWT_AUTH = {
#         'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
#     }
#
# (4)在注册时的序列化创建了多用户之后签发jwttoken(记录登录状态)
#  <1>导包：from rest_framework_jwt.settings import api_settings
#  <2>签发JWT：
#     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#     payload = jwt_payload_handler(user)
#     token = jwt_encode_handler(payload)
# (5)添加返回的字段token并且把生成的token存在这个字段：比如user.token=token
#
# 6)前端保存token:
#         sessionStorage浏览器关闭即失效
#         localStorage 长期有效
#         1>在js中sessionStorage.clear()
#         2>localStorage.clear()
#         3>localStorage.token = response.data.token
#         4>localStorage.user_id = response.data.user_id
#         5>localStorage.username = response.data.name


# 13.登录
# 在users下的urls下添加登录签发JWT的视图
# (1)导包：from rest_framework_jwt.views import obtain_jwt_token
# (2)添加路由：url(r"^authorizations/$",obtain_jwt_token)
# (3)在user下的views中创建jwt_response_payload_handle函数修改视图到的返回值
# (4)在dev配置中的JWT_AUTH中添加配置
#     "JWT_RESPONSE_PAYLOAD_HANDLER":"users.utils.jwt_response_payload_handler"
# (5)在users/views下自定义一个类(UsernameMobileAuthBackend)继承自ModelBackend,重写django认证系统ModelBackend
#    里面的authenticate(self,request,username=None,password=None,**kwargs)方法自定义用户名或者手机号认证(因为username可能是用户名,也可能是手机号)
# (6)抽出一个根据账号来获取用户对象的方法(get_user_by_account(account))放在自定义类的外面
#  <1>正则账号信息判断是否为手机号，根据手机号查询数据库获得用户对象
#  <2>否则根据用户名查询数据库获得用户对象
#  <3>捕获异常，因为是get查询数据库，不存在返回none，否则返回用户对象
# (7)在重写的authenticate方法中调用获取对象的方法，传参为接收到的username，接收获取的用户对象
# (8)验证用户对象的密码，认证成功返回用户对象
#   if user is not None and user.check_password(password):
#       return user
# (9)配置文件中添加认正方法的配置
#     AUTHENTICATION_BACKENDS=['users.utlis.UsernameMobileAuthBackend']
#
# (10)修改前端页面
#
#
# 14.qq登录
# (1)注册成为qq互联开发人员
#   http://wiki.connect.qq.com/%E6%8 ... 0%E5%8F%91%E8%80%85
# (2)创建应用，获取项目对应与qq互联的应用id：
#    http://wiki.connect.qq.com/__trashed-2
# (3)根据qq登录开发文档进行开发，文档连接
#   http://wiki.connect.qq.com/%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C_oauth2-0
# (4)创建qq登录模型类
# (5)创键一个新的应用:oauth
#  <1>添加到dev的注册app
# (6)创建qq登录模型类(继承自基类)，并且进行数据库的迁移
# (7)第一个接口：oauth中创建类视图(继承APIView,get方式)返回qq登录的网址
#  <1>获取next参数，如果没有，返回主页next="/"
#  <2> 拼接qq登录的网址(调用拼接qq登录网址的辅助工具类，传入参数：OauthQQ(state=next))
#  <3>返回(Response({"login_url":"login_url"}))
# (8)oauth下创建utils文件，创建qq认证辅助工具类的(OauthQQ)拼接qq登录网址
#  <1>定义方法拼接url(get_login_url)
#  <2>根据文档查看url以及需要发送的参数(client_id,redirect_url,state)参数设置成字典数据类型
#  <3>发送的参数在__init__下定义，因为每个对象的参数不一样，创建对象时传入
#  <4>在dev配置文件中设置qq登录时的默认值，在不传参时就使用默认值(因为有些值是一样的
#     不需要改变，就可以使用默认值)
#         QQ_CLIENT_ID = '101474184'
#             QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
#             QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'
#             QQ_STATE = '/'
#
#  <5>通过form django.conf import settings 使用django的配置文件中的内容
#  <6>使用urllib.parse下的urlencode(字典)，将字典转换为url路径中的查询字符串，拼接到url后面
#     from urllib.parse import urlencode
#  <7>返回url
#
# (9)注册路由&在总路由中包含，设置前缀（oauth）
# (10)实现qq登录前端，在login.js中增加qq登录的方法，请求成功获取返回的qq登录网址，调准到qq登录的页面
# (11)前端处理QQ_REDIRECT_URL设置的oauth_callback.html
#  <1>创建oauth_callback.html
#  <2>js中创建oauth_callback.js

# (12)第二个接口
# (1)创建新的类视图:QQAuthUserView(ApiView),判断qq登录的用户
# (2)获取code，如果不存在返回信息
# (3)凭借code获取access_token：创建辅助工具类，调用get_access_token()方法，传参数为code
#  <1>在qq认证辅助工具类中添加获取access_token的方法get_access_token
#  <2>添加url，设置参数
#  <3>拼接url带上参数
#  <4>使用urllib.request.urlopen(url,data=none)发送请求，获得返回响应
#  <5>读取响应体数据，响应调用read()读取数据，解析数据decode()
#  <6>解析响应体数据，urllib.parse.paese_qs(数据),解析出来是字典
#  <7>d读取access_token(在异常抛出之后)在一个子弹中获取access_toekn是一个列表，然后返回access_token[0]
#  <8>辅助类中捕获异常,记录日志,抛出异常:发送请求时开始捕获,解析完成后记录异常('获取access_token异常:%s'%e),
#     并抛出异常自定义的异常OAuthQQAPIError.如果没有异常再进行读取access_token.
#  <9>自定义一个异常：
#      a.oauth下创建新的模块exception.py
#      b.创建自定义的异常类OauthQQApiError,继承exception，不实现，直接pass
#  <10>在类视图中调用get_access_token()时捕获自定义的异常:OAuthQQAPIError
#  <11>直接返回Response({'message': '访问QQ接口异常'})
# (4)凭借access_token获取openid
#  <1>走到这一步说明access_token获取成功
#  <2>调用qq工具类的中的获取openid方法(get_openid)，参数为access_token
#  <3>根据qq互联wend编写get_openid
#  <4>和获得access的流程类似
#  <5>得到的数据不同，解析的openid的方式也不一样
#  <6>返回的数据：callback({"client_id":"YOUR_APPID","openid":"YOUR_OPENID"})
#  <7>通过切片解析数据，转化为json字符串为字典，抛异常
# (5)根据openid查询数据库OauthQQuser，捕获异常判断数据是否存在
# (6)如果数据不存在，处理openid并返回
# (7)如果数据存在，表示用户已经绑定过身份，签发JWT token
# (8)返回JWT_token数据
# (9)拼接路由
# (10)修改前端oauth_callback.js中的mounted方法

#
# (13)第三个接口
# 1 > 在QQAuthUserView中定义post方法
# 2 > 获取数据
# 3 > 校验数据
# 4 > 判断用户是否存在, 如果存在, 绑定, 创建OAuthQQUser数据
# 5 > 如果不存在, 先创建User, 再创建OAuthQQUser
# 6 > 签发JWT
# token
#
# 7 > 上面的这套流程可以直接继承CreateAPIView
# 8 > 直接在视图函数中调用序列化器OAuthQQUserSerializer
# 9 > 添加序列化器模块, 定义序列化器OAuthQQUserSerializer
# 10 > 实现OAuthQQUserSerializer: 继承serializer.ModelSerializer
# (1).添加字段sms_code只反序列化, access_token只反序列化, token只序列化.抽出mobile字段(可序列化,
#                                                                可反序列化), 因为模型类中的mobile设置了只能是唯一, 这里需要抽出来, 把只能是唯一的验证去掉, 不抽出来在模型类中会抛出异常, 那么后面的判断手机号是否在数据库中就没有办法判断了.
# (2).Meta中指定模型类, 指定显示字段fields = ('mobile', 'password', 'sms_code', 'access_token', 'id', 'username', 'token')
# (3).为字段添加额外的条件: extra_kwargs = {
#     'username': {
#         'read_only': True
#     },
#     'password': {
#         'write_only': True,
#         'min_length': 8,
#         'max_length': 20,
#         'error_messages': {
#             'min_length': '仅允许8-20个字符的密码',
#             'max_length': '仅允许8-20个字符的密码'
#         }
#     }
# }
# (4).定义校验数据的方法validate.
# (5).获取access_token
# (6).校验access_token, 在QQ辅助工具类中添加校验access_token的静态方法, 使用的是itsdangerous模块, 因为生成也是这个模块.返回校验后的openid
# (7).validate中赋值openid: attrs['openid'] = openid
# (8).校验短信验证码, 失败抛出异常
# (9).根据mobile获取user, 捕获异常, 不存在抛出异常, pass操作, 没有异常则获取密码, 验证码密码, 调用user的密码认证系统: user.check_password(
#     password), 如果没有返回值, 抛出验证错误异常, 提示密码错误.
# (10)
# 密码验证通过则把user添加到序列化器的数据字典中: attrs['user'] = user
# (11).返回attrs
# (12).修改序列化器的create方法.
# (13).获取user, openid, mobile, password
# (14).如果user不存在, 在数据库中创建这个user, 用户名为手机号, 手机号也是手机号, 密码为前端发送过来校验后的密码.调用的django认证系统的创建用户的方法create_user()
# (15).绑定, 创建OAuthQQUser数据: OAuthQQUser.objects.create(user=user, openid=openid)
# (16).签发JWT
# token, 和登录里面的一样的.
# (17).返回user
# 11 > 修改oauth_callback.js添加点击submit时的方法


# 注册：
# from django.shortcuts import render,redirect
# from django.views import View
# from django.http import HttpResponse,
# from users.models import User
# import re
# class indexview(View):
#     def get(self,request):
#         return render(request,"index.html")
#
# class userregisterview(View):
#     def get(self,request):
#         return render(request,"register.html")
#
#     def post(self,request):
#         #获取表单数据
#         data=request.POST
#         username=data.get("user_name")
#         pwd1=data.get("pwd1")
#         pwd2=data.get("cpwd")
#         mobile=data.get("phone")
#         image_code=data.get("pic_code")
#         sms_code=data.get("msg_code")
#         allow=data.get("allow")
#         #验证表单数据
#         if usernmae is none or pwd1 is none or pwd2 is none or mobile is  none
#             or image_code is none or sms_code is none or allow is none:
#             return render(request,"register.html",{"error_allow":"true"})
#         #验证用户名长度
#         if len(username)<5 or len(usernmae)>20:
#             return HttpResponse("长度不符合要求，重新输入")
#         try:
#             user=User.objects.get(username=username)
#         except :
#             user=none
#         if user:
#             return HttpResponse("用户存在")
#         #验证密码
#         if pwd1!=pwd2:
#             return HttpResponse("密码不一致")
#         #判断手机号
#         if not re.match(r"1[3-9]\d{9}",mobile) and len(mobile)==11:
#             return HttpResponse("手机号不符合要求")
#         if len(sms_code)!=6:
#             return HttpResponse("输入正确的短信验证码")
#         #保存到数据库中
#         User.objects.create_user(username=usernmae,mobile=mobile,password=pwd1)
#         return redirect("/index/")  #重定向到首页
#
#
#
# #图形验证码
# from django.shortcuts import redirect,render
# from django.views import View
# from django.http import HttpResponse
# from django_redis import get_redis_connection
# from meiduo_mall.libs.captcha.captcha import Captcha
# from users.models import User
# from threading import Thread
#
# class imageview(View):
#     def get(self,request,uuid):
#         #生成图片验证
#         captcha=Captcha.instance()
#         data,text,image=captcha.generate_captcha()
#         client=get_redis_connection("verify_code")
#         client.setex("image_code_%s"%uuid,60*5,text)
#         #返回验证码图片
#         return HttpResponse(image,content_type="image/jpg")
#
# class smscodeview(View):
#     def get(self,request,moblie):
#         client=get_redis_connection("verfiy_code")
#         #判断两次请求的时间间隔是否在60秒内
#         flag_data=client.get("sms_flag_%s"%moblie)
#         if flag_data:
#             return HttpResponse("请求过于频繁")
#         #获取前端数据
#         image_code=request.GET.get("image_code")
#         uuid=request.GET.get("image_code_id")
#         #验证图片验证码
#         client=get_redis_connection("verify_code")
#         real_code=client.get("image_code_%s"%uuid)
#         if real_code is None:
#             return HttpResponse("图片验证码失效")
#         if image_code.lower()!=real_code.lower()
#             return HttpResponse("请输入正确的验证码")
#
#         #生成短信验证码
#         sms_code="%06"%random.randit(0,999999)
#
#         #发送短信调用celery异步任务完成发送短信
#         send_sms_code.delay(moblie,sms_code)
#
#         #b保存生成的短信验证吗到redis
#         # 开启redis管道
#         pl=client.pipeline()
#         pl.setex("sms_code_%s"%moblie,60*50,sms_code)
#         pl.setex("sms_flag_%s"moblie,60,123)
#
# # 判断用户名是否重复注册
# class usernamecount():
#     def get(self,request,ussername):
#         count=User.objects.filter(username=username).count()
#         return JsonResponse({"count":count})
#
# # 判断手机号是否重复注册
# class mobilecount():
#     def get(self,request,mobile):
#         count=User.objects.filter(mobile=mobile).count()
#         return JsonRequest({"count":count})

# from django.shortcuts import render,redirect
# from django.views import View
# from django.http HttpResponse
# from users.models import User
# import re
#
# class indexview(View):
#     def get(self,request):
#         return render(request,"index.html")
#
# class userregister(View):
#     def get(self,request):
#         return render(request,"register.html")
#
#     def post(self,request):
#         data=request.POST
#         username=data.get("user_name")
#         pwd1=data.get("pwd")
#         pwd2=data.get("cpwd")
#         mobile=data.get("mobile")
#         image_code=data.get("pic_code")
#         sms_code=data.get("sms_code")
#         allow=data.get("allow")
#         if username is None or pwd1 is None or pwd2 is None or mobile is None
#             or image_code is None or sms_code is None or allow is None
#             return render(request,"register.html")
#         if len(username)<5 or len(username)>20:
#             return HttpResponse("不符合长度要求")
#         try :
#             username=User.objects.get(username=username)
#         except:
#             username=None
#         if user:
#             return HttpResponse("用户名已存在")
#         if pwd1!=pwd2:
#             return HttpResponse("密码不一致")
#         if not re.match(r"1[3-9]\d{9}",mobile)
#             return HttpResponse("输入正确的手机号格式")
#         if len(mobile):
#             return HttpResponse("手机号格式不对")
#         if len(sms_code)!=6:
#             return HttpResponse("短信验证码不正确")
#         User.objects.create_user(username=username,mobile=mobile,password=pwd1)
#         return redirect("/index/")
#
#
# from django.shortcuts import redirect,render
# from django.views import View
# from django.http import HttpResponse,JsonResponse
# from django_redis import get_redis_connection
# from meiduo_mall.libs.captcha import Captcha
# import random
# from users.models import User
# from celery_tasks import send_sms_code
#
# class immageview(View):
#     def get(self,request,uuid):
#         #生成图片验证码
#         captcha=Captcha.instance()
#         data,text,image=captcha.generate_captcha()
#         #保存到redis
#         client=get_redis_connection("verify_code")
#         client.setex("image_code_%s"%uuid,60,text)
#         #返回验证码图片
#         return HttpResponse(image,content_type="image/jpg")
#
# class smscodeview(View):
#     def get(self,request,mobile):
#         #验证图片验证码
#         image_code=request.GET.get("image_code")
#         uuid=request.GET.get("image_code_id")
#         client=get_redis_connection("verfiy_code")
#         real_image_code=client.get("image_code_%s"%uuid)
#         if real_image_code is None:
#             return HttpResponse("图片验证失效")
#         if real_image_code.lower() != image_code.lower():
#             return HttpResponse("请输入正确的验证码")
#
#         # 判断两次请求是否在60秒之内
#         flag_data=client.GET.get("sms_flag_%s"%mobile)
#         if flag_data:
#             return HttpResponse("两次请求频繁")
#
#         #发送短信
#         sms_code=random.randint(0,999999)
#         send_sms_code.delay(mobile,sms_code)
#
#         #保存数据
#         pl=client.pipeline()
#         pl.setex("sms_code_%s"%mobile,60*5,sms_code)
#         pl.setex("sms_flag_%s"%mobile,60,123)
#         pl.execute()
#
#         return JsonResponse({"code":0})
#
# class usernamcount(View):
#     def get(self,request,username):
#         count=User.objects.filter(username=username).count()
#
#         return JsonResponse({"count":count})
#
# class mobilecount(View):
#     def get(self,request,mobile):
#         count=User.objects.filter(mobile=mobile).count()
#
#         return JsonResponse({"count":count})

# 生成图片验证码
class imageview(view):
    def get(self,request,uuid):
        captcha=Captcha.instance()
        data,text,image=captcha.generate_captcha()
        client=get_redis_connection("verify_code")
        client.setex("image_code_%s"%uuid,60,text)
        return HttpResponse(image,content_type="image/jpg")

class smscodeview(View):

    def get(self,request,mobile):

        client = get_redis_connection("verify_code")
        data=client.get("sms_flag_%s"mobile)
        if data:
            return Httpresponse("短信验证码请求频繁")
        # 随机生成短信验证码
        sms_code = random.randint(0, 999999)

        # 判断短信验证码
        image_code=request.GET.get("image_code")
        uuid=request.GET.get("image_code_id")
        client=get_redis_connection("verify_code")
        real_code=client.get("image_code_%s"%uuid)
        if real_code is None:
            return HttpResponse("验证码失效")
        if real_code.lower() !=image_code.lower():
            return HttpResponse("验证码错误")

        pl=client.pipeline()
        pl.setex("sms_code_%s"%mobile,60,sms_code)
        pl.setex("sms_flag_%s"mobile,60,123)  #设置的flag来判断用户请求频繁
        pl.execute()
        return JsonResponse({"code":0})


from django.shortcuts import render,redirect
from django.views import View
from django_redis import get_redis_connection
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from models import User

#进入首页页面
# class indexview(View):
#     def get(self,request):
#         #user=request.user
#         #return render(request,"index.html",{"user":user})
#         return render(request,"index.html")
#
# #注册页面
# class userregisterview(View):
#     def get(self,request):
#         data=request.POST
#         username=data.get("username")
#         pwd1=data.get("pwd")
#         pwd2=data.get("cpwd")
#         mobile=data.get("iphone")
#         image_code=data.get("image_code")
#         sms_code=data.get("sms_code")
#         allow=data.get("allow")
#         if username is None or pwd1 is None or pwd2 is None or mobile is None or image_code is None
#             sms_code is None or allow is None:
#             return render(request,"register.html")
#         if len(username)<5 or len(username)>20:
#             return render(request,"register.html",{"error":"名字不符合规范"})
#         if pwd1!=pwd2:
#             return render(request,"register.html",{"error":"密码不一致"})
#         if not re.match(r"1[3-9]\d{9}",mobile):
#             return render(request,"register.html",{"error":"手机号不正确"})
#         if len(sms_code)!=6:
#             return HttpResponse("短信验证码不对")
#         client=get_redis_connection("verify_code")
#         real_code=client.get("sms_Code_%s"%mobile)
#         if real_code is None:
#             return HttpResponse("短信验证码失效")
#         if sms_code.lower()!=real_code.lower():
#             return HttpResponse("短信验证码不对")
#
#         user=User.objects.create_user(username=username,password=pwd,mobile=mobile)
#         login(request,user)
#
#         response=redirect("/index/")
#         response.set_cookie("username",username)
#         return response
#
# class loginview(View):
#     def get(self,request):
#         return render(request,"login.html")
#     def post(self,request):
#         data=request.POST
#         username=data.get("username")
#         password=data.get("pwd")
#         remembered=data.get("remembered")
#         user=authenticate(request,username=username,password=password)
#         if user is None:
#             return render(request,"login.html")
#         login(request,user)
#
#         if rememberd=="on":
#             request.session.set_expiry(60*60*24*7)
#             response=redirect("/")
#             response.set_cookie("username",username,60*60*24*7)
#         else:
#             request.session.set_expiry(60 * 60 * 2)
#             response = redirect('/')
#             response.set_cookie('username', username, 60 * 60 * 2)
#         return render(request,"index.html")

# 第三方登录qq
# 一：
# 1.注册成为qq开放平台的开发者
# 2.创建网站应用，提交审核
# 3.审核成功，拿到app_id 和app_key
# 4.前端页面中放置qq图标
# 5.获取access_token
# 6.获取open_id值(是qq用户的唯一标识)

# 二：创建模型类
# from djang.db import models
# class basemodel(models.Model):
#     create_time=models.datetimefield(auto_now_add=True,verbose_name="创建时间")
#     update_time=models.datetimefield(auto_now=True,veribose_name="更新时间")
#     class meta:
#         abstarct=True #用于说明抽象模型类，用于继承使用，数据库迁移时不会创建basemodel表
#
# # 创建一个oauth的应用，在models中   与用户模型类的user关联
# from django.db import models
# from meiduo_mall.utils.models import basemodel
# class oauthqquser(basemodel):
#     user=models.foreignkey("users.user",on_delete=models.CASCADE,verbose_name="用户")
#     openid=models.charfield(max_length=64,verbose_name="openid")
#     class meta:
#         db_table="tb_oauth"
#
# # 三：qq登录SDK使用
# # qq官方没有给出响应的python3版本的SDK，所以，根据qq开放的官方文档手写qq登录SDK
# # 除了手写，还可以使用qqlogintool第三方模块
#
# # 四：自定义qq登录的sdk
# import json
# from urllib.parse import urlencode,parse_qs
# import requests
# from django.conf import settings
#
# class oauth(object):
#     def __init__(self,client_id=none,client_secret=none,redirect_url=none,state=none):
#         self.client_id=client_id or settings.qq_client_id
#         self.client_secret=client_secret or settings.qq_client_secret
#         self.redirect_url=redirect_url or settings.qq_redirect_url
#         self.state=state or settings.qq_state
#
#     def get_qq_url(self):
#         """
#         获取qq登录的连接
#         :return:
#         """
#         data_dict={
#             "response_type":"code"
#             "client_id":self.client_id
#             "redirect_url":self.client_uri
#             "state":self.state
#         }
#         #构造qq登录连接
#         qq_url='https://graph.qq.com/oauth2.0/authorize?'+urlencode(data_dict)
#         return qq_url
#
#     def get_access_token(self,code):
#         """
#         获取access_token
#         :param code:
#         :return:
#         """
#         # 构建参数数据
#         data_dict={
#             "grant_type":"authorization_code"
#             "client_id":self.client_id
#             "client_serect":self.client_secret
#             "redirect_url":self.redirect_url
#             "code":code
#         }
#         # 构造url
#         access_url='https://graph.qq.com/oauth2.0/token?+urlencode(data_dict)
#
#         #发送请求
#         try:
#             response=request.get(access_url)
#             #提取数据
#             data=response.text
#             #转化为字典
#             data=parse_qs(data)
#         except:
#             raise exception("qq请求失败")
#         #提取access_token
#         access_token=data.get("access_token")
#         if not access_token:
#             raise exception("access_token提取失败")
#         return access_token
#
#     def get_open_id(self,access_token):
#         """
#         获取openid
#         :param access_token:
#         :return:
#         """
#         # 构建请求url
#         url = "https://graph.qq.com/oauth2.0/me?access_token=" + access_token
#         #发送请求
#         try:
#             response=requests.get(url)
#             #提取数据
#             data=response.text
#             # 错误的时候返回的结果
#             data=data[10:-3]
#
#         except:
#             raise exception("qq请求失败")
#         #转化为字典
#         try:
#             data_dict=json.loads(data)
#             #获取openid
#             openid=data_dict.get("openid")
#         except:
#             raise exception("openid获取失败")
#         return openid
#
# # 五：返回qq登录网址的视图
# 5.1准备配置信息在settings中
# QQ_CLIENT_ID="***********"
# QQ_CLIENT_SECRET="&**************8"
# QQ_REDIRECT_URL='http://www.meiduo.site:8080/oauth_callback.html'
#
# class qqauthurlview(view):
#     def get(self,request):
#         """
#         获取qq登录的连接
#         :param request:
#         :return:
#         """
#         next=request.query_params.get("state")
#         if not next:
#             next="/"
#         oauth=oathuqq(client_id=settings.qq_client_id,client_secret=settings.qq_client_serect
#                     redirect_url=qq_redirect_url,state=next)
#         login_url=oauth.get_qq_url()
#         return response({"login_url":login_url})
#
# class qqoauthview(view):
#     def get(self,request):
#         """
#         第三方登录检查
#         :param request:
#         :return:
#         """
#         # 1.获取code的值
#         code=request.query.get("code")
#         # 2.检查参数
#         if not code:
#             return response({"error":"缺少code值"})
#         #3.通过code获取token
#         state="/"
#         qq=oauthqq(client_id=settings.qq_client_id,client_secret=settings.qq_client_secret
#                    redirect_url=settings.qq_redirect_url,state=state)
#         access_token=qq.get_access_token(code=code)
#         openid=qq.get_access_id(access_token=access_token)
#         #判断是否绑定过美多账号
#         try:
#             qq_user=qauthuser.objects.get(openid=openid)
#         except:
#             #未绑定，进入绑定页面，完成绑定
#             tjs=tjs(settings.secret_key,300)
#             open_id=tjs.dumps({"openid":openid}).decode()
#             return resposne({"access_token":open_id})
#         else:
#             #绑定过，则登录成功
#             #生成jwt-token
#             user=qq_user.user
#             jwt_payload_handle=api_settings.jwt_payload_handle
#             jwt_encode_handle=api_settings.jwt_encode_handle
#             payload=jwt_payload_handle(user)
#             token=jwt_encode_handle(payload)
#             response={
#                 "token":token
#                 "usernmae":user.username
#                 "user_id":user.id
#             }
#             return response
#
#
# # 七：使用itsdangerous的使用
# pip intall itsdangeerous
#
# from itsdangerous import timejsonwebsignatureserializer
# from django.conf iimport settings
# serializer=serializer(settings.secret_key,300)
# token=serializer.dumps({"mobile":"1881131516"}).decode()
#
# #检验token
# serializer=serializer(settings.secret_key,300)
# try:
#     data=serializer.loads(tokens)
# except：
#     return none
#
#
# # 八：openid绑定美多商场用户
# 业务逻辑：
# 1.用户需要填写手机号、密码、图片验证码、短信绑定验证码
# 2.如果用户未在美多商场注册过，则会将手机号作为用户名为用户创建一个美多账号,并绑定用户
# 3.如果用户已在美多商场注册过，则检验密码直接绑定用户

from django.db import models
class basemodel(models.Model):
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time=models.DateTimeField(auto_now=True,verbose_name="更新时间")

    class Mete:
        abstract=True

# 创建一个子应用oauth,写models
from django.db import models
from meiduo_mall.utils.models import basemodel
class oauthqquser(basemodel)
    user=models.ForeignKey("users.User", on_delete=models.CASCADE)
    openid=models.CharField(max_length=64,verbose_name="openid",db_indexxTrue)
    weibotoken=models.charfield(max_length=64,verbose_name="weibotokrn")

    class Meta:
        db_table="tb_oauth"
        verbose_name="第三方登录用户数据"
        verbose_name_plural=verbose_name

# qq登陆SDK使用
1.pip install qqlogintool
2.手写官方文档手写一个qq登录sdk

自定义qq登录的SDK
import json
import urllib.parse import urlrncode,parse_qs
import requests
import django.conf import  settings

class oauth(object):
    def __init__(self,client_id=none,client_secret=none,redirect_url=none,state=none):
        self.client_id=client_id
        self.client_secret=client_secret
        self.redirect_url=redirect_url
        self.state=state

    def get_qq_url(self):
        data={
            "response_type":"code"
            "client_id":self.client_id
            "redirect_url":self.redirect_url
            "state":self.state
        }
        qq_url='https://graph.qq.com/oauth2.0/authorize?'+urlencode(data)
        return qq_url

    def get_access_token(self,code):
        data_dict={
            "grant_type":"authorization_code"
            "client_id":"self.client_id"
            "client_secret":self.client_secret
            "code":code
        }
        access_url='https://graph.qq.com/oauth2.0/token?'+urlencode(data_dict)

        # 解析
        try:
            response=requets.get(access_url)
            data=response.text
            data=parse_qs(data)
        except:
            raise Exception("qq请求失败")
        access_token=data.get("access_token")
        return access_token

    def get_open_id(self,access_token):
        url="https://graph.qq.com/oauth2.0/me?access_token=" + access_token
        try:
            response=requests.get(url)
            data=response.text
        except:
            raise exception("qq请求失败")
        try:
            data_dict=json.loads(data)
            openid=data_dict.get("openid")
            return openid

# 上面相当于qqlogintool，只是自己手写的sdk文档，可以直接使用
# 配置文件信息
QQ_CLIENT_ID="*********"
QQ_CLIENT_SECRET="*********"
QQ_REDIRECT_URL="'http://www.meiduo.site:8080/oauth_callback.html'"

# 后端的逻辑实现
class qqauthurlview(view):
    def get(self,request):
        next=request.query_params.get("state")
        if not next:
            next="/"
        oauth=oauthqq(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET
                      ,redirect_url=settings.QQ_REDIRECT_URL,state=next)
        login_utl=get_qq_url(oauth)
        return login_utl

oauth2.0认证
1.准备oauth_callback回调页，用于扫码后接受authorization code
2.通过authorization code 获取access token
3.通过access token获取openid
用户在qq登录时成功后，qq会将用户重定向回我们配置的回调callback网址，本项目中
我们申请的qq登录开发资质时配置的回调地址为：http://www.meiduo.site:8080/oauth_callback.html
我们在front_end_pc目录中新建oauth_callback.html文件，用于接收qq登录成功的
用户回调请求，在该页面中，提供了首次使用qq登录时需要绑定用户身份表单信息


class qqauthullview(view):
    def get(self,request):
        next=request.query_params("state")
        if not next:
            next="/"
        oauth=oauthqq(client_id=settings.QQ_CLIENT_ID,client=settings.QQ_CLIENT_SECRET
                      redirect_url=settings.QQ_REDIRECT_URL,state=next)
        login_url=oauth.get_qq_url()
        return response({"login":login})

class qqauthview(view):
    def get(self,request):
        code=request.query_params("state")
        if not code:
            return response({"error":"缺少code值"})
        state="/"
        qq=oauth(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET
                 ,redirect_url=settings.QQ_REDIRECT_URL.state=state)
        access_token=get_access_token(code=code)
        openid=get_open_id(access_token=access_token)
        try:
            qq_uer=oauthuser.objects.get(openid=openid)
        except:
            # 未绑定进入绑定页面
            tjs=TJS(settings.SECRET_KEY,300)
            access_token=tjs.dump({"access_token":openid})
        else:
            # 已绑定的用户
            user=qq_user.user
            jwt_payload_handle=api_settings.JWT_PAYLOAD_HANDLE
            jwt_encode_handle=api_settings.JWT_ENCODE_HANDLE
            payload=jwt_payload_handle(user)
            token=jwt_encode_handle(payload)
            reponse=Response({
                "token":token
                "username":user.usernmae
                "user_id":user.id
            })

# 补充itsdangeroous的使用
pip install itsdangerous
使用timejsonwebsinatureserializer可以生产带有有效期的token

from itsdangeous import timejsonwebsignatureserializer as tjs
tjs=TJS(settings.SECRET_KEY,300)
access_token=tjs.dumps({"access_token":openid})

# 检验token
tjw=TJW(settings.SECRET_KEY,300)
try:
    data=tjw.loads(access_token)
except:
    return none


# openid绑定美多商场用户
如果是首次使用qq登录，则需要绑定用户
业务逻辑：
用户需要填写手机号，密码，图片验证码，短信验证码
如果用户未在美多商场注册过，则会将手机号作为用户名为用户创建一个美多账号。并绑定用户
如果用户已在美多商场注册过，则检验密码直接绑定用户

import re
from django.conf import settings
from rest_framework_jwt.serializers import serializers
from isdangerous import Timejsonwebsignatureserializer as TJS
from rest_framework_jwt.setting import api_settings
from oauth.models import OauthUser
from models import User
from verifications.views import smscodeview,imagecheckviews

class qqoauthserilizers(serializers.Modelserializer):
    moblie=serializers.CharField(max_length=11)
    sms_code=serializers.CharField(max_length=6,min_length=6,write_only=True)
    access_token=serializers.Charfield(write_only=True)
    token=serializers.CharField(read_only=True)
    user_id=serializers.IntegerField(read_only=True)

    class Meta:
        model=User
        field=('password', 'mobile', 'username', 'sms_code', 'token','access_token', 'user_id')


    def validated_mobile(self,value):
        if not re.match(r"1[3-9]\d{9}",value):
            raise serializers.validationError("手机号格式错误")
        return value
    def validate(self,attrs):
        tjw=TJW(settings.SECRET_KEY,300)
        try:
            data=tjs.loads(attrs["access_token"])
        except:
            raise serializers.ValidationError("无效的token")
        openid=data.get("openid")
        attrs["openid"]=openid
        real_sms_code=smscodeview.checksmscode(attrs["mobile"])
        if not real_sms_code:
            raise serializers.validationError("短信验证失效")
        if attrs["sms_code"]!=real_sms_code:
            raise serializers.validationerror("短信不一致")
        try:
            user=user.objects.get(mobile=attrs["mobile"])
        except:
            return attrs
        else:
            if not user.cjeck_password(attrs["password"]):
                raise serializers.validationerror("密码错误")
            attrs["user"]=user
            return attrs
    def create(self,validated_data):
        user = validated_data.get('user', None)
        if user is None:
            # 创建用户
            user = User.objects.create_user(username=validated_data['mobile'],
                                            password=validated_data['password'],
                                            mobile=validated_data['mobile'])
        # 绑定操作
        OAuthUser.objects.create(user=user, openid=validated_data["openid"])
        # user_id=user.id
        # 生成加密后的token数据
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)  # 生成载荷部分
        token = jwt_encode_handler(payload)  # 生成token

        # user添加token属性
        user.token = token
        user.user_id = user.id

        return user

@method_decorator(login_required,name="dispatch")
class UserInfoView(View):
    """用户中心"""
    def get(self,request):
        return render(request,"user_center_info.html")

@method_decorator(login_required,name="dispatch")
class UserEmailView(View):
    def put(self,request):
        #1.获取json数据
        data=request.body.decode()
        # 2.将json转化为字典
        data_dict=json.loads(data)
        to_email=data_dict["email"]
        #3.验证邮箱的有效性，往用户输入的有效中发送邮件
        #标题  邮件信息内容  用户看到收件人信息 收件人的邮箱 html_message（当标签为html标签使用）
        user=request.user
        tjw=TJW(settings.SECRET_KEY,300)
        token=tjw.dumps({"username":user.username,"email":to_email}).decode()
        verify_url=settings.email_verify_url+"?token=%s"%token
        subject="美多商场邮箱验证"
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
        send_mail(subject, '', settings.EMAIL_FROM, ['SXM_CPP@163.com'], html_message=html_message)

        # 4、更新邮箱
        if not user.is_authenticated:
            return JsonResponse({'code': 4101})
        user.email = to_email
        # save方法必须执行
        user.save()

        return JsonResponse({'code': 0})

from django.shortcuts import render,redirect
from django.views import view
from django.http import JsonResponse
from django.contrib.auth import login
from django.conf import settings
from QQLoginTool.QQtool import OAuthQQ
from oauth.models import OAuthQQUser
from django_redis import get_redis_connection
from users.models import User
from itsdsngerous import TimeJsonwebSignatureSerializer as tjs

class qqloginview(view):
    def get(self,request):
        next=request.GET.get("next")
        if next="/"
    qq=OAuthQQ(client_id=settings.CLIENT_ID,client=settings.CLIENT_SERCRET,
               redirect_uri=settings.QQ_REDIRECT_URL,state=next)
    login_url=qq.get_qq_url()
    return jsonResponse({"login_url":"login_url"})

class QQcallBackview(view):
    code=request.GET.get("code")
    state=request.GET.get("state")
    if code is None state is None:
        return JsonResponse({"error":"缺少数据"})

    qq=qqauth(client_id=settings.QQ_client_id,client_secret=settings.qq_secret,
              redirect_url=settings.qq_redirect_url,state=state)
    try:
        access_token=qq.get_access_token(code)
    except:
        return JsonResponse({"error":"网络错误"})
    try:
        qq_user=oauthqquser.objects.get(openid=openid)
    except:
        tjs=tjs(settings.secrect_key,300)
        tjs.dumps({"openid":"open_id"})
    login(request,qq_user.user)
    response=redirect(state)
    response.set_cookie("username",qq_user.user.user.username)

    def post(self,request):
        data=request.post
        mobile=data.get("mobile")
        mobile=data.get("pwd")
        password=data.get("sms_code")
        openid=data.get("access_token")
        client=get_redis_connection("verify_code")
        real_sms_code=client.get("sms_code_%s"%mobile)
        if real_sms_code is none:
            return render(request,"oau_callback")
        if real_sms_code.decode()!=sms_code:
            return render(request,"oauth_callback.html")
        tjs=TJS(settings.SERCRET_KEY,300)
        try:
           user=User.objeces.get(mobile=mobile)
           if not user.check_password(password):
               return render(request,"oauth_callback.html")
        except:
            tjs=TJS(settings.SECRET_KEY)

        try:
           data = tjs.loads(openid)
        except:
            return render(request,"oauth_callback.html")
        openid = data.get('openid')
        OAuthQQUser.objects.create(openid=openid, user=user)
        return redirect('/')