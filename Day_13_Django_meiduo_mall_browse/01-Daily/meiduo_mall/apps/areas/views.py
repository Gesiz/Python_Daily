from django.http import JsonResponse
from django.views import View
from apps.areas.models import Area


# Create your views here.
class AreasView(View):
    """省市区数据"""

    def get(self, request):
        """提供省市区数据"""

        # 提供省份数据
        try:
            # 查询省份数据
            province_model_list = Area.objects.filter(parent__isnull=True)

            # 序列化省级数据
            province_list = []
            for province_model in province_model_list:
                province_list.append({'id': province_model.id, 'name': province_model.name})
        except Exception as e:

            return JsonResponse({'code': 400, 'errmsg': '省份数据错误'})

        # 响应省份数据
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'province_list': province_list})


class SubAreasView(View):
    """省市区数据"""

    def get(self, request, pk):
        """提供省市区数据"""

        # 提供市或区数据
        try:
            parent_model = Area.objects.get(id=pk)  # 查询市或区的父级
            sub_model_list = parent_model.subs.all()

            # 序列化市或区数据
            sub_list = []
            for sub_model in sub_model_list:
                sub_list.append({'id': sub_model.id, 'name': sub_model.name})

            sub_data = {
                'id': parent_model.id,  # 父级pk
                'name': parent_model.name,  # 父级name
                'subs': sub_list  # 父级的子集
            }

        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '城市或区数据错误'})

        # 响应市或区数据
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'sub_data': sub_data})
