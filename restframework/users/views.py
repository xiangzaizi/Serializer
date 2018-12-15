from django.http import HttpResponse
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


from users.models import Department
from users.serializers import DepartmentSerializer


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