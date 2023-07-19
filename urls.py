from django.urls import path
#from . import views
from .views import (
    TaskListView,
    task_view,
    task_data_view,
    save_task_view,
    topics_view,
    topic_displayed,
    all_tasks_view,
    tasks_chosen
)

app_name = 'main'

urlpatterns = [
    # path('', TaskListView.as_view(), name='main-view'),
    path('', task_view, name='task-view'),
    path('<pk>/data', task_data_view, name='task_data_view'),
    path('<pk>/save', save_task_view, name='save_view'),
    path('tasks-chosen/<pk>/save', save_task_view, name='save_view'),
    path('topics/', topics_view, name='topics_view'),
    path('topic/<t>', topic_displayed, name='topic_displayed'),
    path('all-tasks/', all_tasks_view, name='all_tasks_view'),
    path('tasks-chosen/', tasks_chosen, name='tasks_chosen'),
]
