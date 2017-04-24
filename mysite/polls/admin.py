from django.contrib import admin

from .models import Question, PollCategory, Choice

"""
class QuestionInline(admin.TabularInline):
	model = Question
	extra = 0
"""

class PollCategoryInline(admin.TabularInline):
	model = PollCategory.question.through
	extra = 0
	classes = ['collapse']


class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,					{'fields': ['question_text']}),
		('Date information',	{'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [PollCategoryInline]

class PollCategoryAdmin(admin.ModelAdmin):
	inlines = [
		PollCategoryInline,
	]
	exclude = ('question',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(PollCategory,PollCategoryAdmin)
admin.site.register(Choice)