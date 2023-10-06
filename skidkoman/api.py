from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics
from .serializers import (CategorySerializer,
                          BrandSerializer,
                          ShopSerializer,
                          ProductSerializer,
                          ProductHistorySerializer,
                          RequestSerializer,
                          NotificationsSerializer,
                          )
from .models import (Category,
                     Brand,
                     Shop,
                     Product,
                     ProductHistory,
                     Request,
                     Notifications)

User = get_user_model()


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'name',
    ]


class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'name',
    ]


class ShopList(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'name',
    ]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    http_method_names = ['get']
    filterset_fields = [
        'title',
        'shop',
        'old_price',
        'current_price',
        'url',
        'brand',
        'category',
        'click_rate',
    ]


class ProductHistoryList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ProductHistory.objects.all()
    serializer_class = ProductHistorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        url = self.request.GET.get('url', None)
        queryset = queryset.filter(product_id__url=url).order_by('last_updated')

        if isinstance(user, User):
            return queryset

        return queryset[0:3]


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'endpoint',
        'price',
        'discount',
        'created_at',
        'completed_at',
        'period_date',
        'status',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class NotificationsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'request',
        'created_at',
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(request__user=self.request.user)
        return queryset
