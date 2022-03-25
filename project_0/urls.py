"""project_0 URL Configuration

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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from django.urls import path, re_path, include
from django.views.static import serve

# from test import settings
from test import views as test_views


urlpatterns = [
    path(r'admin/', admin.site.urls), 
    path(r'index/', test_views.index_page), 
    path(r'show_word_info/', test_views.show_word_info_page), 
    path(r'passage/', test_views.select_words_page), 
    path(r'passage/show_definition/', test_views.show_definition_page), 
    path(r'passage/submit_selected_words/', test_views.test_passage_page), 

    path(r'i18n/', include('django.conf.urls.i18n')),
]



