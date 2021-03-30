from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Machine(models.Model):
    partNumber = models.IntegerField()
    operator = models.CharField(max_length=100)
    manufacturedYear = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




JOBS = (
    ('S', 'Schedualed'),
    ('U', 'Unschedualed'),
)

class Maintenance(models.Model):
    date = models.DateField('when are we doing maintenance')
    job = models.CharField(
        max_length=1,
        
        choices = JOBS,
        default = JOBS[0][0]
    )
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_job_display()} on {self.date}"