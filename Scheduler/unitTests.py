from django.test import TestCase
from .models import *
from .units import *


class TestUser(TestCase):

    def setUp(self):
        person = Person(name="Teacher", password="Teacher", email="Teacher@gmail.com",
                         address="address 31st 54342", phoneNumber=123456, permissionLevel=3)
        person.save()
        self.user = User(person)

    def testgetName(self):
        self.assertEqual("Teacher", self.user.getName())

    def testsetName(self):
        self.user.setName("newName")
        self.assertEqual("newName", self.user.getName())

    def testgetEmail(self):
        self.assertEqual("Teacher@gmail.com", self.user.getEmail())

    def testpermissionlevel(self):
        self.assertEqual(3, self.user.getPermissionLevel())

    def testCourseAssingedTo(self):
        self.assertEqual(3, self.user.getPermissionLevel())


class TestPersonalInfo(TestCase):
    def setUp(self):
        person = Person(name="Teacher", password="Teacher", email="Teacher@gmail.com",
                        address="address 31st 54342", phoneNumber=123456, permissionLevel=3)
        person.save()
        self.user = User(person)

    def testPhoneNumber(self):
        self.assertEqual(123456, self.user.getPersonalInfo().phoneNumber())

    def testAddress(self):
        self.assertEqual("address 31st 54342", self.user.getPersonalInfo().mailAddress())

    def testChangePhoneNumber(self):
        self.user.getPersonalInfo().setPhoneNumber(11111)
        self.assertEqual(11111, self.user.getPersonalInfo().phoneNumber())

    def testChangeMailAddress(self):
        self.user.getPersonalInfo().setMailAddress("New mail Address")
        self.assertEqual("New mail Address", self.user.getPersonalInfo().mailAddress())

class TestTA(TestCase):
    def setUp(self):
        self.ta = TA(name="TA")
        self.ta.save()
        self.teacher = Teacher(name="Teacher")
        self.teacher.save()

    def testWrongUser(self):
        with self.assertRaises(TypeError):
            ClassTA(self.teacher)

    def testCorrectUser(self):
        ta = ClassTA(self.ta)
        self.assertEqual("TA", ta.user.getName())

class TestAdmin(TestCase):
    def setUp(self):
        self.admin = Admin()

    def test_getName(self):
        self.admin.name = "Arnold"
        name = self.admin.getName()
        self.assertEqual(name, "Arnold")

    def test_setName(self):
        self.admin.setName("Mike")
        self.assertEqual(self.admin.name, "Mike")

    def test_getAddress(self):
        self.admin.address = "123 Evergreen Rd, Milwaukee, WI 55555"
        address = self.admin.getAddress()
        self.assertEqual(address, "123 Evergreen Rd, Milwaukee, WI 55555")

    def test_setAddress(self):
        self.admin.setAddress("321 North Rd, Milwaukee, WI 55555")
        self.assertEqual(self.admin.address, "321 North Rd, Milwaukee, WI 55555")

    def test_getPhone(self):
        self.admin.phoneNumber = "5556667777"
        phone = self.admin.getPhoneNumber()
        self.assertEqual(phone, "5556667777")

    def test_setPhone(self):
        self.admin.setPhoneNumber("1234567899")
        self.assertEqual(self.admin.phoneNumber, "1234567899")


