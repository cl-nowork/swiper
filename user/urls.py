from django.conf.urls import url
from user import api

urlpatterns = [
    url(r'^get_vcode/', api.get_vcode),
    url(r'^check_vcode/', api.check_vcode),
    url(r'^wb_auth/', api.wb_auth),
    url(r'^wb_callback', api.wb_callback),
]