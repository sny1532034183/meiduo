import os

from django.conf import settings
from django.shortcuts import render
from django.template import loader
from contents.models import ContentCategory
from contents.utils import get_categories
import time
from goods.models import SKU,GoodsCategory,SKUSpecification

def get_index_static():
    "生成静态的主页html文件"
    print("%s:generate_static_index_html"%time.ctime())
    #获取商品频道和分类
    categories=get_categories()
    #广告内容
    contents={}
    content_categories=ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key]=cat.content_set.filter(status=True).order_by("sequence")
        #渲染模板
    context={
        "categories":categories,
        "contents":contents,
    }
    #获取首页模板文件
    template=loader.get_template("index.html")
    #渲染首页html字符串
    html_text=template.render(context)
    #将首页html字符串写入指定目录，命名“index.html”
    file_path=os.path.join(settings.STATICFILES_DIRS[0],"index.html")
    print(file_path)
    with open(file_path,"w",encoding="utf-8")as f:
        f.write(html_text)

def get_detail_static(pk):
    categories=get_categories()
    #2.面包屑导航
    try:
        sku=SKU.objects.get(id=pk)
    except:
        return None
    cat3=GoodsCategory.objects.get(id=sku.category.id)
    cat2=cat3.parent
    cat1=cat2.parent
    #一级分类指定url路径
    cat1.url=cat1.goodschannel_set.filter()[0].url
    breadcrumb={}
    breadcrumb["cat1"]=cat1
    breadcrumb["cat2"]=cat2
    breadcrumb["cat3"]=cat3
    #3.规格和选项参数
    #3.1通过spu商品获取当前商品的规格数据
    spu=sku.spu
    specs=spu.specs.all()
    #3.2给规定指定规格选项
    for spec in specs:
        #遍历所有规格的option规格
        spec.option_list=spec.options.all()
        #遍历每个option选项
        for option in spec.option_list:
            # 判断遍历的这个选项是当前商品的选项
            if option.id==SKUSpecification.objects.get(sku=sku,spec=spec).option_id:
                option.sku_id=sku.id

            else:
                # 遍历的这个选项不是当前商品的选项,其他商品存在这个option
                other_good=SKU.objects.filter(specs__option_id=option.id)
                #查询当前商品的其他规格
                sku_specs=SKUSpecification.objects.filter(sku=sku).exclude(sku=sku,spec=spec)
                #获取其他规格的规格选项
                option_list=[]
                for sku_spec in sku_specs:
                    option_id=sku_spec.option_id
                    option_list.append(option_id)
                other_good1=SKU.objects.filter(specs__option_id__in=option_list)
                good=other_good&other_good1
                option.sku_id=good[0].id
    data={
        "categories":categories,
        "breadcrumb":breadcrumb,
        "sku":sku,
        "spu":spu,
        "category_id":sku.category.id,
        "specs":specs,
    }
    #调用模板渲染数据
    template=loader.get_template("detail.html")
    html_text=template.render(data)
    file_path=os.path.join(settings.BASE_DIR,'static/detail/%s.html' % pk)

    with open(file_path,"w",encoding="utf-8")as f:
        f.write(html_text)
