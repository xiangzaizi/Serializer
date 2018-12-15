from django.http import HttpResponse
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from users.models import Department
from users.serializers import DepartmentSerializer, DepartmentNameSerializer


def index(request):
    return HttpResponse('index')


"""APIView + 序列化器 """
class DepartmentListAPIView(APIView):
    # 列表视图

    # get /departments/
    def get(self, request):
        """查询多条数据"""
        query_set = Department.objects.all()
        # 因为是多条数据所以后面需要+ many=True
        serializer = DepartmentSerializer(query_set, many=True)
        # return JsonResponse(serializer.data, safe=True)  # 字典数据
        return Response(serializer.data)                   # 字典数据

    def post(self, request):
        """新增一条数据"""
        serializer = DepartmentSerializer(data=request.data)
        # 数据校验
        serializer.is_valid(raise_exception=True)
        # 保存一个部门
        serializer.save()
        # 响应数据
        # 参数1: 序列化后的字典数据
        return Response(serializer.data, status=201)


class DepartmentDetailAPIView(APIView):
    # 详情视图

    def get(self, request, pk):
        """查询一条数据"""
        try:
            dep = Department.objects.get(id=pk)
        except Department.DoesNotExist:
            return Response(status=404)
        serializer = DepartmentSerializer(dep)
        return Response(serializer.data)  # 字典数据

    def put(self, request, pk):
        """修改部门"""
        try:
            dep = Department.objects.get(id=pk)
        except Department.DoesNotExist:
            return Response(status=404)
        # 参数1: 要修改的部门
        # 参数2: 用户通过请求体传递过来的参数
        serializer = DepartmentSerializer(dep, data=request.data)
        # 校验参数合法性
        serializer.is_valid(raise_exception=True)
        # 修改部门,会调用序列化器的update
        serializer.save()
        # 修改部门对象后, 序列化后的字典数据
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        # 删除一个部门  DELETE  /departments/<pk>
        # 查询要删除的部门对象
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return Response(status=404)
        # 删除部门
        department.delete()
        # 响应请求
        return Response(status=204)
"""GenericAPIView + 拓展类"""
class DepartmentListAPIView2(ListModelMixin, CreateModelMixin, GenericAPIView):
    # 部门查询集
    queryset = Department.objects.all()
    # 使用的序列化器
    serializer_class = DepartmentSerializer

    # get /departments/(d+)/
    def get(self, request):
        return self.list(request)  # ListModelMixin

    # post /departments
    def post(self, request):
        return self.create(request)  # CreateModelMixin

class DepartmentDetailAPIView2(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    # 首先两步,指定指定模型 + 对应的序列化器
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    # get /departments/(\d+)/
    def get(self, request, pk):
        """查询一条数据"""
        return self.retrieve(request, pk)  # RetrieveModelMixin

    # put /departments/(\d+)/
    def put(self, request, pk):
        """修改一条数据"""
        return self.update(request, pk)  # UpdateModelMixin

    # delete /departments/(\d+)/
    def delete(self, request, pk):
        """删除一条数据"""
        return self.destroy(request, pk)  # DestroyModelMixin

"""可用子类  ListAPIView + RetrieveAPIView"""
class DepartmentListAPIView3(ListAPIView):
    """查询多个部门"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetailAPIView3(RetrieveAPIView):
    """查询一个部门"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

""" 在同一个类中实现get请求的两个业务操作 """
class DepartmentAPIView4(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        print('pk=', pk)
        if pk: # 详情
            return self.retrieve(self, request, *args, **kwargs)
        else: # 列表
            return self.list(self, request, *args, **kwargs)

""" 视图集"""
class MyPermission(BasePermission):
    """自定义权限"""

    def has_permission(self, request, view):
        # 用户未登录无权限访问 list 动作(即查询所有部门)
        if view.action == 'list' and not request.user.is_authenticated():
            return False
        else:
            return True  # 有权限


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2  # 每页显示2条
    page_query_param = 'page'  # 查询关键字名称：第几页
    page_size_query_param = 'page_size'  # 查询关键字名称：每页多少条


class DepartmentViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    # 权限控制
    # permission_classes = [IsAuthenticated]   # 登录后才能访问,
    # permission_classes = [MyPermission]       # 改成自己定义的登录后才能访问所有的部门,其他接口可以任意调用

    # 过滤操作
    filter_fields = ('name',)
    # 指定分页配置
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        """使用不同的序列化器"""
        if self.action == 'name':  # name为自定义的action(修改部门名称)
            return DepartmentNameSerializer
        else:
            return DepartmentSerializer

    # detail为False 表示不需要根据主键操作一个模型类对象
    #
    @action(methods=['get'], detail=False)
    def latest(self, request):
        """
        自定义action: 查询最新成立的部门
        """
        department = Department.objects.latest('create_date')
        serializer = self.get_serializer(department)
        return Response(serializer.data)

    # detail为true表示需要根据主键操作一个模型类对象，
    # 则方法需要添加一个`pk`参数，来接收url传进来的主键
    # True, 配置请求的时候要匹配上ID
    @action(methods=['put'], detail=True)
    def name(self, request, pk):
        """
        自定义action: 修改部门名称
        :param request: 请求对象
        :param pk: 要修改部门的主键
        :return:
        """
        dep = self.get_object()
        dep.name = request.data.get('name')
        dep.save()
        serializer = self.get_serializer(dep)
        return Response(serializer.data)

