"""configurations URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings,urls   
# from django.conf.urls import url   
from django.conf.urls.static import static
from sitepanel.urls import router as AppRouter
from administrator.urls import router as AdminRouter
from django.shortcuts import render
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Survey API')
    

urlpatterns = [
    # url(r'^$', schema_view),
    path('administrator/', admin.site.urls),
    path('api/admin/', include(AdminRouter.urls)),
    path('api/admin/', include('administrator.urls')),
    path('api/user/', include(AppRouter.urls)),
    path('api/user/', include('sitepanel.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)