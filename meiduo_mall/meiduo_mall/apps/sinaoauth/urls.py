from django.conf.urls import url
from . import views
urlpatterns=[
    url(r"sina/login/$",views.WeiboAuthURLLView.as_view()),
    url(r"sinaoauthcallback/$",views.WeiboCallbackView.as_view()),

]