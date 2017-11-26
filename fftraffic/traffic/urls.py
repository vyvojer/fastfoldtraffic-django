from django.conf.urls import url, include

from . import views

app_name = 'traffic'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<room>ps|pp)/(?P<table_name>\w+)/$', views.table, name='table'),
    url(r'^api/v1/scans/$', views.update_scans, name='update_scans'),
]