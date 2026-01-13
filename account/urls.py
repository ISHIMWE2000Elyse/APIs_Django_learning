from django.urls import path, include
from rest_framework import routers
from account.views import UserViewsets, LoginMixin
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


r=routers.DefaultRouter()
r.register('user',UserViewsets)
r.register('login',LoginMixin,basename="auth")

urlpatterns = [
    path("", include(r.urls)),
]
