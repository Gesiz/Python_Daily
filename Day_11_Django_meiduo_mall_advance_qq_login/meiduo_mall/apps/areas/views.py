from django.http import JsonResponse
from django.views import View
from apps.areas.models import Area
import logging

logger = logging.getLogger('django')

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
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '省份数据错误'})

        # 响应省份数据
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'province_list': province_list})