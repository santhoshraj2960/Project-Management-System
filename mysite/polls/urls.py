from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_file$', views.upload_file, name='upload_file'),
    url(r'^display_messages$', views.display_messages, name='display_messages'),
    url(r'^monthly_analytics$', views.monthly_analytics, name='monthly_analytics'),
    url(r'^graph_test$', views.graph_test, name='graph_test'),
]