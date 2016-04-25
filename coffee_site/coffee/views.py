from django.shortcuts import render
from django.http import HttpResponse

from .models import Question
from .forms import NameForm

def index(request):
    return render(request, 'coffee/index.html', {'form': NameForm()})
    #return HttpResponse("This is the main page. Description of site and buttons.")

def login(request):
    return HttpResponse("User login and registration page.")

def survey(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {
            'latest_question_list': latest_question_list,
        }
    return render(request, 'coffee/survey.html', context)

def taste(request):
    return HttpResponse("This is where the coffee tasting will happen.")

def recommend(request):
    return HttpResponse("This is where you will get your coffee recommendations.")
