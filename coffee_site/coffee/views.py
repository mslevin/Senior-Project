from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from .models import Question, Coffee
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
    output = request.POST
    question_list = Question.objects.order_by('-pub_date')
    for question in question_list:
        print question.question_text, " : ", request.POST[str(question.id)]
    return HttpResponse(output)

def taste(request):
    return HttpResponse("This is where the coffee tasting will happen.")

def recommend(request):
    return HttpResponse("This is where you will get your coffee recommendations.")

def coffees(request):
    coffee_list = Coffee.objects.all()
    context = {'coffee_list': coffee_list}
    return render(request, 'coffee/coffees.html', context)
