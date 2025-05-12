from django.urls import path
from shop import views

app_name = 'shop'


urlpatterns = [
    path('shops/check-link/', views.ShopCheckLinkAPIView.as_view(), name='check-link'),
    path('shops/shop-add/', views.ShopCreateAPIView.as_view(), name='shop-add')
]