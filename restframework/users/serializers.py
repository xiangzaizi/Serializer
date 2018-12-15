import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueValidator

from users.models import Department, Employee


class EmployeeSerializer(serializers.Serializer):
    choices_gender = (
        (0, '男'),
        (1, '女'),
    )

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(label='姓名', max_length=20)
    age = serializers.IntegerField(label='年龄')
    gender = serializers.ChoiceField(label='性别', default=0, choices=choices_gender)
    salary = serializers.DecimalField(label='工资', max_digits=8, decimal_places=2)
    comment = serializers.CharField(label='备注', max_length=300, allow_null=True, allow_blank=True)
    hire_date = serializers.DateField(label='入职时间')

    # 关联属性
    # 方式一：　序列化为主键ｉｄ返回回去
    department = serializers.PrimaryKeyRelatedField(label='所属部门', read_only=True)
    # 方式二：　序列化部门对象所有字段
    # department = DepartmentSerializer()

    def create(self, validated_data):
        """新增一个员工"""
        # OrderedDict类型
        # return Department.objects.create(name='xxx', create_date=xxx)  # 关键字参数
        return Employee.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     修改员工信息
    #     :param instance: Department对象,表示要修改的部门
    #     :param validated_data: 用户请求传递过来的参数,OrderedDict类型
    #     :return:
    #     """
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.age = validated_data.get('age', instance.age)
    #     instance.gender = validated_data.get('gender', instance.gender)
    #     instance.salary = validated_data.get('salary', instance.salary)
    #     instance.comment = validated_data.get('comment', instance.comment)
    #     instance.hire_date = validated_data.get('hire_date', instance.hire_date)
    #     instance.save()  # 修改数据库数据
    #     return instance


class DepartmentSerializer(serializers.Serializer):
    """
    序列化器:
    1. 转成字典的属性
    2. 校验的参数
    """
    id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=10, label='部门名称')
    # 参数校验方式1: 通过字段和选项来校验
    name = serializers.CharField(max_length=10, label='部门名称')
    # \u4e00-\u9fa5:中文
    # name = serializers.RegexField('^[a-zA-Z0-9\u4e00-\u9fa5]$',
    #                               max_length=10, label='部门名称',
    #                               validators=[UniqueValidator(queryset=Department.objects.all())])
    create_date = serializers.DateField(label='成立时间')
    is_delete = serializers.BooleanField(default=False, label='是否删除', required=False)

    # 关联属性序列化：
    # 方式一：　
    # employee_set = serializers.PrimaryKeyRelatedField(
    #     label='部门员工', read_only=True, many=True)
    # 方式一:
    # employee_set = EmployeeSerializer(many=True, read_only=True)

    # 参数校验方式2:
    def validate_name(self, value):
        """
        校验部门名称
        :param value: 用户请求传递的要校验的参数值
        :return:
        """
        if not re.match('^[a-zA-Z0-9\u4e00-\u9fa5]+$', value):
            # 校验不通过 则抛异常
            raise ValidationError('部门名称必须为字母数字或中文')
        return value

    def create(self, validated_data):
        """新增一个部门"""
        # OrderedDict类型
        # return Department.objects.create(name='xxx', create_date=xxx)  # 关键字参数
        return Department.objects.create(**validated_data)  # 创建这个部门,与视图中的POST想对应

    def update(self, instance, validated_data):
        """
        修改部门
        :param instance: Department对象,表示要修改的部门
        :param validated_data: 用户请求传递过来的参数,OrderedDict类型
        :return:
        """
        instance.name = validated_data.get('name', instance.name)
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.save()  # 修改数据库数据
        return instance


class UserSerializer(serializers.Serializer):
    # 密码
    password = serializers.CharField(max_length=30)
    # 确认密码
    password2 = serializers.CharField(max_length=30)

    # 参数校验方式2: 校验多个参数
    def validate(self, attrs):
        """
        校验多个参数
        :param attrs: 用户请求传递过来的多个参数 (字典)
        :return:
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise ValidationError('两次输入的密码不一致')
        return attrs


class EmployeeSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Employee  # 关联的模型类对象
        fields = '__all__'  # 表示包含模型类中所有字段
        depth = 1               # 关联对象序列化





class DepartmentNameSerializer(serializers.Serializer):
    name = serializers.CharField(label='部门名称', max_length=20)



"""
# 序列化: 对象
from users.models import *
from users.serializers import *
dep = Department.objects.get(id=1)
serializer = DepartmentSerializer(dep)
print(serializer.data)


# 反序列化:
from users.models import *
from users.serializers import *
dict_data = {'name': '研发部'}
serializer = DepartmentSerializer(data=dict_data)       # 创建序列化
serializer.is_valid()                                   # 校验参数合法性
print(serializer.errors)                                # 校验出错信息
print(serializer.validated_data)                        # 显示校验通过的数据(OrderedDict)


# 反序列化: 保存和修改
from users.models import *
from users.serializers import *
dict_data = {'name': '研发部aaaaa', 'create_date': '2018-1-1'}
serializer = DepartmentSerializer(data=dict_data)       # 创建序列化
serializer.is_valid()                                   # 校验参数合法性
serializer.save()


from users.models import *
from users.serializers import *
dep = Department.objects.get(id=10)
dict_data = {'name': '研发部bbbbbbb', 'create_date': '2018-1-1'}
serializer = DepartmentSerializer(dep, data=dict_data)       # 创建序列化
serializer.is_valid()                                       # 校验参数合法性
serializer.save()

"""

