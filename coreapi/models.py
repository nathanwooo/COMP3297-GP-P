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

