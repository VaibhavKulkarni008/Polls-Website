from django import forms

from .models import Question

class ChoiceForm(forms.ModelForm):
	class Mera:
		model = Question
		fields =[
			"question_text",
			"choice_text",

		]