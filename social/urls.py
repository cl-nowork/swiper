from django.conf.urls import url
from social import api

urlpatterns = [
    url(r'^get_rcmd_users', api.get_rcmd_users)
]