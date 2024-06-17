"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from app.views.SystemMenu.sys_menu_view import SysMenuViewset

from app.views.login.login_view import CustomTokenObtainPairView, CustomTokenRefreshView
from app.views.login.captcha_view import get_captcha
from app.views.example.example_view import ExampleViewset, ExampleLoginedViewset
from django.conf import settings
from django.conf.urls.static import static
from notebook.views.book import UserBookViewset
from notebook.views.book_toc import BookTocViewset
from notebook.views.doc import BookDocViewset

router = routers.SimpleRouter()
router.register(r'example', ExampleViewset)
router.register(r'example_logined', ExampleLoginedViewset)
router.register(r'notebook', UserBookViewset)
router.register(r'notebook_toc', BookTocViewset)
router.register(r'notebook_doc', BookDocViewset)
router.register(r'sys_menu', SysMenuViewset)


urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/api/', include(router.urls), name='api'),
    path('backend/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('backend/refresh_token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('backend/captcha/', get_captcha),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
