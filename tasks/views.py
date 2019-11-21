import datetime
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status


from tasks.models import Task
from tasks.permissions import IsOwnerOrReadOnly
from tasks.serializers import TaskSerializer, UserSerializer


class TaskList(APIView):
    """
    List all tasks on a given date (default to today), or create a new task.
    Optionally take a GET parameter 'date' in ISO 8601 format.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]

    def get(self, request, format=None):
        try:
            date = parse_date(request.query_params['date'])
        except KeyError:
            date = datetime.date.today()
        except ValueError as e:
            return Response(f"Invalid date: {str(e)}", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Invalid date", status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(due=date)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    """
    Retrieve, update or delete a task instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer