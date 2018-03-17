from django.urls import re_path, path

from . import views

app_name = 'traffic'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    path('ps/<slug:table_name>/', views.TableCurrentView.as_view(), name='table_current'),
    path('ps/<slug:table_name>/last-24/', views.TableLast24View.as_view(), name='table_last_24'),
    path('ps/<slug:table_name>/by-hour/', views.TableByHourView.as_view(), name='table_by_hour'),
    path('ps/<slug:table_name>/by-weekday/', views.TableByWeekdayView.as_view(), name='table_by_weekday'),
    re_path(r'^api/v1/scans/$', views.update_scans, name='update_scans'),
]