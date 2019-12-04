from django.shortcuts import render
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from addersses.models import Area,Address
from django.http import JsonResponse
from django.core.cache import cache
import json
import re
from django.core import serializers

@method_decorator(login_required, name='dispatch')
class AddressView(View):
    """
    获取展示页面地址
    """
    # 查询当前用户的地址信息
    def get(self,request):
        user=request.user
        addresses=Address.objects.filter(user=user,is_delete=False)
        addresses_list = []
        for address in addresses:
            addresses_list.append({
                'id': address.id,
                'receiver': address.receiver,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email,
            })

        return render(request, 'user_center_site.html', {'addresses': addresses_list})


@method_decorator(login_required,name="dispatch")
class AreasView(View):
    def get(self,request):
        #获取area_id
        area_id=request.GET.get("area_id")
        #省
        if area_id is None:
            province_list=cache.get("province_list")
            #判断是否有缓存,没有缓存则拿取数据在缓存到其中
            if province_list is None:
                data=Area.objects.filter(parent_id__isnull=True)
                province_list=[]
                for province in data:
                    province_list.append({
                        "id":province.id,
                        "name":province.name
                    })
                #设置缓存key_value还有缓存 时间
                cache.set("province_list",province_list,60*60*3)

        # area_id有值，是市或区
        else:
            # 判断有无缓存
            province_list= cache.get("province_list_%s"%area_id)
            if province_list is None:
                data=Area.objects.filter(parent_id=area_id)
                province_list=[]
                for province in data:
                    province_list.append({
                        "id":province.id,
                        "name":province.name
                    })
                cache.set("province_list_%s"%area_id,province_list,60*60*60)

        return JsonResponse({
            "code":"0",
            "province_list":province_list
        })

class AddressCreateView(View):
    def post(self,request):
        # 1.获取前端数据
        data=request.body.decode()
        data_dict=json.loads(data)
        receiver = data_dict.get('receiver')
        province_id = data_dict.get('province_id')
        city_id = data_dict.get('city_id')
        district_id = data_dict.get('district_id')
        place = data_dict.get('place')
        mobile = data_dict.get('mobile')
        tel = data_dict.get('tel')
        email = data_dict.get('email')
        #2验证数据
        if len(receiver)>20 or len(receiver)<0:
            return JsonResponse({"code":5001})
        if not re.match(r"1[3-9]\d{9}",mobile):
            return JsonResponse({"code":4007})
        if mobile is None or mobile == '':
            return JsonResponse({"code": 4007})

        # 3.保存数据
        user=request.user
        address = Address.objects.create(user=user, receiver=receiver, province_id=province_id, city_id=city_id,
                                         district_id=district_id, place=place, mobile=mobile, tel=tel, email=email)
        address_dict = {
            'id': address.id,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email,
        }
        # 4、返回结果
        return JsonResponse({'code': '0', 'address': address_dict})

    def put(self,request,pk):
        # 1、获取前端数据
        data = request.body.decode()
        data_dict = json.loads(data)
        receiver = data_dict.get('receiver')
        province_id = data_dict.get('province_id')
        city_id = data_dict.get('city_id')
        district_id = data_dict.get('district_id')
        place = data_dict.get('place')
        mobile = data_dict.get('mobile')
        tel = data_dict.get('tel')
        email = data_dict.get('email')

        # 2、验证数据
        if len(receiver) > 20 or len(receiver) < 0:
            return JsonResponse({"code": 5001})
        if not re.match(r'1[3-9]\d{9}', mobile):
            return JsonResponse({"code": 4007})
        if mobile is None or mobile == '':
            return JsonResponse({"code": 4007})

        # 3、更新数据
        address = Address.objects.get(id=pk)
        address.receiver = receiver
        address.province_id = province_id
        address.city_id = city_id
        address.district_id = district_id
        address.place = place
        address.mobile = mobile
        address.tel = tel
        address.email = email
        address.save()

        # 4、返回结果
        address_dict = {
            'id': address.id,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email,
        }
        # 4、返回结果
        return JsonResponse({'code': '0', 'address': address_dict})

    def delete(self,request,pk):
        address=Address.objects.get(id=pk)
        address.is_delete=True
        address.save()

        return JsonResponse({"code":"0"})


class AddressDefaultView(View):
    def put(self,request,address_id):
        address=Address.objects.get(id=address_id)
        #设置地址为默认地址
        request.user.default_address=address
        request.user.save()

        return JsonResponse({"code":"0"})


class AddressTitleView(View):
    def put(self,request,address_id):
        #接收参数，地址标题
        json_dict=json.loads(request.body.decode())
        title=json_dict.get("title")
        #查询地址
        address=Address.objects.get(id=address_id)
        address.title=title
        address.save()
        return JsonResponse({"code":0})

