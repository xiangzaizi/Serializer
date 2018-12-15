from django.conf.urls import url
from users import views
from users.views import DepartmentListAPIView, DepartmentDetailAPIView

urlpatterns = [
    url(r'/', views.index),
    url(r'^department$', DepartmentListAPIView.as_view())
]
