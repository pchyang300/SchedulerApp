import unittest

import self as self
from django.test import TestCase
from django.test import Client
from models import Person, TA, Admin, Teacher, Student

self.client = Client()
user_teacher = Teacher(name="Professor", password="password")
user_teacher.save()

randomStudent =Student(name="RandomStudent", email="studentemail@email.com")
randomStudent.save()

randomTA = TA(name="NumOneTA", email = "TA@email.com")
randomTA.save()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

class addClass(unittest.TestCase):

    def test_add_class(self):
        r = self.client.post("/createcourse/", {"coursename": "Course101", "instructor": "Professor"}, follow=True)
        self.assertTrue(r.context["courses"].contains("Course101"))
        self.assertEqual(r.context["courses/Course101/assignedInstructor"],"Professor")
        self.assertEqual(r.context['message'], "Course Created Successfully!")

    def test_add_existing_class(self):

        r = self.client.post("/createcourse/", {"coursename": "Course101", "instructor": "Professor"}, follow=True) #should something be added here to differentiate between existing and not? Perhaps a test database object?
        self.assertTrue(r.context["courses"].contains("Course101"))
        self.assertEqual(r.context['message'], "This course exists already!")

class assignTA(unittest.TestCase):
    def test_assign_TA(self):
        r = self.client.post("/addta/",{"coursename": "Course101", "instructor": "Professor", "TA":"TheTA1"}, follow=True)
        self.assertTrue(r.context["Course101"].contains("TheTA1"))
        self.assertEqual(r.context["courses/Course101/assignedTA"],"TheTA1")
        self.assertEqual(r.context['message'], "TA Assigned Successfully!")

class dataAccess(unittest.TestCase):
    def get_student_email(self):

        self.assertEqual(Student.objects.get(name="randomStudent").email, "student@email.com")

    def get_TA_email(self):
        self.assertEqual(TA.objects.get(name="NumOneTA").email, "TA@email.com")


class editData(unittest.TestCase):
    def edit_student_email(self):
        r = self.client.post("/edit/email", {"user": "randomStudent", "email": "newemail@email.com"}, follow=True)
        self.assertEqual(r.context["/email/"], "newemail@email.com")

    def edit_TA_email(self):
        r = self.client.post("/edit/email", {"user": "TheTA1", "email": "newemail@email.com"}, follow=True)
        self.assertEqual(r.context["/email/"], "newemail@email.com")

    def edit_admin_email(self):

    def edit_teacher_email(self):
        r = self.client.post("/edit/email", {"user": "OtherProfessor", "email": "newemail@email.com"}, follow=True)
        self.assertNotEqual(r.context["/email/"], "newemail@email.com")

    def edit_my_email(self):
        r = self.client.post("/edit/email", {"user": "Professor", "email": "newemail@email.com"}, follow=True)
        self.assertEqual(r.context["/email/"], "newemail@email.com")

if __name__ == '__main__':
    unittest.main()
