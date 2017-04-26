from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Question, Choice


# custom admin action


def export_question_set_as_csv(modeladmin, request, queryset):
		#for question fields
		opts = modeladmin.model._meta

		field_names = [field.name for field in opts.fields]

		#for choice fields
		

		response = HttpResponse(content_type='text/csv')

		response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

		writer = csv.writer(response)

		writer.writerow(field_names)

		for obj in queryset:

			row = [getattr(obj, field)() 
			if callable(getattr(obj, field)) 
			else getattr(obj, field) 
			for field in field_names]

			writer.writerow(row)

		return response

		export_as_csv.short_description = description

		return export_as_csv





class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 1


class QuestionAdmin(admin.ModelAdmin):
	fields=['question_text','pub_date','category']
	inlines = [ChoiceInline]
	list_display = ['question_text','pub_date']
	actions = [export_question_set_as_csv]


admin.site.register(Question, QuestionAdmin)
