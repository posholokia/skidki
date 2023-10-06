from django.urls import path
from rest_framework import routers
from .api import *


router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('request', RequestViewSet)

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('brands/', BrandList.as_view()),
    path('shops/', ShopList.as_view()),
    path('product-history/', ProductHistoryList.as_view()),
    path('notifications/', NotificationsList.as_view()),
]
urlpatterns += router.urls
