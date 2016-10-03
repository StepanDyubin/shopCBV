from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>[\w-]+)/$', views.page_detail, name='page_detail'),

]
