from django.urls import path
from auusers import views

urlpatterns = [
    path('code/', views.get_code, name='get_code'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]
