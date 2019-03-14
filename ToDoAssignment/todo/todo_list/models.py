from django.db import models
from datetime import datetime

# Create your models here.
class List(models.Model):
    item=models.CharField(max_length=200)
    list_date=models.DateTimeField(default=datetime.now)
    from_time=models.TimeField()
    to_time=models.TimeField()
    completed=models.BooleanField(default=False)

    def __str__(self):
        return self.item+' | '+ str(self.list_date) +' | '+str(self.completed)+'|'+str(self.from_time)+'|'+str(self.to_time)