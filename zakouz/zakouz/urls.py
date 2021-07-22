"""djrest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from .api import router
from django.views.decorators.csrf import csrf_exempt
from knox import views as knox_views
from api import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # path('images/',csrf_exempt(views.imageUpload),name='image_upload'),
    path('admin/', admin.site.urls),
    # path('api-token-auth/', views.obtain_auth_token),
    path('register/', views.RegisterAPI.as_view(),name='register'),
    # path('',include('api.url')),
    path('',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)