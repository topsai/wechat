"""wechat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework import routers
from back import views
from wechat.settings import MEDIA_ROOT
from django.views.static import serve

# from rest_framework.authtoken import views
# from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt.views import token_obtain_pair
from rest_framework_simplejwt import views as JWTAuthenticationViews

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'article', views.ArticleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('login/', views.login),
    url('', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^jwt_auth/', token_obtain_pair),
    path('api/token/', JWTAuthenticationViews.TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', JWTAuthenticationViews.TokenRefreshView.as_view(), name='refresh_token'),

]
