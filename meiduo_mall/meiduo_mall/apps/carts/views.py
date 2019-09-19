from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django_redis import get_redis_connection
import json, pickle, base64
from goods.models import SKU


# Create your views here.
class CartView(View):
    def post(self, request):
        """
            保存购物车数据
        :param request:
        :return:
        """
        # 1、获取前端数据 请求中
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2、验证数据
        sku_id = data_dict.get('sku_id')
        count = data_dict.get('count')
        selected = True
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({"error": '商品不存在'}, status=400)
        if int(count) > sku.stock:
            return JsonResponse({"error": '库存不足'}, status=400)
        # 3、保存数据
        # 3-1判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 3-2登录用户 保存在redis
            client = get_redis_connection('carts')
            # 3-3保存sku_id和count hash
            # client.hset('carts_%s' % user.id, sku_id, count)
            # hincrby可以累加数据
            client.hincrby('carts_%s' % user.id, sku_id, count)
            if selected:
                # 3-4保存选中状态 商品id在集合说明商品处于选中状态
                client.sadd('carts_selected_%d' % user.id, sku_id)
            # 3-5 返回结果
            return JsonResponse({'code': '0'})
        else:
            # 未登录用户 保存在cookie
            # 先获取cookie数据，判断用户是否保存过
            cart_cookie = request.COOKIES.get('cart_cookie')
            if cart_cookie:
                # 有数据 解密
                data_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                data_dict = {}

            # 提取转化后的字典数据
            """
                { sku_id:{'count':10,selected:True}}
            """
            sku_data = data_dict.get(sku_id)
            if sku_data:
                # 如果存在能够获取sku_id数据，说明以前存储过 累加购买数量
                count += sku_data['count']
            # 将新数据写入字典
            data_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            # 将字典加密
            cart_cookie = base64.b64encode(pickle.dumps(data_dict)).decode()
            # 写入cookie
            response = JsonResponse({'code': 0})
            response.set_cookie('cart_cookie', cart_cookie, 60 * 60 * 2)
            return response

    def get(self, request):

        user = request.user
        if user.is_authenticated:
            # 3-2登录用户 保存在redis
            client = get_redis_connection('carts')
            # 3-3获取sku_id和count hash
            # client.hset('carts_%s' % user.id, sku_id, count)
            sku_id_count = client.hgetall('carts_%s' % user.id)
            # 3-4获取选中状态的ku_id
            sku_id_selected = client.smembers('carts_selected_%d' % user.id)
            data_dict={}
            for sku_id,count in sku_id_count.items():
                data_dict[int(sku_id)]={
                    'count':int(count),
                    'selected':sku_id in sku_id_selected
                }
        else:
            # 未登录用户 保存在cookie
            # 先获取cookie数据，判断用户是否保存过
            cart_cookie = request.COOKIES.get('cart_cookie')
            if cart_cookie:
                # 有数据 解密
                data_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                data_dict = {}


        # 获取所有商品的key
        sku_keys = data_dict.keys()
        skus = SKU.objects.filter(id__in=sku_keys)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'price': str(sku.price),
                'caption': sku.caption,
                'count': data_dict[sku.id]['count'],
                'selected': str(data_dict[sku.id]['selected']),
                'default_image_url': sku.default_image.url
            })

        return render(request,'cart.html',{'cart_skus':cart_skus})

    def put(self, request):
        """
            更新购物车数据
        :param request:
        :return:
        """
        # 1、获取前端数据 请求中
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2、验证数据
        sku_id = data_dict.get('sku_id')
        count = data_dict.get('count')
        selected = data_dict.get('selected')
        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({"error": '商品不存在'}, status=400)
        if int(count) > sku.stock:
            return JsonResponse({"error": '库存不足'}, status=400)
        # 3、保存数据
        # 3-1判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 3-2登录用户 更新在redis
            client = get_redis_connection('carts')
            # 3-3更新sku_id和count hash
            client.hset('carts_%s' % user.id, sku_id, count)
            # hincrby可以累加数据
            # client.hincrby('carts_%s' % user.id, sku_id, count)
            if selected:
                # 3-4保存选中状态 商品id在集合说明商品处于选中状态
                client.sadd('carts_selected_%d' % user.id, sku_id)
            else:
                # 未选中 ，从集合中删除
                client.srem('carts_selected_%d' % user.id, sku_id)
            # 3-5 返回结果
            cart_sku = {
                'id': sku.id,
                'name': sku.name,
                'price': str(sku.price),
                'caption': sku.caption,
                'count': count,
                'selected': str(selected),
                'default_image_url': sku.default_image.url
            }
            return JsonResponse({'code': '0','cart_sku':cart_sku})
        else:
            # 未登录用户 保存在cookie
            # 先获取cookie数据，判断用户是否保存过
            cart_cookie = request.COOKIES.get('cart_cookie')
            if cart_cookie:
                # 有数据 解密
                data_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                data_dict = {}

            # 提取转化后的字典数据
            # """
            #     { sku_id:{'count':10,selected:True}}
            # """
            # 将新数据更新到字典
            data_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            cart_sku={
                'id': sku.id,
                'name': sku.name,
                'price': str(sku.price),
                'caption': sku.caption,
                'count': count,
                'selected': str(selected),
                'default_image_url': sku.default_image.url
            }
            # 将字典加密
            cart_cookie = base64.b64encode(pickle.dumps(data_dict)).decode()
            # 写入cookie
            response = JsonResponse({'code': 0,'cart_sku':cart_sku})
            response.set_cookie('cart_cookie', cart_cookie, 60 * 60 * 2)
            return response

    def delete(self,request):
        """
                   删除购物车数据
               :param request:
               :return:
        """

        # 1、获取前端数据 请求中
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2、验证数据
        sku_id = data_dict.get('sku_id')

        try:
            sku = SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({"error": '商品不存在'}, status=400)

        # 3、删除数据
        # 3-1判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 3-2登录用户 更新在redis
            client = get_redis_connection('carts')
            # 3-3删除sku_id和count hash
            client.hdel('carts_%s' % user.id, sku_id)
            # 3-4删除选中状态
            client.srem('carts_selected_%d' % user.id, sku_id)
            # 3-5 返回结果
            return JsonResponse({'code': '0'})
        else:
            # 未登录用户 保存在cookie
            # 先获取cookie数据，判断用户是否保存过
            cart_cookie = request.COOKIES.get('cart_cookie')
            if cart_cookie:
                # 有数据 解密
                data_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                return JsonResponse({'code': 0})
            # 提取转化后的字典数据
            """
                { sku_id:{'count':10,selected:True}}
            """
            # 判断当前sku_id是否在cookie中
            if sku_id in data_dict.keys():
                # 存在则删除字典中所对应的值
                del data_dict[sku_id]

            # 将字典加密
            cart_cookie = base64.b64encode(pickle.dumps(data_dict)).decode()
            # 写入cookie
            response = JsonResponse({'code': 0})
            response.set_cookie('cart_cookie', cart_cookie, 60 * 60 * 2)
            return response


class CartSelectionView(View):

    def put(self,request):
        #1、获取前端传递的更新状态
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2、验证数据
        selected = data_dict.get('selected')
        #2、判读用户是否登录
        user=request.user
        if user.is_authenticated:
            # 登录用户，更新redis中选中状态
            # 连接redis
            client = get_redis_connection('carts')
            # 获取所有的商品sku_id
            sku_id_count=client.hgetall('carts_%s' % user.id)
            sku_ids=sku_id_count.keys()
            if selected:
                # 选中状态，将所有sku_id添加到集合中
                client.sadd('carts_selected_%d' % user.id, *sku_ids)
            else:
                # 未选中状态，将所有sku_id从集合中删除
                client.srem('carts_selected_%d' % user.id, *sku_ids)
            return JsonResponse({'code':0})
        else:
            # 未登录
            # 先获取cookie数据，判断用户是否保存过
            cart_cookie = request.COOKIES.get('cart_cookie')
            if cart_cookie:
                # 有数据 解密
                data_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                return JsonResponse({'code': 0})
            # 遍历字典更新状态
            for sku_id,sku_dict in data_dict.items():
                sku_dict['selected']=selected

            # 将字典加密
            cart_cookie = base64.b64encode(pickle.dumps(data_dict)).decode()
            # 写入cookie
            response = JsonResponse({'code': 0})
            response.set_cookie('cart_cookie', cart_cookie, 60 * 60 * 2)
            return response


class CartSimpleView(View):
    def get(self,request):

        user = request.user
        if user.is_authenticated:
            # 3-2登录用户 保存在redis
            client = get_redis_connection('carts')
            # 3-3获取sku_id和count hash
            # client.hset('carts_%s' % user.id, sku_id, count)
            sku_id_count = client.hgetall('carts_%s' % user.id)
            # 3-4获取选中状态的ku_id
            sku_id_selected = client.smembers('carts_selected_%d' % user.id)
            data_dict={}
            for sku_id,count in sku_id_count.items():
                data_dict[int(sku_id)]={
                    'count':int(count),
                    'selected':sku_id in sku_id_selected
                }
        else:
            # 未登录用户 保存在cookie
            # 先获取cookie数据，判断用户是否保存过
            cart_cookie = request.COOKIES.get('cart_cookie')
            if cart_cookie:
                # 有数据 解密
                data_dict = pickle.loads(base64.b64decode(cart_cookie))
            else:
                data_dict = {}


        # 获取所有商品的key
        sku_keys = data_dict.keys()
        skus = SKU.objects.filter(id__in=sku_keys)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'price': str(sku.price),
                'caption': sku.caption,
                'count': data_dict[sku.id]['count'],
                'selected': str(data_dict[sku.id]['selected']),
                'default_image_url': sku.default_image.url
            })

        return JsonResponse({'cart_skus':cart_skus})
