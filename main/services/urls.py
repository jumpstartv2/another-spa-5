from django.conf.urls import url

from . import api


urlpatterns = [
    url(r'^jumpstart/$', api.JumpStartAPIView.as_view(), name='jumpstart'),
]
