from django.contrib import admin
from .models import Question, Choice
from django import forms
from django.forms.models import BaseInlineFormSet


class AtLeastTwoRequiredInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """clean Checks that at least two choices have been entered.

        Raises:
            forms.ValidationError: Shows a message if no choice is entered
        """
        super(AtLeastTwoRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False) for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least two choices required.')


class ChoicesInline(admin.TabularInline):
    model = Choice
    formset = AtLeastTwoRequiredInlineFormSet
    extra = 2 # Number of choices displayed by default
    exclude = ['votes'] # Field to exclude from the model


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = (ChoicesInline,)
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.save()


admin.site.register(Question, QuestionAdmin)
