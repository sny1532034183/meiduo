import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django_redis import get_redis_connection
from addersses.models import Address
from datetime import datetime
from decimal import Decimal

# Create your views here.
from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


# 结算订单
@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def get(self, request):
        # 渲染地址
        # 获取当前用户下的没有删除的地址
        user = request.user
        addresses = Address.objects.filter(user=user,is_delete=False)
        # 商品数据渲染 从redis中获取选中状态的商品
        client = get_redis_connection('carts')
        # 获取商品数量
        sku_id_count = client.hgetall('carts_%s' % user.id)
        sku_count = {}
        for sku_id, count in sku_id_count.items():
            sku_count[int(sku_id)] = int(count)
        # 获取选中的sku-id
        sku_ids = client.smembers('carts_selected_%d' % user.id)
        # 查询所有的商品信息
        skus = SKU.objects.filter(id__in=sku_ids)
        sku_list = []
        total_count = 0
        total_amount = 0
        for sku in skus:
            sku_list.append({
                'default_image_url': sku.default_image.url,
                'name': sku.name,
                'price': sku.price,
                'count': sku_count[sku.id],
                'total_amount': sku_count[sku.id] * sku.price
            })
            # 累加商品数量
            total_count += sku_count[sku.id]
            # 累加商品价格
            total_amount += sku_count[sku.id] * sku.price
        # 运费
        transit = 10
        # 总金额
        payment_amount = total_amount + transit
        data = {
            'addresses': addresses,
            'sku_list': sku_list,
            'total_count': total_count,
            'total_amount': total_amount,
            'transit': transit,
            'payment_amount': payment_amount
        }
        return render(request, 'place_order.html', data)

#提交订单页面
class OrderCommitView(View):
    # @transaction.atomic
    def post(self, request):
        # 1、获取前端传递的数据 json
        data = request.body.decode()
        data_dict = json.loads(data)
        address_id = data_dict.get('address_id')
        pay_method = data_dict.get('pay_method')
        try:
            address = Address.objects.get(id=address_id)
        except:
            return JsonResponse({'error': '地址不存在'}, status=400)
        # 2、获取当前用户对象
        user = request.user
        # 3、生成订单id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + '%09d' % user.id
        # 开启事务
        with transaction.atomic():
            # 设置保存点
            save_point = transaction.savepoint()
            try:
                # 4、初始化生成订单基本信息表
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal(0),
                    freight=Decimal(10),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM[
                        'ALIPAY'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )
                # 5、查询选中状态的商品
                # 商品数据渲染 从redis中获取选中状态的商品
                client = get_redis_connection('carts')
                # 获取商品数量
                sku_id_count = client.hgetall('carts_%s' % user.id)
                sku_count = {}
                for sku_id, count in sku_id_count.items():
                    sku_count[int(sku_id)] = int(count)
                # 获取选中的sku-id
                sku_ids = client.smembers('carts_selected_%d' % user.id)
                # 查询所有的商品信息
                # skus = SKU.objects.filter(id__in=sku_ids)

                # 6、循环遍历商品处理订单商品表
                for sku_id in sku_ids:
                    while True:
                        # 6-1 获取当前商品的库存
                        sku = SKU.objects.get(id=sku_id)
                        count = sku_count[sku.id]
                        stock_old = sku.stock
                        sales_old = sku.sales
                        # 6-2 判断购买的数据是否超过库存
                        if count > stock_old:
                            return JsonResponse({'message': '库存不足'}, status=400)
                        # 6-3 修改sku商品库存和销量
                        stock_new = sku.stock - count
                        sales_new = sku.sales + count
                        # 当判断库存充足进行数量更新
                        print('q111111111')
                        print('22222222')
                        # stock = sku.stock
                        # if stock_old != stock:
                        #     return JsonResponse({'message': '库存不足'}, status=400)
                        # sku.stock = stock_new
                        # sku.sales = sales_new
                        # sku.save()
                        res = SKU.objects.filter(id=sku_id, stock=stock_old).update(stock=stock_new, sales=sales_new)
                        print(res)
                        if res == 0:
                            continue
                        # 6-4 修改spu表中的总销量
                        sku.spu.sales += count
                        # 6-5 累加订单数量
                        order.total_count += count
                        # 6-6 累加订单的价格
                        order.total_amount += sku.price * count
                        # 6-7 保存订单商品数据
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=count,
                            price=sku.price
                        )
                        break

                order.total_amount += order.freight
                order.save()
            except:
                # 回滚到爆保存点
                transaction.savepoint_rollback(save_point)
                return JsonResponse({'error': '保存失败'}, status=400)
            else:
                # 没有数据库操作异常进行提交
                transaction.savepoint_commit(save_point)
                # 7、删除购物车选中状态的商品
                client.hdel('carts_%s' % user.id, *sku_ids)
                client.srem('carts_selected_%d' % user.id, *sku_ids)

                return JsonResponse({'code': 0, 'order_id': order_id})


class OrderSuccessView(View):
    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')
        data = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method

        }
        return render(request, 'order_success.html', data)


class OrderInfoView(View):
    def get(self, request, pk):
        # 1、获取当前登录用户
        user = request.user
        orders = OrderInfo.objects.filter(user=user)
        # 订单商品

        for order in orders:
            order.details = []
            # 获取订单商品
            order_goods = order.skus.all()
            for order_good in order_goods:
                order.details.append(
                    {
                        'default_image_url': order_good.sku.default_image.url,
                        'price': order_good.sku.price,
                        'name': order_good.sku.name,
                        'count': order_good.count,
                        'total_amount': order_good.count * order_good.sku.price
                    }
                )

        page = Paginator(orders,5)
        order_pages = page.page(pk)

        data = {
            'page': order_pages,  # 分页后的商品数据
            'page_num': pk,  # 当前页数
            'total_page': page.num_pages,  # 总页数
        }

        return render(request, 'user_center_order.html', data)


class OrderCommentView(View):
    def get(self, request):
        """
            订单评价页面
        :param request:
        :return:
        """
        # 1、获取订单编号查询订单对象
        order_id = request.GET.get('order_id')
        # 2、根据订单对象查询订单商品信息
        try:
            order = OrderInfo.objects.get(order_id=order_id)
        except:
            return render(request, '404.html')
        goods_order = order.skus.filter(is_commented=False)
        # 3、构建渲染数据内容
        skus = []
        for good in goods_order:
            skus.append({
                'name': good.sku.name,
                'price': str(good.price),
                'count': good.count,
                'comment': good.comment,
                'score': good.score,
                'is_anonymous': str(good.is_anonymous),
                'is_commented': str(good.is_commented),
                'default_image_url': good.sku.default_image.url,
                'order_id': order_id,
                'sku_id': good.sku.id
            })

        data = {'skus': skus}

        return render(request, 'goods_judge.html', data)

    def post(self, request):
        """
            保存订单商品评价信息
        :param request:
        :return:
        """
        # 1、获取数据
        data = request.body.decode()
        data_dict = json.loads(data)
        # 2、验证数据
        sku_id = data_dict.get('sku_id')
        order_id = data_dict.get('order_id')
        comment = data_dict.get('comment')
        score = data_dict.get('score')
        is_anonymous = data_dict.get('is_anonymous')
        try:
            sku=SKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'error':'商品不存在'},status=400)
        try:
            OrderInfo.objects.get(order_id=order_id)
        except:
            return JsonResponse({'error': '订单不存在'}, status=400)
        # 3、保存评价信息
        OrderGoods.objects.filter(order=order_id,sku=sku).update(comment=comment,score=score,is_anonymous=is_anonymous,is_commented=True)
       #4.累计评论数据
        sku.comments+=1
        sku.save()
        sku.spu.comments+=1
        sku.spu.save()
        #5.如果所有订单商品都已评价，则修改订单状态为以完成
        if OrderGoods.objects.filter(order_id=order_id,is_commented=False).count==0:
            OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM["FINISHED"])

        # 6、返回结果
        return JsonResponse({'code':0})
