from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^fav_toggle/(?P<pk>[\d]+)/$',
        views.fav_toggle,
        name="fav_toggle",),
        ]
