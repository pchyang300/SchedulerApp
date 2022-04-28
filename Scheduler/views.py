from django.shortcuts import render, redirect
from django.views import View
from .models import *

class Home(View):
    def get(self, request):
        if 'email' not in request.session:
            return render(request, "login.html", {"messages": ["Log in to continue"]})
        person = Person.objects.get(email=request.session['email'])
        if person.permissionLevel == 3:
            courses = Courses.objects.all()
        elif person.permissionLevel == 2:
            courses = Courses.objects.filter(courseTeacher=person)
        else:
            courses = []
            labs = Labs.objects.filter(assignedTAs=person).all()
            for lab in labs:
                courses.append({
                    'course': lab.course,
                    'labName': lab.labName
                })
        return render(request, 'home.html', {"role": person.permissionLevel, 'courses': courses})


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        try:
            person = Person.objects.get(email=request.POST['email'])
            if person.password != request.POST['password']:
                return self.returnBadRender(request)
            else:
                request.session['email'] = person.email
                request.session['role'] = person.permissionLevel
                return redirect("/")
        except:
            return self.returnBadRender(request)

    def returnBadRender(self, request):
        return render(request, "login.html", {"messages": ["Invalid password or email!"]})


class CreateUser(View):
    def get(self, request):
        user = Person.objects.get(email=request.session['email'])
        if user.permissionLevel != 3:
            return redirect('/permissiondenied')
        return render(request, 'creatuser.html', {'role': user.permissionLevel})

    def post(self, request):
        name = request.POST['firstname'] + " " + request.POST['lastname']
        email = request.POST['email']
        try:
            Person.objects.get(name=name, email=email)
            return render(request, "creatuser.html", {"messages": ["User already exists"], 'role': 3})
        except:
            m = request.POST.get('role')
            if m == 'admin':
                adminPerson = Admin(name=name, password=request.POST['password'],
                                    email=request.POST['email'])
                adminPerson.save()
            elif m == 'teacher':
                teacherPerson = Teacher(name=name, password=request.POST['password'],
                                        email=request.POST['email'])
                teacherPerson.save()

            else:
                TAPerson = TA(name=name, password=request.POST['password'],
                              email=request.POST['email'])
                TAPerson.save()
            return render(request, "creatuser.html", {"messages": ["User Created Successfully"], "role": 3})


class CreateCourse(View):
    def get(self, request):
        users = Teacher.objects.filter(permissionLevel=2).all()
        user = Person.objects.get(email=request.session['email'])
        if user.permissionLevel != 3:
            return redirect('/permissiondenied')
        return render(request, 'createcourse.html', {'role': 3, 'users': users})

    def post(self, request):
        # if teacher doesnt exist in the database return error
        try:
            t = Teacher.objects.get(email=request.POST["instructor"])
        except:
            return render(request, "createcourse.html", {"messages": ["teacher with that name doesn't exist"], 'role': 3})
        n = request.POST["coursename"]
        users = Teacher.objects.filter(permissionLevel=2).all()
        try:
            Courses.objects.get(courseName=n)
        except:
            newCourse = Courses(courseTeacher=t, courseName=n)
            newCourse.save()
            return render(request, "createcourse.html", {"messages": ["created course successfully"], 'role': 3, 'users': users})
        else:
            return render(request, "createcourse.html", {"messages": ["course already exists"], 'role': 3, 'users': users})

class EditCourse(View):
    def get(self, request, coursename=None):
        user = Person.objects.get(email=request.session['email'])
        teachers = Person.objects.filter(permissionLevel=2).all()
        if user.permissionLevel != 3 and user.permissionLevel != 2:
            return redirect('/permissiondenied')
        if not coursename:
            return render(request, "editcourse.html",
                          {'role': user.permissionLevel, 'courses': Courses.objects.all(), 'teachers': teachers,
                           'defaultTeacher': ''})
        else:
            defaultTeacher = Courses.objects.get(courseName=coursename).courseTeacher
            teachers = teachers.exclude(name=defaultTeacher.name)
            return render(request, "editcourse.html",
                          {'role': user.permissionLevel, 'coursename': coursename, 'teachers': teachers,
                           'defaultTeacher': defaultTeacher})

    def post(self, request):
        try:
            Courses.objects.get(courseName=request.POST['newcoursename'])
            return redirect('/editcourse/' + request.POST['coursename'])
        except:
            course = Courses.objects.get(courseName=request.POST['coursename'])
            course.courseName = request.POST['newcoursename']
            course.courseTeacher = Person.objects.get(email=request.POST['newinstructor'])
            course.save()
            return redirect('/')


class AssignTAToCourse(View):
    def get(self, request, coursename=None):
        user = Person.objects.get(email=request.session['email'])
        if user.permissionLevel != 3 and user.permissionLevel != 2:
            return redirect('/permissiondenied')
        tas = Person.objects.filter(permissionLevel=1).all()
        course = Courses.objects.get(courseName=coursename)
        labs = Labs.objects.filter(course=course).all()
        datas = []
        try:
            for lab in labs:
                datas.append({
                    'courseName': coursename,
                    'section': lab.labName,
                    'tas': lab.assignedTAs.all()
                })
        finally:
            return render(request, "assignTAToCourse.html",
                          {'role': user.permissionLevel, 'coursename': coursename, 'tas': tas, 'datas': datas})

    def post(self, request):
        try:
            course = Courses.objects.get(courseName=request.POST['coursename'])
            lab = Labs.objects.get(course=course, labName=request.POST['courseSection'])
            lab.assignedTAs.add(TA.objects.get(email=request.POST['taEmail']))
            lab.save()
        finally:
            return self.get(request, request.POST['coursename'])

class SignOut(View):
    def get(self, request):
        request.session.flush()
        return redirect('/login')

class EditProfile(View):
    def get(self, request, userEmail=None):
        if userEmail is None:
            user = Person.objects.get(email=request.session['email'])
            return render(request, "editprofile.html", {'user': user, 'role': user.permissionLevel})
        else:
            currentUser = Person.objects.get(email=request.session['email'])
            user = Person.objects.get(email=userEmail)
            return render(request, "editprofile.html", {'user': user, 'role': currentUser.permissionLevel})

    def post(self, request):
        name = request.POST['name']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        try:
            t = Person.objects.get(email=request.POST['email'])
            t.name = name
            t.address = address
            t.phoneNumber = phoneNumber
            t.save()

            return redirect('/profile/{email}'.format(email = request.POST['email']))
        except:
            return redirect('/')

class UserProfile(View):
    def get(self, request, userEmail = None):
        canEdit = False
        try:
            user = Person.objects.get(email = userEmail)
        except:
            return redirect("/permissiondenied")
        if request.session['role'] == 3 or userEmail == request.session['email']:
            canEdit = True
        return render(request, "userprofile.html", {'user': user, 'role': request.session['role'], 'canEdit': canEdit})

class CreateLab(View):
    def get(self, request, coursename=None):
        user = Person.objects.get(email=request.session['email'])
        if user.permissionLevel != 3 and user.permissionLevel != 2:
            return redirect('/permissiondenied')
        return self.returnSingleRender(request, coursename, [], user)

    def post(self, request):
        person = Person.objects.get(email=request.session['email'])
        labSection = str(request.POST['labSection'])
        course = Courses.objects.get(courseName=request.POST['coursename'])
        try:
            Labs.objects.get(labName=labSection, course=course)
            return self.returnSingleRender(request, course.courseName, ["Lab already exists."], person)
        except:
            newLab = Labs(labName=labSection, course=course)
            newLab.save()
            return self.returnSingleRender(request, course.courseName, ["Lab successfully created."], person)

    def returnSingleRender(self, request, coursename, messages, person):
        course = Courses.objects.get(courseName=coursename)
        labs = Labs.objects.filter(course=course).all()
        data = [{
            'name': course.courseName,
            'labs': labs,
        }]
        return render(request, "createLab.html",
                      {"messages": messages, 'role': person.permissionLevel,
                       'coursename': course.courseName, 'sections': labs, 'data': data})

class UserDirectory(View):
    def get(self, request):
        data = Person.objects.all()
        person = Person.objects.get(email=request.session['email'])
        return render(request, "userdirectory.html", {'role': person.permissionLevel, 'users': data})

    def post(self, request):
        pass

class PermissionDenied(View):
    def get(self, request):
        person = Person.objects.get(email=request.session['email'])
        return render(request, "permissiondenied.html", {'role': person.permissionLevel})
