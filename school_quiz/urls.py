from django.urls import path, include

from school_quiz import views
app_name = 'school_quiz'

urlpatterns = [
    path('', views.home_page),
    path('welcome_page',views.welcome_page,name='welcome'),
    path('login_user',views.login_user),
    path('register_user',views.register_user),
    path('get_categories',views.get_categories,name='get_categories'),
    path('get_questions',views.get_questions),
    path('updateques',views.update_question),
    path('gotohome',views.go_to_home),
    path('see_records',views.see_records,name='see_records'),
    path('logging_out',views.logging_out,name='logging_out')

]