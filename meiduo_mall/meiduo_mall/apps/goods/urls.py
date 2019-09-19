from django.conf.urls import url
from . import views

urlpatterns=[
    #列表页数据渲染
    url(r"^list/(?P<categorie_id>\d+)/(?P<page_num>\d+)/$",views.GoodsListView.as_view()),
    #获取热销商品
    url(r"^hot/(?P<categorie_id>\d+)/$",views.GoodsHotView.as_view()),
    url(r"^search/$",views.GoodsSearchView.as_view()),
    # 详情页渲染
    url(r'detail/(?P<pk>\d+)/$', views.GoodsDetailView.as_view()),
    # 商品分类访问量记录
    url(r'detail/visit/(?P<pk>\d+)/$', views.GoodsVisitView.as_view()),
    # 用户浏览历史记录
    url(r'browse_histories/$', views.GoodsHistoryView.as_view()),
]