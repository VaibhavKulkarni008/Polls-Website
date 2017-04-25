from django.contrib import admin

from .models import Question, Choice

"""
class QuestionInline(admin.TabularInline):
	model = Question
	extra = 0
"""

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 0
	classes = ['collapse']


class QuestionAdmin(admin.ModelAdmin):
	fields=['question_text','pub_date','category']
	inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
