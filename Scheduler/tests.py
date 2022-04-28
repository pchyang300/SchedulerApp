from django.test import TestCase
from django.test import Client
from .models import *

# Create your tests here.
class LoginTest(TestCase):
    # id, name, password, email, address, phoneNumber, permissionLevel
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        Person(name="admin2", password="admin2", email="admin@admin.com").save()

    def testLogin(self):
        r = self.client.post("/login/", {"email": "admin@admin.com", "password": "admin2"}, follow=True)
        self.assertRedirects(r, '/')  # First time logging in, should redirect to home page

    def testBadLogin(self):
        r = self.client.post("/login/", {"name": "admin@admin.com", "password": "wrongpass"}, follow=True)
        self.assertListEqual(r.context['messages'], ['Invalid password or email!'], "Should say the password is incorrect")


class AdminTest(TestCase):
    # id, name, password, email, address, phoneNumber, permissionLevel
    def setUp(self):
        self.client = Client()
        user_PersonExample = Teacher(id="001", name="Jim Smith", password="password2",
                                     email="jimsmith@uwm.edu", address="", phoneNumber="", permissionLevel=2)
        user_PersonExample.save()
        course_Example = Courses("English", "Jim Smith")
        course_Example.save()

    def testCreateAccount(self):
        r = self.client.post("/createuser/", {"email": "johnharb@uwm.edu", "firstname": "John",
                                             "lastname": "Harb", "password": "password1", "role": "TA"}, follow=True)
        testPerson = Person.objects.get(email="johnharb@uwm.edu")
        self.assertEqual(testPerson.name, "John Harb")
        self.assertEqual(testPerson.email, "johnharb@uwm.edu")
        self.assertEqual(testPerson.address, "")
        self.assertEqual(testPerson.phoneNumber, "")
        self.assertEqual(testPerson.permissionLevel, 2)
        self.assertEqual(testPerson.password, "password1")
        self.assertEqual(r.context['message'], "User Created Successfully!")
        # self.assertEqual(r.context["id"], ["001", "002"])
        # self.assertEqual(r.context["name"], [("Jim", "Smith"), ("John", "Harb")])
        # self.assertEqual(r.context["password"], ["password2", "password1"])
        # self.assertEqual(r.context["email"], ["jimsmith@uwm.edu", "johnharb@uwm.edu"])
        # self.assertEqual(r.context["address"], ["", ""])
        # self.assertEqual(r.context["phoneNumber"], ["", ""])
        # self.assertEqual(r.context["permissionLevel"], [2, 1])

    def testExistingAccount(self):
        r = self.client.post("/createuser/", {"email": "jimsmith@uwm.edu", "firstname": "Jim",
                                             "lastname": "Smith", "password": "password2", "role": "Instructor"},
                             follow=True)
        self.assertTrue(r.context["email"].contains("jimsmith@uwm.edu"))
        self.assertEqual(r.context['message'], "User With email alreadly found")

    def testCreateCourses(self):
        r = self.client.post("/createcourse/", {"coursename": "Math", "instructor": "Jim Smith"}, follow=True)
        self.assertFalse(r.context["courses"].contains("Math"))
        self.assertEqual(r.context['message'], "Course Created Successfully!")
        self.assertEqual(r.context["courses"], ["English", "Math"])

    def testExistingCourse(self):
        r = self.client.post("/createcourse/", {"coursename": "English", "instructor": "Jim Smith"}, follow=True)
        self.assertTrue(r.context["courses"].contains("English"))
        self.assertEqual(r.context['message'], "Course already exists")
        user_admin = Admin(name="admin", password="admin")
        user_admin.save()

class TATest(TestCase):
    # id, name, password, email, address, phoneNumber, permissionLevel
    def setUp(self):
        self.client = Client()
        user_ta = TA(name="misterTA", password="password")
        user_ta.save()
        Courses(owner="misterTA", name="Calculus", type="Discussion", hours="MW 12:00-13:30", section="802").save()
        Courses(owner="misterTA", name="Biology", type="Lab", hours="TTh 9:00-10:30", section="700").save()

    def test_ViewAllTAAssignments(self):
        c = self.client.session
        c["name"] = "misterTA"
        c.save()
        resp = self.client.post("/", {"view":"View"}, follow=True)
        self.assertEqual(resp.context["course"], ["Calculus Discussion Sect 802 MW 12:00-13:30",
                                                  "Biology Lab Sect 700 TTh 9:00-10:30"])

    def test_setEmail(self):
        c = self.client.session
        c["name"] = "misterTA"
        c.save()
        self.client.post("/info/", {"email": "misterta@uwm.edu"}, follow=True)
        self.assertEqual(TA.objects.get(name="misterTA").email, "misterta@uwm.edu",
                         "TA email was not set properly")

    def test_setPhoneNumber(self):
        c = self.client.session
        c["name"] = "misterTA"
        c.save()
        self.client.post("/info/", {"phoneNumber": "4142223333"})
        self.assertEqual(TA.objects.get(name="misterTA").phoneNumber, "4142223333", "TA phone was not properly added")

    def test_setAddress(self):
        c = self.client.session
        c["name"] = "misterTA"
        c.save()
        self.client.post("/info/", {"address": "244 Ceder Rd, Milwaukee, WI 66666"}, follow=True)
        self.assertEqual(TA.objects.get(name="misterTA").address, "244 Ceder Rd, Milwaukee, WI 66666",
                         "TA address was not set properly")


class TeacherTest(TestCase):
    # id, name, password, email, address, phoneNumber, permissionLevel
    def setUp(self):
        self.client = Client()
        user_teacher = Teacher(name="misterTA", password="password")
        user_teacher.save()

    def testViewCourseAssignments(self):
        pass

    def testEditContactInformation(self):
        pass


class TestPerson(TestCase):
    # id, name, password, email, address, phoneNumber, permissionLevel
    def setUp(self):
        self.clientTest = Client()
        person = Person(name="test", password="test", email="xyz@gmail.com", address="street",
                        phoneNumber="1-234-567-8977")
        person.save()

    def testDatabaseSave(self):
        checkPerson = Person.objects.get(name="test")
        pass

    def testDatabaseIncrementId(self):
        pass

    def testDatabaseSaveMultiple(self):
        pass

    def testDatabaseSaveDifferentPersons(self):
        pass


class TestHome(TestCase):

    def setUp(self):
        self.client = Client()
        teacher = Teacher(name="Jim Smith", password="password",
                          email="jimsmith@uwm.edu", address="", phoneNumber="", permissionLevel=2)
        teacher.save()
        admin = Admin(name="admin", password="admin", email="admin@uwm.edu", permissionLevel=3)
        admin.save()
        course = Courses(courseName='Course1', courseTeacher=teacher)
        course.save()
        course2 = Courses(courseName='Course2', courseTeacher=teacher)
        course2.save()

    def testPremissionIsSent(self):
        c = self.client.session
        c['email'] = "jimsmith@uwm.edu"
        c.save()
        r = self.client.get('')
        self.assertIn('role', r.context, msg="home needs a context variable role")

    def testCourse(self):
        c = self.client.session
        c['email'] = "jimsmith@uwm.edu"
        c.save()
        r = self.client.get('/')
        print('Content')
        print(r.context)
        self.assertEqual('Course1', r.context['courses'][0].courseName , msg="courses did not have professors course")

    def testAdminCourses(self):
        c = self.client.session
        c['email'] = "admin@uwm.edu"
        c.save()
        r = self.client.get('/')
        self.assertIn('Course2',  r.context['courses'][1].courseName, msg="admin view should include all the courses")
        
class TestProfile(TestCase):
    def setUp(self):
        self.client = Client()
        user_PersonExample = Teacher(name="Jim Smith", password="password2",
                                     email="jimsmith@uwm.edu", address="", phoneNumber="", permissionLevel=2)
        user_PersonExample.save()

    def testEditProfile(self):
        r = self.client.post("/editprofile/", {"email": "jimsmith@uwm.edu", "name": "Jim Smith", "password": "password2",
                                               "phoneNumber": "4141234567", "address": "123 main street"})
        testPerson = Person.objects.get(email="jimsmith@uwm.edu")
        self.assertEqual(testPerson.name, "Jim Smith")
        self.assertEqual(testPerson.address, "123 main street")
        self.assertEqual(testPerson.phoneNumber, "4141234567")
        self.assertEqual(testPerson.password, "password2")


class TestCreateLab(TestCase):
    def setUp(self):
        self.client = Client()
        user_PersonExample = TA(name="Jim Smith", password="password2",
                                     email="jimsmith@uwm.edu", address="", phoneNumber="")
        user_PersonExample.save()
        Lab_Example = Labs(labName = "Lab 902", assignedTAs = "Jim Smith")
        Lab_Example.save()
    def createLab(self):
        r = self.client.post("/createLab/", {"labSection": "Lab 901"})
        self.assertEqual(r.context['messages'], ["profile edited successfully"])

    def createExistingLab (self):
        r = self.client.post("/createLab/", {"labSection": "Lab 902"})
        self.assertEqual(r.context['messages'], ["Lab already exists"])

class TestEditCourse(TestCase):

    def testEditCourse(self):
        teacher = Teacher(name="Jay", email="Jay@uwm.edu")
        teacher.save()
        course = Courses(courseName="887", courseTeacher=teacher)
        course.save()
        teacher2 = Teacher(name="Jim Smith", email="JSmith@uwm.edu")
        teacher2.save()
        r = self.client.post("editcourse.html", {"coursename": "887", "newcoursename": "337", "instructor": "Jim Smith"}, follow=True)
        testCourse = Courses.objects.get(courseName="337")
        testPerson = Person.objects.get(email="jimsmith@uwm.edu")
        self.assertEqual(testPerson.name, "Jim Smith")
        self.assertEqual(testCourse.courseName, "337")
        self.assertEqual(r.context['messages'], ["course edit successful"])

class TestCourseAssignments(TestCase):

    def testAssignTAToCourse(self):
        r = self.client.post("assignTAToCourse.html", {"coursename": "337", "courseSection": "1", "taEmail": "ta@uwm"
                                                                                                             ".edu"},
                             follow=True)
        testCourse = Courses.objects.get(coursename="coursename")
        testCourseSection = Courses.labs.objects.get(labSection="labSection")
        testTA = Person.objects.get(taEmail="taEmail")
        self.assertEqual(testCourse.courseName, "337")
        self.assertEqual((testCourseSection.labName, "labSection"))
        self.assertEqual(testTA.email, "taEmail")
        self.assertEqual(r.context['message'], ["TA assignment successful"])

    def testAssignTAToLab(self):
        r = self.client.post("assignTAToLab.html", {"coursename": "337", "courseSection": "1", "taEmail": "ta@uwm"
                                                                                                          ".edu"},
                             follow=True)
        testCourse = Courses.objects.get(coursename="coursename")
        testCourseSection = Courses.labs.objects.get(labSection="labSection")
        testTA = Person.objects.get(taEmail="taEmail")
        self.assertEqual(testCourse.courseName, "337")
        self.assertEqual((testCourseSection.labName, "labSection"))
        self.assertEqual(testTA.email, "taEmail")
        self.assertEqual(r.context['message'], ["TA assignment successful"])
