from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^fav_toggle/(?P<pk>[\d]+)/$',
        views.fav_toggle,
        name="fav_toggle",),
    url(r'^register/$',
        views.register,
        name="register",),
    url(r'^get_token/$',
        views.get_token,
        name="get_token",),
        ]
