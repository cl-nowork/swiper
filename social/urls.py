from django.conf.urls import url
from social import api

urlpatterns = [
    url(r'^get_rcmd_users', api.get_rcmd_users),
    url(r'^like', api.like),
    url(r'^superlike', api.superlike),
    url(r'^dislike', api.dislike),
    url(r'^who_liked_me', api.who_liked_me),
    url(r'^friend_list', api.friend_list),
]