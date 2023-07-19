from django.urls import path
from . import views

urlpatterns = [
    path('groups/manager/users/', views.ManagerUserView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerUserView.as_view()),
    path('groups/delivery-crew/users/', views.DeliveryCrewUserView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewUserView.as_view()),

    path('cart/menu-items', views.CartView.as_view()),

    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>', views.CategoryView.as_view()),

    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),

    # orders endpoints
    path('orders/', views.OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    # path('orders/delivery-crew/     ', views.AssignedOrderListView.as_view(), name='assigned-order-list'),
    # path('orders/delivery-crew/<int:pk>', views.AssignedOrderUpdateView.as_view(), name='assigned-order-update'),
]
