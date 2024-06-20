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
urlpatterns += [
    path('order/<uuid:uuid>/update', views.update_orderview_staff, name='updateorder_staff'),
    path('order/<uuid:uuid>/delete', views.delete_orderview_staff, name='deleteorder_staff'),
]
urlpatterns += [
    path('order/<uuid:uuid>/update/customer', views.update_orderview_customer, name='updateorder_customer'),
]