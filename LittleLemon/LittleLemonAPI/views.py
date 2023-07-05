from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from LittleLemonAPI.models import Cart, MenuItem, Category, Order, OrderItem
from LittleLemonAPI.permissions import IsManagerUser, IsCustomerUser, IsDeliveryUser, IsManagerOrDeliveryUser, \
    IsManagerOrDeliveryOrCustomerUser
from LittleLemonAPI.serializers import UserSerializer, CartSerializer, MenuItemSerializer, CategorySerializer, \
    OrderSerializer, OrderItemSerializer
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class ManagerUserView(ListCreateAPIView, DestroyAPIView):
    permission_classes = (IsManagerUser,)
    pagination_class = PageNumberPagination
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        managers = Group.objects.get()
        return User.objects.filter(groups=managers).order_by('id')

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        try:
            user = get_object_or_404(User, username=username)
            user.groups.add(Group.objects.get())
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return Response({"message": f'{username} is added to the manager group'}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"message": "Username doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        try:
            user = get_object_or_404(User, id=user_id)
            user.groups.remove(Group.objects.get())
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return Response({"message": f'User with ID {user_id} is removed from the manager group'},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class DeliveryCrewUserView(ListCreateAPIView, DestroyAPIView):
    permission_classes = (IsManagerUser,)
    pagination_class = PageNumberPagination
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        delivery_crew = Group.objects.get(name="delivery_crew")
        return User.objects.filter(groups=delivery_crew).order_by('id')

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        try:
            user = get_object_or_404(User, username=username)
            user.groups.add(Group.objects.get(name="delivery_crew"))
            return Response({"message": f'{username} is added to the delivery crew group'},
                            status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"message": "Username doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        try:
            user = get_object_or_404(User, id=user_id)
            user.groups.remove(Group.objects.get())
            return Response({"message": f'User with ID {user_id} is removed from the delivery crew group'},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class CartView(ListCreateAPIView, DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]
    authentication_classes = [TokenAuthentication]
    # permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    model = Cart
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Cart.objects.filter(user=user).order_by('id')
        else:
            return Cart.objects.none()

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['user'] = user.id
        serializer = CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    def get_permissions(self):
        if self.request.method in ("POST", "PATCH", "PUT", "DELETE"):
            return [IsManagerUser(), IsAdminUser()]
        return [AllowAny()]


class MenuItemView(ListCreateAPIView):
    queryset = MenuItem.objects.all().order_by('id')
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['price', 'category']
    search_fields = ['title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsManagerUser()]
        return [AllowAny()]


class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    model = MenuItem
    queryset = MenuItem.objects.all()
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]

    def get_permissions(self):
        if self.request.method in ("PATCH", "PUT", "DELETE"):
            return [IsManagerUser(), IsAdminUser()]
        return [AllowAny()]


class OrderListCreateAPIView(ListCreateAPIView):
    model = Order
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ]
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomerUser()]
        elif self.request.method == "GET":
            return [IsManagerOrDeliveryOrCustomerUser()]
        else:
            return []

    def get_queryset(self):
        user = self.request.user
        if IsCustomerUser().has_permission(self.request, self):
            return Order.objects.filter(user=user).order_by('id')
        elif IsManagerUser().has_permission(self.request, self):
            return Order.objects.all()
        elif IsDeliveryUser().has_permission(self.request, self):
            return Order.objects.filter(delivery_crew=user).order_by('id')
        else:
            return Order.objects.none()

    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user).all()
        order = Order.objects.create(user=user)
        order_items = []
        total = 0
        for item in cart_items:
            order_items.append(
                OrderItem(
                    menu_item=item.menu_item,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    price=item.price,
                    order=order
                )
            )
            total += item.price

        # total = sum(item.price for item in order_items)
        order.total = total
        order_items = OrderItem.objects.bulk_create(order_items)
        order.status = False
        order = order.save()

        items_serializer = OrderItemSerializer(order_items, many=True)
        order_serializer = OrderSerializer(order)

        return Response({
            "order_details": order_serializer.data,
            "order_items": items_serializer.data
        }, status=status.HTTP_201_CREATED)


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    model = Order
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    throttle_classes = (AnonRateThrottle, UserRateThrottle,)

    def get_queryset(self):
        if IsCustomerUser().has_permission(self.request, self):
            return Order.objects.filter(user=self.request.user).order_by('id')
        elif IsManagerUser().has_permission(self.request, self) or IsDeliveryUser().has_permission(self.request, self):
            return Order.objects.all()
        else:
            return Order.objects.none()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "PATCH":
            return [IsManagerOrDeliveryUser()]
        elif self.request.method in ("PUT", "DELETE"):
            return [IsAuthenticated(), IsManagerUser()]
        else:
            return []

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if IsDeliveryUser().has_permission(request, self):
            # Delivery crew can update the order status only
            statu = request.data.get('status')
            if statu is not None:
                instance.status = statu
            else:
                return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        elif IsManagerUser().has_permission(request, self):
            # Manager can update delivery crew and order status
            stat = request.data.get('status')
            delivery_crew_id = request.data.get('delivery_crew')
            if delivery_crew_id:
                try:
                    delivery_crew = User.objects.get(id=delivery_crew_id)
                    instance.delivery_crew = delivery_crew
                except User.DoesNotExist:
                    return Response({'detail': 'Invalid delivery crew.'}, status=status.HTTP_400_BAD_REQUEST)
            if stat is not None:
                instance.status = stat
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
