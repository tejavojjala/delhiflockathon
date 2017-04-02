from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^events$', views.events, name='events'),
	url(r'^index$', views.index, name='index'),
	url(r'^pinnedmessages$', views.pinnedmessages, name='pinnedmessages'),
	url(r'^pinnedmessages/like$', views.like, name='like'),
	url(r'^pinnedmessages/dislike$', views.dislike, name='dislike'),
	url(r'^pinnedmessages/remove$', views.remove, name='remove'),
	url(r'^pinnedmessages/comment$', views.comment),
	url(r'^pinnedmessages/removecomment$', views.removeComment),
]
