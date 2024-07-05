from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from task.models import Task

class UserManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        # if not email:
        #     raise ValueError('Users must have an email address')
        kwargs['email'] = self.normalize_email(kwargs.get('email'))
        user = self.model(**kwargs)
        print(kwargs)
        print(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        user = self.create_user(password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()

class PushRecord(models.Model):
    type = models.CharField(max_length=255, blank=False, choices=[
        ('START', 'Start'),
        ('END', 'End'),
        ('RESUME', 'Resume'),
        ('SUSPEND', 'Suspend'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class TaskRecord(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'user')
    punch = models.ForeignKey(PushRecord, on_delete=models.CASCADE)

    objects = models.Manager()
