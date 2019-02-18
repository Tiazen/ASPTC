"""ascpt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from asp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('gettasklist/', views.gettasklist),
    path('getclasslist/', views.getclasslist),
    path('regist/', views.registuser),
    path('login/', views.login),
    path('logout/', views.logout),
    path('addtask/', views.addtask),
    path('edittask/', views.edittask),
    path('search/', views.searchlist),
    path('stats/', views.stat),
    path('settings/', views.returnsettings),
    path('updatethemes/', views.updatethemes),
    path('tasktheme/', views.tasktheme),
    path('loadfile/', views.saveFile),
    path('deletetask', views.deleteTask),
    path('getcode/', views.getcode),
    path('gettests/', views.gettests),
    path('profile/', views.profile),
    path('changepass/', views.changepass),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)