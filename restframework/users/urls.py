from django.conf.urls import url
from rest_framework.routers import SimpleRouter, DefaultRouter

from users import views
from users.views import DepartmentListAPIView, DepartmentDetailAPIView, DepartmentListAPIView2,DepartmentListAPIView3,DepartmentDetailAPIView3,DepartmentAPIView4

urlpatterns = [
    url(r'index', views.index),
    url(r'^department$', DepartmentListAPIView.as_view()),
    url(r'^department/(?P<pk>\d+)$', DepartmentDetailAPIView.as_view()),
    url(r'^departments2$', DepartmentListAPIView2.as_view()),
    url(r'^departments3$', DepartmentListAPIView3.as_view()),
    url(r'^departments3/(?P<pk>\d+)$', DepartmentDetailAPIView3.as_view()),
    url(r'^departments4$', DepartmentAPIView4.as_view()),
    url(r'^departments4/(?P<pk>\d+)$', DepartmentAPIView4.as_view()),

    # 视图集的url配置方式一
    # {'get': 'list'}:
    # 键:　请求方法
    # 值: action动作，　要调用的业务方法名
    # url(r'^departments5/$', views.DepartmentViewSet.as_view({'get': 'list'})),
    # url(r'^departments5/(?P<pk>\d+)/$', views.DepartmentViewSet.as_view({'get': 'retrieve'})),
    # url(r'^departments5/latest/', views.DepartmentViewSet.as_view({'get': 'latest'})),  # action, 查找最新添加的数据
    # url(r'^departments5/(?P<pk>\d+)/name/$', views.DepartmentViewSet.as_view({'put': 'name'})),  # action, 指定修改部门的名称

]

# url配置方式二
router = SimpleRouter()
# router = DefaultRouter() # API root 会展示列表以外的视图集, 就是请求的URL 会展示出来
# 参数1: 路由地址的前缀
router.register(r'departments5', views.DepartmentViewSet)
router.register(r'employee5', views.EmployeeViewSet)
urlpatterns += router.urls
