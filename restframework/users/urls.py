from django.conf.urls import url
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
]
