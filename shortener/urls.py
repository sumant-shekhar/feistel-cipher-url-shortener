from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/shorten/', views.URLCreateAPIView.as_view(), name='api-shorten'),
    path('<str:short_code>/', views.redirect_view, name='redirect'),
]
