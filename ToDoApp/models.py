from django.db import models
from accounts.models import Account
# Create your models here.


class Work(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    journal = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)

    def __str__(self):
        return self.title
