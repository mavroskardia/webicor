from django.conf.urls import url, include

from . import views

urlpatterns = [    
    url(r'^entries$', views.entries, name='entries'),
    url(r'^test$', views.test)
]
