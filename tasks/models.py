from django.db import models

class Task(models.Model):
    due = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, default='Unnamed task')
    body = models.TextField(max_length=4096, blank=True, default='')
    completed = models.BooleanField(default=False, blank=True)
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} task"