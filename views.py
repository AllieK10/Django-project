from django.shortcuts import render
from django.http import HttpResponse
from . models import Task
from django.views.generic import ListView
from questions.models import Question, Answer
from results.models import Result
from collections import OrderedDict
from django.utils.http import urlencode
from operator import attrgetter


class TaskListView(ListView):
    model = Task
    template_name = 'main/main.html'


def task_view(request):
    current_user = request.user
    user_results = Result.objects.filter(user=current_user.id)
    return render(request, 'main/main.html', {'results': user_results})


def task_data_view(request, pk):
    tasks = Task.objects.get(pk=pk)
    questions = tasks.get_questions()
    print(questions)
    return render(request, 'main/task.html', {'tasks': tasks})


def save_task_view(request, pk):
    print(request)
    data = request.GET
    data_ = dict(data.lists())
    questions =[]
    for k in data_.keys():
        print('key: ', k)
        question = Question.objects.get(id=k)
        questions.append(question)
    print(questions)

    user = request.user
    tasks = Task.objects.get(pk=pk)
    score = 0
    multiplier = 100/tasks.number_of_questions
    results = []
    correct_answer = None

    for q in questions:
        print(data_)
        a_selected = data_[str(q.id)][0]
        print(q.id)
        print(a_selected)
        a = Answer.objects.get(id=int(a_selected))
        if a.correct:
            score += 1
            correct_answer = a
        results.append({'correct_answer': correct_answer, 'answered': a, 'question': q})

    score_ = score * multiplier
    result, created = Result.objects.get_or_create(task=tasks, user=user, defaults={'score': 0})
    print(result)
    result.score = score_
    result.save()

    if score_ >= tasks.score_to_pass:
        return render(request, 'main/results.html', {'passed': True, 'score': score_, 'results': results})
    else:
        return render(request, 'main/results.html', {'passed': False, 'score': score_, 'results': results})


def topics_view(request):
    topics = Task.objects.values_list('topic')
    print(topics)
    topics_list = []
    for t in topics:
        print(t)
        topics_list.append(t[0])

    topics_list = list(OrderedDict.fromkeys(topics_list).keys())
    print(topics_list)

    return render(request, 'main/topics.html', {'topics': topics_list})


def topic_displayed(request, t):
    tasks = Task.objects.filter(topic=t)
    print(tasks)
    return render(request, 'main/topic_tasks.html', {'tasks': tasks})


def all_tasks_view(request):
    tasks = Task.objects.all()
    print(tasks) #returned a query set of tasks
    task_list = []
    questions = []
    for i in tasks:
        print(i.name)
        task_list.append(i)
    return render(request, 'main/all_tasks.html', {'tasks': task_list})


def tasks_chosen(request):
    current_user = request.user
    user_results = Result.objects.filter(user=current_user.id) #getting current user's result
    if not user_results:
        all_tasks = Task.objects.filter(difficulty='easy')
    else:
        for u in user_results:
            print(u.score)
        res = min(user_results, key=attrgetter('score')) #choosing minimal result among all
        weak_topic_res=[]
        for w in user_results:
            if res.task.topic == w.task.topic:
                weak_topic_res.append(w)

        best_res = max(weak_topic_res, key=attrgetter('score'))
        res_pass = float(res.task.score_to_pass)

        if res.score < res_pass: #comparing user's result with score_to_pass of that task
            print("did not pass") #if user's score is less, then they haven't passed the test
            if best_res.score > res_pass:
                all_tasks = [res.task]
            else:
                all_tasks = Task.objects.filter(topic=res.task.topic, difficulty='easy').exclude(pk=res.task.pk) #a list of easy tasks to choose from

        else:
            print("passed") #otherwise they've passed
            # choosing tasks on the same topic and with the same difficulty level, except for the one they've already done
            all_tasks = Task.objects.filter(topic=res.task.topic, difficulty=res.task.difficulty).exclude(pk=res.task.pk)

        if not all_tasks:
            all_tasks = [res.task]

    return render(request, 'main/task.html', {'tasks': all_tasks[0]})
