from django.conf.urls import url
from . import  views
urlpatterns=[
    url(r'^index/$', views.IndexView.as_view()),
    # url("^img/$",views.ImageView.as_view())
]