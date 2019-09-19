from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from collections import OrderedDict
from contents.utils import get_categories
from contents.models import ContentCategory
from goods.models import SKU

class ImageView(View):
    def get(self,request):
        skus=SKU.objects.all()
        skus_list=[]
        for sku in skus:
            skus_list.append({
                "img_url":sku.default_image.url
            })
        return render(request,"img.html",{"skus":skus_list})

class IndexView(View):
    "首页广告"
    # def get(self,request):
    #     "提供首页广告界面"
    #     #查询商品频道和分类
    #     categories=get_categories()
    #
    #    #广告数据
    #     contents={}
    #     content_categories=ContentCategory.objects.all()
    #     for cat in content_categories:
    #         contents[cat.key]=cat.content_set.filter(status=True).order_by("sequence")
    #
    #     #渲染模板的上下文
    #     context={
    #         "categories":categories,
    #         "contents":contents
    #     }
    #     return render(request,"index.html",context)
    def get(self,request):
        return redirect("/static/index.html")