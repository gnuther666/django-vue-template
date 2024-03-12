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
from app.views.login.login_view import CustomTokenObtainPairView
from app.views.login.captcha_view import get_captcha
from app.views.example.example_view import ExampleViewset, ExampleLoginedViewset
from django.conf import settings
from django.conf.urls.static import static

router = routers.SimpleRouter()
router.register(r'example', ExampleViewset)
router.register(r'example_logined', ExampleLoginedViewset)

urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/api/', include(router.urls)),
    path('backend/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('backend/captcha/', get_captcha),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
