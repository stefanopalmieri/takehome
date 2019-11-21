import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from tasks.models import Task

class TastModelTests(TestCase):
    def test_task_to_string(self):
        """
        Return properly formatted string for task string method
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)

        self.assertEqual(str(task), "test task")

class TaskListViewTests(TestCase):
    def test_no_tasks(self):
        """
        If no tasks exist, return an empty list in API response
        """
        client = APIClient()
        response = client.get(reverse('tasks:taskslist'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_task_list_create_authenticated(self):
        """
        Create a task through API while authenticated
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()

        client = APIClient()
        client.force_authenticate(user=user)
        task_dict = {
                'due': date.isoformat(),
                'body': 'This is a test task',
                'title': 'test',
                'owner': 'basic',
                'completed': False
            }
        response = client.post(reverse('tasks:taskslist'), task_dict)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, task_dict)

    def test_task_list_create_unauthenticated(self):
        """
        Create a task through API while not authenticated
        """

        date = datetime.date.today()

        client = APIClient()
        task_dict = {
                'due': date.isoformat(),
                'body': 'This is a test task',
                'title': 'test',
                'owner': 'basic',
                'completed': False
            }
        response = client.post(reverse('tasks:taskslist'), task_dict)

        self.assertEqual(response.status_code, 403)

    def test_task_list_today_default(self):
        """
        Return existing tasks due today in default API response
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        response = client.get(reverse('tasks:taskslist'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            [{
                'due': date.isoformat(),
                'body': 'This is a test task',
                'title': 'test',
                'owner': 'basic',
                'completed': False
            }])

    def test_task_list_not_today_default(self):
        """
        Do not return existing tasks not due today in default API response
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today() - datetime.timedelta(days = 1)
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        response = client.get(reverse('tasks:taskslist'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_task_list_not_today_not_default(self):
        """
        Existing tasks due tomorrow are returned in API response
        when tomorrow's date is passed as a query parameter
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today() + datetime.timedelta(days = 1)
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        querystring = urlencode({"date":date.isoformat()})
        response = client.get(f"{reverse('tasks:taskslist')}?{querystring}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            [{
                'due': date.isoformat(),
                'body': 'This is a test task',
                'title': 'test',
                'owner': 'basic',
                'completed': False
            }])

    def test_task_list_invalid_date(self):
        """
        A 400 bad request response is returned in API response
        when the date query parameter is invalid
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        querystring = urlencode({"date":"2019-13-01"})
        response = client.get(f"{reverse('tasks:taskslist')}?{querystring}")

        self.assertEqual(response.status_code, 400)

class TaskDetailViewTests(TestCase):
    def test_task_detail_get_existing(self):
        """
        Return an existing task in detail API response
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        response = client.get(reverse('tasks:tasksdetail', args=[task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            {
                'due': date.isoformat(),
                'body': 'This is a test task',
                'title': 'test',
                'owner': 'basic',
                'completed': False
            })

    def test_task_detail_get_nonexisting(self):
        """
        A 404 is returned in detail API response for a get on a nonexistant task
        """
        client = APIClient()
        response = client.get(reverse('tasks:tasksdetail', args=[0]))

        self.assertEqual(response.status_code, 404)

    def test_task_detail_put_existing(self):
        """
        Update an existing task and return detail API response
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.put(reverse('tasks:tasksdetail', args=[task.pk]),
                              {"completed": True})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            {
                'due': date.isoformat(),
                'body': 'This is a test task',
                'title': 'test',
                'owner': 'basic',
                'completed': True
            })

    def test_task_detail_put_existing_unauthenticated(self):
        """
        A 403 forbidden response is returned in detail API response
        when an unauthenticated put occurs on an existing task
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        response = client.put(reverse('tasks:tasksdetail', args=[task.pk]),
                              {"completed": True})

        self.assertEqual(response.status_code, 403)

    def test_task_detail_put_nonexisting(self):
        """
        A 404 is returned in detail API response for put on a nonexistant task
        """
        username = "basic"
        user = User.objects.create(username=username)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('tasks:tasksdetail', args=[0]))

        self.assertEqual(response.status_code, 404)

    def test_task_detail_delete_existing(self):
        """
        A 204 No Content response is returned in detail API response
        when an existing task is deleted
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(reverse('tasks:tasksdetail', args=[task.pk]))

        self.assertEqual(response.status_code, 204)

    def test_task_detail_delete_existing_unauthenticated(self):
        """
        A 403 forbidden response is returned in detail API response
        when an unauthenticated delete occurs on an existing task
        """
        username = "basic"
        user = User.objects.create(username=username)
        date = datetime.date.today()
        task = Task.objects.create(title="test", body="This is a test task",
                                   completed=False, owner=user, due=date)
        task.save()

        client = APIClient()
        response = client.delete(reverse('tasks:tasksdetail', args=[task.pk]))

        self.assertEqual(response.status_code, 403)

class UserListCreateViewTests(TestCase):
    def test_user_list(self):
        """
        Return existing users in user list response
        """
        username = "basic"
        user = User.objects.create(username=username)
        user.save()

        client = APIClient()
        response = client.get(reverse('tasks:userslist'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "username": "basic",
                        "tasks": []
                    }
                ]
            }
        )

    def test_user_create_authenticated(self):
        """
        Create a user
        """
        username = "admin"
        user = User.objects.create(username=username)
        user.save()

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(reverse('tasks:userslist'),
            {
                "username": "basic",
                "tasks": []
            })

        self.assertEqual(response.status_code, 201)

    def test_user_create_unauthenticated(self):
        """
        Create a user while not authenticated
        """
        client = APIClient()
        response = client.post(reverse('tasks:userslist'),
            {
                "username": "basic",
                "tasks": []
            })

        self.assertEqual(response.status_code, 403)

class UserDetailViewTests(TestCase):
    def test_user_detail(self):
        """
        Return a user detail in response
        """
        username = "basic"
        user = User.objects.create(username=username)
        user.save()

        client = APIClient()
        response = client.get(reverse('tasks:usersdetail', args=[user.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            {
                "id": 1,
                "username": "basic",
                "tasks": []
            }
        )