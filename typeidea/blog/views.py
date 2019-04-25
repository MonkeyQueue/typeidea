from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import  Post,Tag,Category
from config.models import SideBar

def post_list(request,category_id=None,tag_id=None):
    # content='post_list category_id={category_id},tag_id={tag_id}'.format(
    #     category_id=category_id,
    #     tag_id=tag_id,
    #     )
    # return HttpResponse(content)

    # return render(request,'blog/list.html',context={'name':'post_list'})
    tag=None
    category=None
    # post_list=Post.objects.filter(status=Post.STATUS_NORMAL)

    # if tag_id:
    #     try:
    #         tag=Tag.objects.get(id=tag_id)
    #     except:
            
    #         post_list=[]
    #     else:
            
    #         post_list=tag.post_set.filter(status=Post.STATUS_NORMAL) #得到的是Post的一个实例对象，多对多关系，一对多关系逆向查询用到_set.all()
    # else:
    #     # post_list=Post.objects.filter(status=Post.STATUS_NORMAL)
    #     # if category_id:
    #     #     post_list=post_list.filter(category_id=category_id)
    #     pass
    # context={
    #     'tag':tag,
    #     'post_list':post_list,
    # }
    # # return render(request,'blog/list.html',context={'post_list':post_list})
    #使用以上代码，不论是首页（文章列表页），还是分类页，还是标签页，显示的都是首页的格式，不能凸显出来分类和标签的意思
    #一下作修改，使能够分别显示
    # else:
    #     post_list=Post.objects.filter(status=Post.STATUS_NORMAL)
    #     if category_id:
    #         try:
    #             category = Category.objects.get(id=category_id)
    #         except Category.DoesNotExist:
    #             category = None
    #         else:
    #             post_list = post_list.filter(category_id=category_id)
    # context={
    #         'category':category,
    #         'tag':tag,
    #         'post_list':post_list,
        
    # }
    #以上方法可以正常实现效果
    #     if category_id:
    # elif category_id:
    #     try:
    #         category=Category.objects.get(id=category_id)
    #     except CategoryNotExist:
    #         post_list=[]
    #     else:
    #         post_list=category.post_set.filter(status=Post.STATUS_NORMAL)
    # context={
    #         'category':category,
    #         'tag':tag,
    #         'post_list':post_list,
    #         }
    if tag_id:
        post_list,tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list,category = Post.get_by_category(category_id)
    else:
        post_list=Post.latest_posts()
        # post_list=Post.objects.filter(status=Post.STATUS_NORMAL)

    context={
        'category':category,
        'tag':tag,
        'post_list':post_list,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request,'blog/list.html',context=context)



def post_detail(request,post_id=None):
    # return HttpResponse('detail')
    # return render(request,'blog/detail.html',context={'name':'post_detail'})
    try:
        post=Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post=None

    context={
        'post':post,
    }
    context.update(Category.get_navs())
    return render(request,'blog/detail.html',context=context)