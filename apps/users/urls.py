from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^verify$', views.verify),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^process$', views.process),
    url(r'^user/(?P<number>\d+)$', views.user_page),
    url(r'^add/(?P<number>\d+)$', views.add),
    url(r'^remove/(?P<number>\d+)$', views.remove),
    url(r'^logout$', views.logout),

]