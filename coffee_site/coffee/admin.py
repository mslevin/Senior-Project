from django.contrib import admin
from .models import Choice, Question
from .models import Chemical, GCMSResult
from .models import Roaster, Coffee
from .models import SurveyResult, Answer
from .models import BrewMethod, Brew
from .models import UserData

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

class GCMSResultAdmin(admin.ModelAdmin):
    inlines = [ChemicalInline]

#class SecondaryFlavorAdmin(admin.ModelAdmin):
#    inlines = [ChemicalInline]

class RoasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'roaster', 'origin')

class BrewAdmin(admin.ModelAdmin):
    list_display = ('user', 'method', 'date')

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'recommendation')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Chemical)
#admin.site.register(PrimaryFlavor)
#admin.site.register(SecondaryFlavor)
#admin.site.register(TertiaryFlavor)
admin.site.register(Roaster, RoasterAdmin)
admin.site.register(Coffee, CoffeeAdmin)
admin.site.register(SurveyResult, SurveyResultAdmin)
admin.site.register(BrewMethod)
admin.site.register(Brew, BrewAdmin)
admin.site.register(GCMSResult, GCMSResultAdmin)
admin.site.register(UserData, UserDataAdmin)
