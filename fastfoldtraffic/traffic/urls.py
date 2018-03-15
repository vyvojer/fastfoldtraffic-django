from django.urls import re_path, path

from . import views

app_name = 'traffic'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    path('ps/<slug:table_name>/', views.TableView.as_view(), name='table'),
    re_path(r'^api/v1/scans/$', views.update_scans, name='update_scans'),
]