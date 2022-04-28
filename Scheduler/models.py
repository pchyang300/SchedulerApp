from django.db import models


# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=40, unique=True)
    address = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=20)
    permissionLevel = models.SmallIntegerField(editable=False)

    def __str__(self):
        return self.name + "- Permission Level: " + str(self.permissionLevel)


class TA(Person):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('permissionLevel').default = 1
        super(TA, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True


class Teacher(Person):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('permissionLevel').default = 2
        super(Teacher, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True


class Admin(Person):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('permissionLevel').default = 3
        super(Admin, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True  # Keeps all on same table, Person table and just changes the permission level.


class Courses(models.Model):
    courseName = models.CharField(max_length=20, unique=True)
    courseTeacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.courseName + " Taught by " + self.courseTeacher.name

class Labs(models.Model):
    labName = models.CharField(max_length=30)
    assignedTAs = models.ManyToManyField(TA)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.labName + " Hosted by " + self.assignedTAs.name
