from django.contrib import admin

# Register your models here.
from .models import Link,SideBar
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

@admin.register(Link,site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display=('title','href','status','weight','owner','created_time')
    fields = ('title','href','status','weight','owner')

    def save_model(self,request,obj,form,change):
        obj.owner=request.user
        return super(LinkAdmin,self).save_model(request,obj,form,change)

@admin.register(SideBar,site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display=('title','display_type','status','content','owner','created_time')
    fields=('title','display_type','status','content','owner')

    def save_model(self,request,obj,form,change):
        obj.owner=request.user
        return super(LinkAdmin,self).save_model(request,obj,form,change)
