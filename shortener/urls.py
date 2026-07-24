from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/shorten/', views.URLCreateAPIView.as_view(), name='shorten'),
    path('<str:short_code>/', views.redirect_view, name='redirect'),
]
