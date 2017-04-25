#Built In Librarise
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

#3-rd party libraries
import django_excel as excel

#Model imports
from .models import Question, Choice

#class based views
class IndexView(generic.ListView):
	""" View to display latest 5 questions """
	template_name='polls/index1.html'
	context_object_name= 'latest_question_list'

	def get_queryset(self):
		"""Pass the modelset to the template"""
		return Question.objects.order_by('-pub_date')[:5]


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


# def export_excel(request):
# 	question_list = Question.objects.all()
# 	choice_list = Choice.objects.all()
# 	question_dict= dict()
# 	choice_dict=dict()
# 	new_dict = dict()



def export_excel(request, question_id):
	""" Export the data form given question id into excel file """
	question = get_object_or_404(Question, pk=question_id)
	query_sets = Choice.objects.filter(question=question)
	column_names = ['choice_text','votes']
	return excel.make_response_from_tables([Choice,Question], 'csv',file_name="All_Questions")

# """
# 	return excel.make_response_from_query_sets(
# 		query_sets, column_names, 'csv', file_name="question"
# 		)
# 	"""



