from django.contrib import admin
from Scheduler.models import Teacher, TA, Admin, Courses, Labs, Person

admin.site.register(Person)
admin.site.register(Teacher)
admin.site.register(TA)
admin.site.register(Admin)
admin.site.register(Courses)
admin.site.register(Labs)
