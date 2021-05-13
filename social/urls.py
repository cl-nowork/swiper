from django.conf.urls import url
from social import api

urlpatterns = [
    url(r'^get_rcmd_users', api.get_rcmd_users),
    url(r'^like', api.like),
    url(r'^superlike', api.superlike),
    url(r'^dislike', api.dislike),
    url(r'^show_liked_me', api.show_liked_me),
    url(r'^friend_list', api.friend_list),
    url(r'^rewind', api.rewind),
]