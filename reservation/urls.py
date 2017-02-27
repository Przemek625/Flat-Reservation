from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', view=views.index, name='index'),
    url(r'^add_flat/$', view=views.add_flat, name="add_flat"),
    url(r'^add_city/$', view=views.add_city, name="add_city"),
    url(r'^reserve_flat/', view=views.reserve_flat, name="reserve_flat"),
    url(r'reserve_flat_result/', view=views.reserve_flat_result, name="reserve_flat_result")
]
