from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, viewsets, permissions
from .serializers import *
from .models import *
# Create your views here.

class MenuItemsView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
