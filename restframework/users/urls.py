from django.conf.urls import url
from users import views
from users.views import DepartmentListAPIView, DepartmentDetailAPIView, DepartmentListAPIView2

urlpatterns = [
    url(r'index', views.index),
    url(r'^department$', DepartmentListAPIView.as_view()),
    url(r'^department/(?P<pk>\d+)$', DepartmentDetailAPIView.as_view()),
    url(r'^departments2$', DepartmentListAPIView2.as_view()),
]
