from rest_framework import serializers
from .models import Question, Choice
from django.contrib.auth.models import User



class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Question
		
		fields = ('id','question_text','pub_date','category')

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Choice
		fields = ('id','choice_text','votes')