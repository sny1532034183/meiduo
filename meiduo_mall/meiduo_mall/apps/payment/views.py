from alipay import AliPay
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from orders.models import OrderInfo
import os
# Create your views here.
from payment.models import Payment


class PayMentView(View):

    def get(self,request,order_id):
        """
            构建跳转连接
        :param request:
        :param order_id:  订单id
        :return:
        """
        try:
            order=OrderInfo.objects.get(order_id=order_id)
        except:
            return JsonResponse({'error':'订单不存在'},status=400)
        path=os.path.join(settings.BASE_DIR,'apps/payments/keys/app_private_key.pem')
        # 1、初始化支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID, # 支付宝应用中的appid
            app_notify_url=None,  # 默认回调url
            # 美多私钥
            app_private_key_path=os.path.join(settings.BASE_DIR,'apps/payment/keys/app_private_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR,'apps/payment/keys/alipay_public_key.pem'),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug = settings.ALIAPY_DEBUG  # 默认False
        )
        # 构建网址中的查询字符传数据
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id, # 指定当前订单的编号
            total_amount=str(order.total_amount), # 指定订单的金额
            subject='美多商城-%s'%order_id,  # 订单标题
            return_url=settings.ALIPAY_RETURN_URL, # 支付成功后跳转美多连接地址
        )
        alipay_url=settings.ALIPAY_URL+order_string

        return JsonResponse({'alipay_url':alipay_url,'code':0})


class PayMentStatusView(View):
    def get(self,request):
        """
            保存支付结果
        :param request:
        :return:
        """
        # 1、获取查询字符串数据
        data=request.GET.dict()
        signature = data.pop("sign")

        # 2、验证是否是从支付宝跳转回来的请求
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 支付宝应用中的appid
            app_notify_url=None,  # 默认回调url
            # 美多私钥
            app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/payment/keys/app_private_key.pem'),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/payment/keys/alipay_public_key.pem'),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        success = alipay.verify(data, signature)
        if success:
            # 3、保存支付结果
            order_id=data['out_trade_no']
            trade_id=data['trade_no']
            Payment.objects.create(order_id=order_id,trade_id=trade_id)
            # 当前订单状态的修改
            OrderInfo.objects.filter(order_id=order_id,pay_method=2).update(status=2)
            # 4、渲染支付成功页面
            return render(request,'pay_success.html',{'trade_no':trade_id})
        else:
            return render(request,'404.html')
