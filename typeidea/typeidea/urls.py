"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog.views import post_list,post_detail
from config.views import links

from typeidea.custom_site import custom_site

urlpatterns = [
    url(r'^$',post_list,name='index'),
    url(r'^category/(?P<category_id>\d+)/$',post_list,name='category_list'),
    url(r'^tag/(?P<tag_id>\d+)/$',post_list,name='tag_list'),
    url(r'^post/(?P<post_id>\d+).html$',post_detail,name='post_detail'),
    url(r'^links/$',links,name='links'),
    url(r'^super_admin/',admin.site.urls,name='super_admin'),
    url(r'^admin/',custom_site.urls,name='admin'), #定制site，关联custom_site.py文件
    # url(r'^blog/',include('blog.urls'),name='blog'),
]


