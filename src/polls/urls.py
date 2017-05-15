from django.conf.urls import url
from . import views

#imports for api
from rest_framework import routers


app_name ='polls'


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name = "index"),
    
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name= 'results'),

    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name = 'vote'),

     url(r'^(?P<question_id>[0-9]+)/export/$', views.export_excel, name= 'export_excel'),

]


router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'choices', views.ChoiceViewSet)

urlpatterns += router.urls