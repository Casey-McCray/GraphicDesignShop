from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='site-home'),
    path('work/', views.work, name='work'),
    path('register/', views.register, name='register'),
    path('order/new/', views.NewOrder.as_view(), name='new-order'),
    path('order/new/success/', views.order_success, name='order-success'),
    path('orders/', views.orders, name='orders'),
    path('order/<int:pk>/deadline/', views.deadline_update.as_view(), name='deadline-update'),
    path('order/<int:pk>/amount/', views.amount_update.as_view(), name='amount-update'),
    path('order/<int:pk>/amount-get/', views.get_amount.as_view(), name='get-amount'),
    path('purchase/', views.purchase, name='purchase'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
] 