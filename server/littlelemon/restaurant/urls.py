from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
urlpatterns = [
    path('menu/',views.MenuItemsView.as_view()),
    path('menu/<int:pk>',views.SingleMenuItemView.as_view()),
]