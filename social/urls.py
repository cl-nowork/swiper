from django.conf.urls import url
from social import api

urlpatterns = [
    url(r'^get_rcmd_users', api.get_rcmd_users),
    url(r'^like', api.like),
    url(r'^superlike', api.superlike),
]