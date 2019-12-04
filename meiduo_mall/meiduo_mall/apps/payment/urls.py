from .import views
from django.conf.urls import url
urlpatterns=[
    url(r"payment/(?P<order_id>\d+)/$",views.PayMentView.as_view()),
    # 保存支付结果
    url(r'^payment/status/$', views.PayMentStatusView.as_view()),
]