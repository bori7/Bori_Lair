"""webnew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('GPACALC/', views.GPAcalc, name = 'GPAcal'),
    path('GPAresult/', views.GPAresult, name = 'GPAcalresult'),
    path('signup/', views.signup, name = 'signup'),
    path('loggedin/', views.loggedin, name = 'loggedin'),
    path('forgotpasword/', views.forgotpassword, name = 'forgotpassword'),
    path('D&W/', views.DandW, name = 'DandW'),
    path('About_D&W/', views.aboutDandW, name = 'aboutDandW'),
    path('CompPlay/', views.CompPlay, name = 'CompPlay'),
    path('secret1/', views.secret_1, name = 'secret1'),
    path('secret2/', views.secret_2, name = 'secret2'),
    path('winner/', views.winner, name = 'winner'),
    path('giveup/', views.giveup, name = 'giveup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

