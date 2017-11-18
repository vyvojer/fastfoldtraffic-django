from django.conf.urls import url, include

from .views import index

app_name = 'traffic'

urlpatterns = [
    url(r'^$', index, name='index'),
]