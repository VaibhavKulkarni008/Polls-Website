
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from polls import views


urlpatterns = [

	url(r'^polls/', include('polls.urls')),
	url(r'^admin/', admin.site.urls),
]
urlpatterns += [
	url(r'^api-auth/', include('rest_framework.urls',
								namespace='rest_framework')),
]