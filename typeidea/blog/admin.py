from django.contrib import admin
# Register your models here.
from .models import Post,Category,Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry

#使在分类列表中也能够编辑文章的内容
class PostInline(admin.TabularInline):
    fields=('title','desc')   #设置可编辑的字段
    extra = 1
    model = Post   #Post文章类


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""
    title='分类过滤器'
    parameter_name='owner_category'

    def lookups(self,request,model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self,request,queryset):
        category_id=self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):#admin.ModelAdmin
    form=PostAdminForm  #将文章描述字段改成textarea组件
    list_display=[
        'title','category','status',
        'created_time','operator','owner',
    ]
    list_display_links=[]
    list_filter=[CategoryOwnerFilter,]

    search_fields=['title','category__name']

    actions_on_top = True  #默认值为True
    actions_on_bottom = True  #默认值为False

    save_on_top = True
    exclude=['owner']
    # fields=(
    #     ('category','title'),
    #     # 'category',
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    #     )
    filter_vertical=('tag',)
    fieldsets=(
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title','category'),
                'status',
                ),
            }),
        ('内容',{
            'fields':(
                'desc',
                'content',
                ),
            }
            ),
        ('额外信息',{
            'classes':('collapse',), #给配置的板块加CSS元素
            'fields':('tag',),

            }
            )
    )


    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change',args=(obj.id,))
            )
    operator.short_description='操作'

#新增之后，设置默认owner为当前登录账户
    def save_model(self,request,obj,form,change):
        obj.owner = request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)
#设置查看权限，登录账户只能查看自己创建的文章
    def get_queryset(self,request):
        qs=super(PostAdmin,self).get_queryset(request) #父类对象，传入的参数是当前的request,所有展示数据的集合
        return qs.filter(owner=request.user)


    # class Media:
    #     css={
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #         }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)
        



@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):#admin.ModelAdmin
    inlines=[PostInline,]
    list_display=('name','status','is_nav','created_time','post_count',)
    fields=('name','status','is_nav')


    # def save_model(self,request,obj,form,change):
    #     obj.owner=request.user
    #     return super(CategoryAdmin,self).save_model(request,obj,form,change)

    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description='文章数量'

@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display=('name','status','created_time')
    fields=('name','status')

    def save_model(self,request,obj,form,change):
        obj.owner=request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)

@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display=['object_repr','object_id','action_flag','user','change_message']
