from django.urls import path
from . import views

urlpatterns = [
    path('', views.URLCreateAPIView.as_view()),
    path('<str:short_code>/', views.redirect_view),
]
