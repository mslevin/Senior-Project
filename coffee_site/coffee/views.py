from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
import datetime
import os
import json

from .models import Question, Choice, Coffee, SurveyResult, Answer
from .forms import NameForm

def index(request):
    return render(request, 'coffee/index.html', {'form': NameForm()})
    #return HttpResponse("This is the main page. Description of site and buttons.")

#def login(request):
#    return render(request, 'coffee/login.html')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'coffee/login.html')
    def post(self, request, *args, **kwargs):
        username = request.POST['user']
        password = request.POST['pass']
        print "Authenticate: " + username + " " + password
        user = authenticate(username=username, password=password)
        if user is not None:
            print "Authenticated"
            if user.is_active:
                print "User is active"
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                print "User is not active"
        else:
            print "Authenticate failed"
        return HttpResponseRedirect(reverse('login'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def survey(request):
    question_list = Question.objects.order_by('-pub_date')
    context = {
            'question_list': question_list,
        }
    return render(request, 'coffee/survey.html', context)

def submit(request):
    question_list = Question.objects.order_by('-pub_date')
    print request.user.username
    result = SurveyResult(user=request.user, completed=datetime.datetime.now())
    result.save()
    answer = Answer(result=result, question=question_list[0], answer=Choice.objects.get(pk=request.POST[str(1)]))
    print answer
    for question in question_list:
        answer = Answer(result=result, question=question, answer=Choice.objects.get(pk=request.POST[str(question.id)]))
        answer.save()
        ans = Choice.objects.get(pk=request.POST[str(question.id)])
        print question.question_text, " : ", ans
    return HttpResponseRedirect(reverse('recommend'))

def taste(request):
    return HttpResponse("This is where the coffee tasting will happen.")

def recommend(request):
    all_surveys = SurveyResult.objects.filter(user=request.user).order_by('-completed')
    if (len(all_surveys) > 0):
        survey = all_surveys[0]
        answers = survey.answer_set.all()
        modifiers = []
        for ans in answers:
            for mod in ans.answer.description.split(', '):
                modifiers.append(mod)
        context = {
            "survey": survey,
            "modifiers": ",".join(modifiers)
        }
        return render(request, 'coffee/recommend.html', context)
    else:
        return render(request, 'coffee/no_surveys.html')

def coffees(request):
    coffee_list = Coffee.objects.all()
    context = {'coffee_list': coffee_list}
    return render(request, 'coffee/coffees.html', context)
