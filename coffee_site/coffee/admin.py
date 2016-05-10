from django.contrib import admin
from .models import Choice, Question, PrimaryFlavor, SecondaryFlavor, TertiaryFlavor, Chemical, Roaster, Coffee, SurveyResult, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text', 'description']
    inlines = [ChoiceInline]

class AnswerInline(admin.TabularInline):
    model = Answer

class SurveyResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed')
    inlines = [AnswerInline]

class ChemicalInline(admin.TabularInline):
    model = Chemical
    extra = 2

class SecondaryFlavorAdmin(admin.ModelAdmin):
    inlines = [ChemicalInline]

class RoasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'roaster', 'origin')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Chemical)
admin.site.register(PrimaryFlavor)
admin.site.register(SecondaryFlavor)
admin.site.register(TertiaryFlavor)
admin.site.register(Roaster, RoasterAdmin)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(SurveyResult, SurveyResultAdmin)
