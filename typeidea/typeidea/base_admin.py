from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用来自动补充文章分类标签；侧边栏 友联这些model的owner字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude=('owner',)

    #新增之后，设置默认owner为当前登录账户
    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)
#设置查看权限，登录账户只能查看自己创建的文章
    def get_queryset(self,request):
        qs=super(BaseOwnerAdmin,self).get_queryset(request) #父类对象，传入的参数是当前的request,所有展示数据的集合
        return qs.filter(owner=request.user)
