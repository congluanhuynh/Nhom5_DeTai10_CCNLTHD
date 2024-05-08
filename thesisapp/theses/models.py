from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['id']


class Department(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Major(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=10, null=False, unique=True)
    phone_num = models.CharField(max_length=10)
    school_year = models.IntegerField()
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Council(BaseModel):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='CouncilMembership')

    def __str__(self):
        return self.name


class CouncilMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.council.name} ({self.role})"


class Thesis(BaseModel):
    name = models.CharField(max_length=200)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    students = models.ManyToManyField('Student', blank=False, related_name='students_group')
    users = models.ManyToManyField('User', blank=False,related_name='instructors')

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    council = models.ForeignKey(Council, on_delete=models.RESTRICT, null=False)
    thesis = models.ForeignKey(Thesis, on_delete=models.RESTRICT, null=False)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)


class Score(Interaction):
    score_value = models.SmallIntegerField(default=0)








