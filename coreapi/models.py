from django.db import models


# Create your models here.
class Venue(models.Model):
    TYPES = (
        ('LT', 'Lecture Theatre'),
        ('CR', 'Classroom'),
        ('TR', 'Tutorial Room'),
    )
    venuecode = models.CharField(max_length=20, primary_key=True)
    location = models.CharField(max_length=150)
    type = models.CharField(max_length=2, choices=TYPES)
    capacity = models.IntegerField()

    def __str__(self):
        return self.venuecode

class HkuMember(models.Model):
    hku_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=150)
    venues = models.ManyToManyField(Venue, through='Visit')

    def __str__(self):
        return f'{self.hku_id} {self.name}'

class Visit(models.Model):
    EVENT = (
        ('I', 'Entry'),
        ('O', 'Exit'),
    )
    member = models.ForeignKey(HkuMember, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    time = models.DateTimeField()
    event = models.CharField(max_length=1, choices=EVENT)

    def __str__(self):
        return f'{self.time} {self.event} {self.member.hku_id} {self.venue.venuecode}'

class App_User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=40,blank=True)
    def __str__(self):
        return f'{self.username} {self.first_name} {self.last_name} {self.email}'