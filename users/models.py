from django.db import models
from django.contrib.auth.models import AbstractUser

from users.manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=260, error_messages={'unique': 'Email already exist'})
    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-id']

    def __str__(self):
        return self.email
    


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.email
    

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    img = models.ImageField(upload_to='events')
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    capacity = models.IntegerField()

    class Meta:
        db_table = 'events'
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['-id']

    def __str__(self):
        return self.name
    

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Prevent double registration

    def __str__(self):
        return f"{self.user.email} → {self.event.name}"