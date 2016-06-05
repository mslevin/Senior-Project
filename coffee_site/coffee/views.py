from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.utils import timezone

import datetime
import os
import json

from .models import Question, Choice, Coffee, SurveyResult, Answer, BrewMethod, Brew, GCMSResult, Chemical, UserData
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
        print "Authenticate: " + username
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
    # make sure that someone is logged in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    question_list = Question.objects.order_by('-pub_date')
    context = {
            'question_list': question_list,
        }
    return render(request, 'coffee/survey.html', context)

def submit(request):
    question_list = Question.objects.order_by('-pub_date')
    result = SurveyResult(user=request.user, completed=timezone.now())
    result.save()
    #answer = Answer(result=result, question=question_list[0], answer=Choice.objects.get(id=request.POST[str(1)]))
    #print answer
    for question in question_list:
        #print question.id
        #print request.POST.get(str(question.id))
        Answer(result=result, question=question, answer=Choice.objects.get(id=request.POST[str(question.id)])).save()
        ans = Choice.objects.get(pk=request.POST[str(question.id)])
        #print question.question_text, " : ", ans
    return HttpResponseRedirect(reverse('recommend'))

class TasteView(View):
    def get(self, request, *args, **kwargs):
        # make sure that someone is logged in
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        # this is the START of a tasting
        # user will choose a coffee and enter brew information
        recommendation = UserData.objects.get(user=request.user).recommendation
        context = {
            "recommendation": recommendation,
            "coffees": Coffee.objects.all(),
            "brew_methods": BrewMethod.objects.all()
        }
        return render(request, 'coffee/taste.html', context)
    def post(self, request, *args, **kwargs):
        # make sure that someone is logged in
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        # validate brew data
        # make a new brew object and save it to the DB

        # check if the tasting is complete
        if (request.POST.get("complete") != "true"):
            ratio = round(float(request.POST['grams_water']) / float(request.POST['grams_coffee']), 2)
            brew = Brew(user=request.user,\
                        method=BrewMethod.objects.get(name=request.POST['brewmethod']),\
                        coffee=Coffee.objects.get(name=(request.POST['coffee']).split(" - ")[0]),\
                        grams_coffee=request.POST['grams_coffee'],\
                        grams_water=request.POST['grams_water'],\
                        water_temp=request.POST['water_temp'],\
                        grind=request.POST['grind_setting'],\
                        duration=request.POST['brew_time'])

            context = {
                "brew":brew,
                "ratio":ratio
            }
            return render(request, 'coffee/taste2.html', context)
        else:
            return HttpResponse("lol")


def saveTasting(request):
    print request.POST


def recommend(request):
    # make sure that someone is logged in
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    all_surveys = SurveyResult.objects.filter(user=request.user).order_by('-completed')
    if (len(all_surveys) > 0):
        survey = all_surveys[0]
        # have they taken the survey since their last recommendation?
        try:
            ud = UserData.objects.get(user=request.user)
        except UserData.DoesNotExist:
            ud = UserData(user=request.user)

        modifiers = []
        best_result = GCMSResult.objects.all()[0]
        if (ud.time < survey.completed and ud.recommendation is not None):
            best_result = GCMSResult.objects.get(coffee=ud.recommendation)
            print "Using previous recommendation"
        else:
            answers = survey.answer_set.all()
            for ans in answers:
                for mod in ans.answer.description.split(', '):
                    modifiers.append(mod)
            # Find the best coffee!
            best_score = 0
            best_descriptors = []
            for res in GCMSResult.objects.all():
                curr_score = get_score(modifiers, all_descriptors(res))
                print res.coffee.name + " " + str(curr_score)
                if (curr_score > best_score):
                    best_score = curr_score
                    best_result = res
                    #best_descriptors = all_descriptors(res)

        descriptors = ["+" + str(d).encode("utf-8") for d in all_descriptors(best_result)]

        try:
            UserData.objects.get(user=request.user).delete()
        except UserData.DoesNotExist:
            print "No UserDatas found"
        data = UserData(user=request.user, recommendation=best_result.coffee)
        data.save()
        context = {
            "recommendation": best_result.coffee,
            "survey": survey,
            "modifiers": ",".join(modifiers),
            "descriptors": ",".join(descriptors)
        }
        return render(request, 'coffee/recommend.html', context)
    else:
        return render(request, 'coffee/no_surveys.html')


def coffees(request):
    # its ok to not be logged in here
    coffee_list = Coffee.objects.all()
    context = {'coffee_list': coffee_list}
    return render(request, 'coffee/coffees.html', context)

def coffee_details(request, coffee_id):
    coffee = Coffee.objects.get(id=coffee_id)
    descriptors = ["+" + str(d).encode("utf-8") for d in all_descriptors(GCMSResult.objects.get(coffee=coffee))]
    #chemicals = []
    chemicals = Chemical.objects.filter(result=GCMSResult.objects.get(coffee=coffee))
    #brews = Brew.objects.get(coffee=coffee)
    context = {
        "coffee": coffee,
        "descriptors": ",".join(descriptors),
        "chemicals": chemicals
        }
    print coffee.name
    return render(request, 'coffee/coffee_details.html', context)


## Helper functions

# Compiles a list of all descriptors from the chemical compounds
def all_descriptors(result):
    all = []
    for chem in result.chemical_set.all():
        for d in chem.descriptors.split(", "):
            all.append(d)
    return all

# Computes the Jaccard Index score for a coffee
def get_score(survey, coffee):
    survey_likes = []
    survey_dislikes = []
    for s in survey:
        if "+" in s:
            survey_likes.append(s[1:])
        else:
            survey_dislikes.append(s[1:])

    coffee_list = coffee
    s_set = set(survey_likes)
    c_set = set(coffee_list) - set(survey_dislikes)
    # Kenya Kathakwa 0.195652173913
    return (len(s_set.intersection(c_set)) / float(len(s_set.union(c_set))))
