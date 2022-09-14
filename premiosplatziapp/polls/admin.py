from django.contrib import admin
from .models import Question, Choice
from django import forms
from django.forms.models import BaseInlineFormSet


class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """clean Checks that at least one choice has been entered.

        Raises:
            forms.ValidationError: Shows a message if no choice is entered
        """
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False) for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least two choices required.')


class ChoicesInline(admin.StackedInline):
    model = Choice
    formset = AtLeastOneRequiredInlineFormSet
    extra = 2
    exclude = ['votes']


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = (ChoicesInline,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.save()


admin.site.register(Question, QuestionAdmin)
