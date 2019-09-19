from django.conf.urls import url
from . import views

urlpatterns=[
    url("^qq/login/$",views.QQLoginView.as_view()),
    url(r'^oauth_callback/$', views.QQCallBackView.as_view())
]