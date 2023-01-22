from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from auusers import views

urlpatterns = [
    path('code/', csrf_exempt(views.GetCode.as_view()), name='get-code'),
    path('get/one-id/access-token/', csrf_exempt(views.GetOneIdAccessToken.as_view()), name='access-token'),
    path('get/user-info-from/one-id/', csrf_exempt(views.GetUserInfoFromOneId.as_view()), name='user-info'),
    path('logout-from-one-id/', csrf_exempt(views.LogoutFromOneId.as_view()), name='logout'),
]
