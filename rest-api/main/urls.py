from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('rules/', views.RulestView.as_view(), name='rules'),
]