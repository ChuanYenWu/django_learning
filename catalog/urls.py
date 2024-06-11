from django.urls import path
from catalog import views

urlpatterns = [
     path('', views.index, name='index'),
     path('lunchboxs/', views.LunchboxListView.as_view(), name='lunchboxs'),
     path('lunchbox/<int:pk>', views.LunchboxDetailView.as_view(), name='lunchbox-detail'),
     path('orderlist/', views.BuyingListView.as_view(), name='orderlist'),  #staff view: all order
]
urlpatterns += [
    path('neworder/', views.neworder, name='neworder'),
    path('checkorder/', views.checkorder, name='checkorder'),
    path('order_result/', views.order_result, name='order_result'),
]