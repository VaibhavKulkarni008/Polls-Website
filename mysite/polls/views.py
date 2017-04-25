from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
import django_excel as excel

from .models import Question, Choice

class IndexView(generic.ListView):
	""" View to display latest 5 questions """
	template_name='polls/index.html'
	context_object_name= 'latest_question_list'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	"""View to Display details of a Question"""
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	""" View to display results of a Question """
	model = Question
	template_name= 'polls/results.html'

def vote(request, question_id):
	""" Vote and display the results """
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


def export_excel(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	query_sets = Choice.objects.filter(question=question)
	column_names = ['choice_text','votes']

	return excel.make_response_from_query_sets(query_sets, column_names, 'xls', file_name="question")