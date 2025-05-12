from django.urls import path
from account import views

app_name = 'account'


urlpatterns = [
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('users/<int:telegram_id>/', views.GetUserAPIView.as_view(), name='get-user'),
    path('users/add/', views.UserCreateAPIView.as_view(), name="users-add"),
    path('users/check-phone/', views.UserCheckPhoneAPIView.as_view(), name='check-phone'),
    path("users/update_phone/", views.UpdateUserPhoneLanguageView.as_view(), name="update_phone"),
    path("users/update_link/", views.UpdateUserLinkView.as_view(), name="update_link"),
]