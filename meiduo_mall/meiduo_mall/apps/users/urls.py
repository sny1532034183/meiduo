from django.conf.urls import url

from . import views

urlpatterns = [
    # 首页处理

    url(r'^register/$', views.UserRegisterView.as_view()),
    url(r"^login/$", views.LoginView.as_view()),
    url(r"^logout/$", views.LogoutView.as_view()),
    url(r"^info/$", views.UserInfoView.as_view()),
    url(r'^emails/$', views.UserEmailView.as_view()),
    url(r"^password/$",views.ChangePasswordView.as_view()),
    url(r"find_password/$",views.FindPwdView.as_view()),
    # 找回密码第三步，修改密码
    # url('^users/(?P<user_id>\d+)/password/$', views.ChangePwdView.as_view()),


]
