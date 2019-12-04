from . import views
from django.conf.urls import url

urlpatterns=[
    #获取地址页面
    url(r"addresses/$",views.AddressView.as_view()),
    #获取省信息
    url(r"areas/$",views.AreasView.as_view()),
    #保存收货地址
    url(r"addresses/create/$",views.AddressCreateView.as_view()),
    #修改收货地址
    url(r"addresses/(?P<pk>\d+)/$",views.AddressCreateView.as_view()),
    #设置默认地址
    url(r"addresses/(?P<address_id>\d+)/default/$",views.AddressDefaultView.as_view()),
    #修改标题
    url(r"addresses/(?P<address_id>\d+)/title/$",views.AddressTitleView.as_view())
]