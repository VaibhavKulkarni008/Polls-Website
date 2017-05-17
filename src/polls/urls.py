from django.conf.urls import url
from . import views
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns


app_name ='polls'


urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name = "index"),

	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

	url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name= 'results'),

	url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name = 'vote'),

	url(r'^(?P<question_id>[0-9]+)/export/$', views.export_excel, name= 'export_excel'),
]


urlpatterns += [
    url(r'^api/questions/$', views.QuestionList.as_view(), name= 'question-list'),
    url(r'^api/questions/(?P<pk>[0-9]+)/$', views.QuestionDetail.as_view(), name='question-detail'),
    url(r'^api/choices/$', views.ChoiceList.as_view(), name= 'choice-list'),
    url(r'^api/choices/(?P<pk>[0-9]+)/$', views.ChoiceDetail.as_view(), name='choice-detail'),
]



urlpatterns = format_suffix_patterns(urlpatterns)

