from django.shortcuts import render,redirect
from django import forms

import random
import os

# TODO: Add Login page

class AnswerKey:
    """ Container for questions and their respective answers 
    """

    def __init__(self, num, answers):
        self.id = int(num)
        self.answers = []
        for i in range(0, 8):
            assert answers[i] == "S" or answers[i] == "N"
            answer_head = "abcdefgh"
            self.answers.append((answer_head[i], answers[i]))

    def __repr__(self):
        return "AnswerKey{{id={}, answers={}}}".format(self.id, self.answers)



def answer_keys_from_file(filename):
    """ Reads the answer keys file from filename
        :parameter filename path string to answerkeys file
    """
    qa = []
    with open(filename, 'r') as aks:
        line = 1
        for ak in aks:
            ak_split = ak.strip().split()
            try:
                qa.append(AnswerKey(ak_split[0], ak_split[1]))
            except (IndexError, AssertionError):
                print("Couldn't read file. Input is malformed.")
                print("Line {}: {}".format(line, ak.strip()))
            line += 1
    
    return qa


def check_answers(ak, option, given_answer):
  """ Queries for answers and checks them
    :parameter ak An AnswerKey object
    :parameter num The number of answers to ask. Must be in (0,8]
    :parameter rand Whether the answers should be asked in random order """
  
  # legacy support (answer format changed)
  if given_answer.upper() == "A":
    given_answer = "S"
  elif given_answer.upper() == "D":
    given_answer = "N"

  for i in ak.answers:
    if i[0] == option and i[1] == given_answer:
      return True
  return False

class ModeForm(forms.Form):
  """ModeForm definition."""
  mode = forms.IntegerField(min_value=1,max_value=3)
  start = forms.IntegerField(min_value=1,max_value=len(answer_keys_from_file("quiz/answerkeys.txt")),required=False)


def ModeView(request):
  if request.method == "POST":
    form = ModeForm(request.POST)
    return render(request,"templates/questions.html",{"form":form})
  else:
    form = ModeForm()
    return render(request,"mode.html",{"form":form})





from django.http import JsonResponse 


def ajaxQuestionsView(request,mode):
    aks = answer_keys_from_file("quiz/answerkeys.txt")
    mode = int(mode)
    if mode == 1:
      ak = random.sample(aks,k=4)
      questions = {}
      for a in ak:
        ak_seq = random.sample(range(0,8),k=4)
        questions[a.id] = []
        for i in ak_seq:
          questions[a.id].append(a.answers[i][0])
    
    elif mode == 2 or mode == 3:
      start = int(request.POST['start'])
      end = start + 8 if start + 8 < len(aks) else len(aks)
      ak = []
      for i in range(start,end):
        ak.append(aks[i-1])
      questions = {}
      for a in ak:
        if mode == 2:
          ak_seq = random.sample(range(0,8),k=8)
        elif mode == 3:
          ak_seq = range(0,8)
        questions[a.id] = []
        for i in ak_seq:
          questions[a.id].append(a.answers[i][0])     

    else:
        questions["error"] = "Wrong Mode"
    return JsonResponse({"questions":questions,"question_keys":list(questions)})



def ajaxAnswer(request):
  aks = answer_keys_from_file("quiz/answerkeys.txt")
  answer = None
  for key,item in request.POST.items():
    try:
      number,option = key.split("-")
      number = int(number)
      answer = check_answers(aks[number], option, item)
    except:
      continue

  # return JsonResponse({"answer":answer})
  return JsonResponse({"answer":True})


def QuestionTemplate(request,mode):
  return render(request, "questions.html",{"mode":mode})