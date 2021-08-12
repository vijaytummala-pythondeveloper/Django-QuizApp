from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from requests import get
from random import shuffle
from .models import UserData

# Create your views here.


def home_page(request):
    return render(request,'index.html')


def welcome_page(request):
    return render(request,'login.html')


def login_user(request):
    username = request.POST['login_username']
    password = request.POST['login_password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request,'user_home.html')
    else:
        return render(request,'login.html',{'msg':'User Not Found please Register or use guest'})


def register_user(request):
    username = request.POST['register_username']
    email = request.POST['register_email']
    password = request.POST['register_password']
    User.objects.create_user(username = username,email=email,password=password)
    return render(request, 'login.html',{'reg_msg':'User created successfully please login'})


def get_categories(request):
    res_obj = UserData()
    res_obj.user_name = request.user
    res_obj.correctly_answered = 0
    res_obj.wrongly_answered = 0
    res_obj.questions_answered = 0
    res_obj.correct_answer = None
    res_obj.ques_count = 0
    res_obj.save()
    return render(request,'quiz_home.html',{'res_obj':res_obj})

def get_questions(request):
    ques_id = int(request.GET['ques_id'])
    res_obj = UserData.objects.get(pk=ques_id)
    res_obj.ques_count+= 1
    if res_obj.ques_count <= 10:
        category_dict = {
            'GeneralKnowledge':9,
            'Computers':18,
            'History':23,
            'Maths':19
        }
        cat = request.GET['quiz_category']
        cat1 = category_dict[cat]
        question = get(f'https://opentdb.com/api.php?amount=1&category={cat1}&difficulty=easy&type=multiple')
        json_data = question.json()
        category = json_data['results'][0]['category']
        question = json_data['results'][0]['question']
        correct_answer = json_data['results'][0]['correct_answer']
        incorrect_answers = json_data['results'][0]['incorrect_answers']
        incorrect_answers.append(correct_answer)
        shuffle(incorrect_answers)
        options = incorrect_answers

        res_obj.question = question
        res_obj.quiz_cat = cat
        res_obj.correct_answer = correct_answer
        res_obj.save()
        context = {
            'category':category,
            'question':question,
            'options':options,
            'res_obj':res_obj
        }
        return render(request,'quiz_template.html', context)
    else:
        context = {
            'res_obj':res_obj
        }
        return render(request,'results.html',context)

def update_question(request):
    ques_id = int(request.POST['ques_id'])
    ques_obj = UserData.objects.get(pk=ques_id)
    ques_obj.questions_answered += 1
    print(request.POST['selected_option'])
    print(ques_obj.correct_answer)
    if request.POST['selected_option'] == ques_obj.correct_answer:
        answered = True
        ques_obj.correctly_answered += 1
        ques_obj.save()
    else:
        answered = False
        ques_obj.wrongly_answered += 1
        ques_obj.save()
    context = {
            'your_answer':request.POST['selected_option'],
            'answered':answered,
            'ques_obj':ques_obj
        }
    return render(request,'showoutput.html',context)

def go_to_home(request):
    return render(request, 'user_home.html')

def see_records(request):
    obj = UserData.objects.filter(user_name=request.user)
    return render(request,'show_records.html',{'obj':obj})

def logging_out(request):
    logout(request)
    return render(request,'login.html')