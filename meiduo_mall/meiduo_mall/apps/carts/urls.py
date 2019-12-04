from django.conf.urls import url
from . import views
urlpatterns=[
    url(r"^carts/$",views.CartView.as_view()),
    url(r"^carts/selection/$",views.CartSelectionView.as_view()),
    url(r"^carts/simple/$",views.CartSimpleView.as_view())
]