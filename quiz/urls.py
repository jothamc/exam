from django.urls import path
from .views import ajaxQuestionsView,ModeView,ajaxAnswer,QuestionTemplate,CreateUser
from django.contrib.auth.views import LoginView

app_name = "quiz"
urlpatterns = [
    path("",ModeView,name="mode"),
    path("create-account",CreateUser,name="register"),
   	path("login/", LoginView.as_view(),name="login"),
    path("mode/<mode>/",QuestionTemplate,name="question"),
    path("ajax-question/<mode>/",ajaxQuestionsView,name="questions"),
    path("ajax-answer/",ajaxAnswer,name="ajax"),
]
