from django.db import models
from authentication.models import User

# Create your models here.


class Room(models.Model):
    room_id = models.CharField(max_length=50)
    lecture = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.room_id
    
    
    
class Students(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    student = models.ForeignKey(User,on_delete=models.CASCADE)