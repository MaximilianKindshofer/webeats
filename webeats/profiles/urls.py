from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^fav_toggle/(?P<pk>[\d]+)/$',
        views.fav_toggle,
        name="fav_toggle",),
    url(r'^register/$',
        views.register,
        name="register",),
    url(r'^request_token/$',
        views.request_token,
        name="request_token",),
    url(r'^get_token/$',
        views.get_token,
        name="get_token",),
    url(r'^profile/$',
        views.profle,
        name="profile",),
        ]

