from django.db import models
import django.utils as du

class Race(models.Model):
    date = models.DateField(default=du.timezone.now)
    track = models.CharField(max_length=25)
    raceNumber = models.IntegerField(default=0)
    surface = models.CharField(max_length=25)
    distance = models.CharField(max_length=50)
    condition = models.CharField(max_length=25)
    fieldSize = models.IntegerField(default=0)
    maidens = models.BooleanField(default=False)
    firstCall = models.IntegerField(default=0)
    secondCall = models.IntegerField(default=0)

    def __str__(self):
        return "{} {} {}".format(self.date, self.track, self.raceNumber)
    
    class Meta:
        constraints = [
                models.UniqueConstraint(fields=["date", "track", "raceNumber"], name='unique_race')]