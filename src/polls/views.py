#Built In Librarise
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import csv


# import for custom authetication for api
from rest_framework import permissions
from .permissions import ObjectPermissionCHeck



#Model imports
from .models import Question, Choice

#imports for viewset(rest api)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer, ChoiceSerializer

from rest_framework import mixins
from rest_framework import generics


#class based views
class IndexView(generic.ListView):
	""" View to display latest 5 questions """
	template_name='polls/index.html'
	context_object_name= 'latest_question_list'
	paginate_by = 5 



	def get_queryset(self):
		"""Pass the modelset to the template"""

		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


		


class DetailView(generic.DetailView):
	"""View to Display details of a Question"""
	model = Question
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
	""" View to display results of a Question """
	model = Question
	template_name= 'polls/results.html'


#function based views
def vote(request, question_id):
	""" Function to validate the voting form and calculating the votes """
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




def export_excel(request,question_id):
	""" Export the data form given question id into excel file """
	question_provided_in_url = get_object_or_404(Question, pk=question_id)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="question.csv"'

	writer = csv.writer(response)
	writer.writerow(['Question', 'Choice','Votes'])
	choice_list = Choice.objects.filter(question=question_provided_in_url)
	for given_choice in choice_list:
			writer.writerow(
				[
				question_provided_in_url.question_text,
				given_choice.choice_text,
				given_choice.votes,
				]
				)
	return response



#viewsets for api

class QuestionList(mixins.ListModelMixin,
					mixins.CreateModelMixin,
					generics.GenericAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)





class QuestionDetail(mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.DestroyModelMixin,
					generics.GenericAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

	def get(self, request, *args, **kwargs):

		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class ChoiceList(mixins.ListModelMixin,
					mixins.CreateModelMixin,
					generics.GenericAPIView):
	queryset = Choice.objects.all()
	serializer_class = ChoiceSerializer
	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)





class ChoiceDetail(mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.DestroyModelMixin,
					generics.GenericAPIView):
	queryset = Choice.objects.all()
	serializer_class = ChoiceSerializer

	permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

	def get(self, request, *args, **kwargs):

		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)