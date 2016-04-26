from django.contrib import admin
from .models import Choice, Question, PrimaryFlavor, SecondaryFlavor, TertiaryFlavor, Chemical

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    inlines = [ChoiceInline]

class ChemicalInline(admin.TabularInline):
    model = Chemical
    extra = 2

class SecondaryFlavorAdmin(admin.ModelAdmin):
    inlines = [ChemicalInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Chemical)
admin.site.register(PrimaryFlavor)
admin.site.register(SecondaryFlavor)
admin.site.register(TertiaryFlavor)
