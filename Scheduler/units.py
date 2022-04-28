import Scheduler
from .models import *


class PersonalInfo:

    def __init__(self, user):
        self.user = user

    def phoneNumber(self):
        return self.user.phoneNumber

    def mailAddress(self):
        return self.user.address

    def setPhoneNumber(self, phoneNumber):
        self.user.phoneNumber = phoneNumber

    def setMailAddress(self, address):
        self.user.address = address


class User:

    def __init__(self, user):
        self.user = user

    def getName(self):
        return self.user.name

    def setName(self, name):
        self.user.name = name

    def getEmail(self):
        return self.user.email

    def getPermissionLevel(self):
        return self.user.permissionLevel

    def courseAssignedTo(self):
        return Courses.objects.filter(CourseInstructor=self.user)

    def getPersonalInfo(self):
        return PersonalInfo(self.user)


class ClassTA(User):

    def __init__(self, ta):
        if not ta or type(ta) is not Scheduler.models.TA:
            raise TypeError
        self.user = User(ta)

    # methods for TA


class ClassTeacher(User):

    def __init__(self, teacher):
        if not teacher or type(teacher) is not Scheduler.models.teacher:
            raise TypeError
        self.user = User(teacher)

class ClassAdmin(User):

    def __init__(self, admin):
        if not admin or type(admin) is not Scheduler.models.admin:
            raise TypeError
        self.user = User(admin)

    def getName(self):
        return self.user.name

    def setName(self, name):
        self.user.name = name

    def getAddress(self):
        return self.user.address

    def setAddress(self, address):
        self.user.address = address

    def getPhoneNumber(self):
        return self.user.phoneNumber

    def setPhoneNumber(self, phoneNumber):
        self.user.phoneNumber = phoneNumber
