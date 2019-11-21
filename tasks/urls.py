from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks import views

app_name = 'tasks'
urlpatterns = [
    path('tasks/', views.TaskList.as_view(), name='taskslist'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='tasksdetail'),
    path('users/', views.UserList.as_view(), name='userslist'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='usersdetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)