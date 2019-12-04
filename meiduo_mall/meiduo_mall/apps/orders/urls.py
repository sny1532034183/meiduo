from . import views
from django.conf.urls import url
urlpatterns=[
    url(r"orders/settlement/$",views.OrderView.as_view()),
    # 保存订单
    url(r'^orders/commit/$', views.OrderCommitView.as_view()),
    # 获取订单成功页面
    url(r'^orders/success/$', views.OrderSuccessView.as_view()),
    # 用户中心获取当前用户的订单信息
    url(r'^orders/info/(?P<pk>\d+)/$', views.OrderInfoView.as_view()),
]